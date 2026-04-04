#!/usr/bin/env python3
"""
OpenSIN Competitor Intelligence Scanner
Scans 50+ competitors across GitHub and the web.
"""

import json
import os
import sys
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class CompetitorUpdate:
    name: str
    category: str
    priority: str
    update_type: str  # commit, release, pr, issue, star_milestone, blog, changelog
    title: str
    description: str
    url: str
    timestamp: str
    significance: str  # low, medium, high, critical

class CompetitorScanner:
    def __init__(self, github_token: str = None):
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN", "")
        self.headers = {"Authorization": f"token {self.github_token}"} if self.github_token else {}
        self.competitors = self._load_competitors()
        self.previous_results = self._load_previous_results()
        self.updates: List[CompetitorUpdate] = []

    def _load_competitors(self) -> Dict:
        with open("all-competitors.json") as f:
            return json.load(f)

    def _load_previous_results(self) -> Dict:
        try:
            with open("competitor-research-results.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"last_scan": None, "competitors": {}}

    def scan_all(self) -> List[CompetitorUpdate]:
        """Scan all competitors and return updates."""
        for category, competitors in self.competitors.get("competitors", {}).items():
            for competitor in competitors:
                self._scan_competitor(competitor, category)
        return self.updates

    def scan_by_priority(self, priority: str) -> List[CompetitorUpdate]:
        """Scan only competitors matching the given priority."""
        for category, competitors in self.competitors.get("competitors", {}).items():
            for competitor in competitors:
                if competitor.get("priority") == priority:
                    self._scan_competitor(competitor, category)
        return self.updates

    def scan_by_category(self, category: str) -> List[CompetitorUpdate]:
        """Scan only competitors in the given category."""
        competitors = self.competitors.get("competitors", {}).get(category, [])
        for competitor in competitors:
            self._scan_competitor(competitor, category)
        return self.updates

    def _scan_competitor(self, competitor: Dict, category: str):
        """Scan a single competitor."""
        name = competitor["name"]
        repo = competitor.get("repo", "")
        priority = competitor["priority"]

        # GitHub scanning
        if repo and "/" in repo:
            self._scan_github_commits(name, repo, category, priority)
            self._scan_github_releases(name, repo, category, priority)
            self._scan_github_prs(name, repo, category, priority)
            self._scan_github_issues(name, repo, category, priority)
            self._scan_github_stars(name, repo, category, priority)

        # Web scanning
        if competitor.get("changelog"):
            self._scan_changelog(name, competitor["changelog"], category, priority)

        if competitor.get("website"):
            self._scan_blog(name, competitor["website"], category, priority)

    def _scan_github_commits(self, name: str, repo: str, category: str, priority: str):
        """Scan latest commits for a repo."""
        try:
            resp = requests.get(
                f"https://api.github.com/repos/{repo}/commits?per_page=10",
                headers=self.headers,
                timeout=30
            )
            if resp.status_code == 200:
                commits = resp.json()
                for commit in commits[:5]:
                    sha = commit["sha"][:7]
                    message = commit["commit"]["message"].split("\n")[0]
                    date = commit["commit"]["author"]["date"]
                    author = commit["commit"]["author"]["name"]

                    # Check if this is a new commit since last scan
                    last_scan = self.previous_results.get("last_scan")
                    if last_scan and date > last_scan:
                        self.updates.append(CompetitorUpdate(
                            name=name,
                            category=category,
                            priority=priority,
                            update_type="commit",
                            title=f"{author}: {message}",
                            description=f"Commit {sha} by {author}",
                            url=f"https://github.com/{repo}/commit/{sha}",
                            timestamp=date,
                            significance="high" if priority == "CRITICAL" else "medium"
                        ))
        except Exception as e:
            print(f"Error scanning commits for {name}: {e}")

    def _scan_github_releases(self, name: str, repo: str, category: str, priority: str):
        """Scan latest releases for a repo."""
        try:
            resp = requests.get(
                f"https://api.github.com/repos/{repo}/releases?per_page=5",
                headers=self.headers,
                timeout=30
            )
            if resp.status_code == 200:
                releases = resp.json()
                for release in releases[:3]:
                    tag = release["tag_name"]
                    published = release["published_at"]
                    body = release.get("body", "")[:200]

                    last_scan = self.previous_results.get("last_scan")
                    if last_scan and published > last_scan:
                        self.updates.append(CompetitorUpdate(
                            name=name,
                            category=category,
                            priority=priority,
                            update_type="release",
                            title=f"Release {tag}",
                            description=body,
                            url=release["html_url"],
                            timestamp=published,
                            significance="critical"
                        ))
        except Exception as e:
            print(f"Error scanning releases for {name}: {e}")

    def _scan_github_prs(self, name: str, repo: str, category: str, priority: str):
        """Scan merged PRs for a repo."""
        try:
            resp = requests.get(
                f"https://api.github.com/repos/{repo}/pulls?state=closed&per_page=10",
                headers=self.headers,
                timeout=30
            )
            if resp.status_code == 200:
                prs = resp.json()
                for pr in prs[:5]:
                    if pr.get("merged_at"):
                        title = pr["title"]
                        merged = pr["merged_at"]
                        user = pr["user"]["login"]

                        last_scan = self.previous_results.get("last_scan")
                        if last_scan and merged > last_scan:
                            self.updates.append(CompetitorUpdate(
                                name=name,
                                category=category,
                                priority=priority,
                                update_type="pr",
                                title=f"PR merged: {title}",
                                description=f"PR #{pr['number']} by {user}",
                                url=pr["html_url"],
                                timestamp=merged,
                                significance="medium"
                            ))
        except Exception as e:
            print(f"Error scanning PRs for {name}: {e}")

    def _scan_github_issues(self, name: str, repo: str, category: str, priority: str):
        """Scan closed issues for significant features."""
        try:
            resp = requests.get(
                f"https://api.github.com/repos/{repo}/issues?state=closed&per_page=10",
                headers=self.headers,
                timeout=30
            )
            if resp.status_code == 200:
                issues = resp.json()
                for issue in issues[:5]:
                    if "pull_request" not in issue:
                        title = issue["title"]
                        closed = issue["closed_at"]

                        last_scan = self.previous_results.get("last_scan")
                        if last_scan and closed > last_scan:
                            self.updates.append(CompetitorUpdate(
                                name=name,
                                category=category,
                                priority=priority,
                                update_type="issue",
                                title=f"Feature: {title}",
                                description=f"Issue #{issue['number']} closed",
                                url=issue["html_url"],
                                timestamp=closed,
                                significance="low"
                            ))
        except Exception as e:
            print(f"Error scanning issues for {name}: {e}")

    def _scan_github_stars(self, name: str, repo: str, category: str, priority: str):
        """Check for star milestones."""
        try:
            resp = requests.get(
                f"https://api.github.com/repos/{repo}",
                headers=self.headers,
                timeout=30
            )
            if resp.status_code == 200:
                data = resp.json()
                stars = data.get("stargazers_count", 0)

                # Check for milestones
                milestones = [1000, 5000, 10000, 25000, 50000, 100000, 200000, 500000]
                prev_stars = self.previous_results.get("competitors", {}).get(name, {}).get("stars", 0)

                for milestone in milestones:
                    if prev_stars < milestone <= stars:
                        self.updates.append(CompetitorUpdate(
                            name=name,
                            category=category,
                            priority=priority,
                            update_type="star_milestone",
                            title=f"\u2b50 {stars} stars! (crossed {milestone} milestone)",
                            description=f"Reached {stars} GitHub stars",
                            url=f"https://github.com/{repo}/stargazers",
                            timestamp=datetime.utcnow().isoformat(),
                            significance="high"
                        ))
                        break
        except Exception as e:
            print(f"Error scanning stars for {name}: {e}")

    def _scan_changelog(self, name: str, url: str, category: str, priority: str):
        """Scan changelog URL for updates."""
        try:
            resp = requests.get(url, timeout=30, headers={"User-Agent": "OpenSIN-Scanner/1.0"})
            if resp.status_code == 200:
                # Simple check - if page changed since last scan
                content_hash = hashlib.md5(resp.text.encode()).hexdigest()
                prev_hash = self.previous_results.get("competitors", {}).get(name, {}).get("changelog_hash", "")

                if content_hash != prev_hash:
                    self.updates.append(CompetitorUpdate(
                        name=name,
                        category=category,
                        priority=priority,
                        update_type="changelog",
                        title=f"Changelog updated",
                        description=f"Changelog page changed: {url}",
                        url=url,
                        timestamp=datetime.utcnow().isoformat(),
                        significance="medium"
                    ))
        except Exception as e:
            print(f"Error scanning changelog for {name}: {e}")

    def _scan_blog(self, name: str, website: str, category: str, priority: str):
        """Scan blog/website for announcements."""
        blog_urls = [
            f"{website}/blog",
            f"{website}/changelog",
            f"{website}/news",
            f"{website}/updates",
        ]

        for blog_url in blog_urls:
            try:
                resp = requests.get(blog_url, timeout=30, headers={"User-Agent": "OpenSIN-Scanner/1.0"})
                if resp.status_code == 200:
                    content_hash = hashlib.md5(resp.text.encode()).hexdigest()
                    prev_hash = self.previous_results.get("competitors", {}).get(name, {}).get("blog_hash", "")

                    if content_hash != prev_hash:
                        self.updates.append(CompetitorUpdate(
                            name=name,
                            category=category,
                            priority=priority,
                            update_type="blog",
                            title=f"Blog/website updated",
                            description=f"Page changed: {blog_url}",
                            url=blog_url,
                            timestamp=datetime.utcnow().isoformat(),
                            significance="medium"
                        ))
                        break
            except Exception:
                continue

    def generate_report(self) -> Dict:
        """Generate a comprehensive scan report."""
        report = {
            "last_scan": datetime.utcnow().isoformat(),
            "total_updates": len(self.updates),
            "critical_updates": [asdict(u) for u in self.updates if u.significance == "critical"],
            "high_updates": [asdict(u) for u in self.updates if u.significance == "high"],
            "medium_updates": [asdict(u) for u in self.updates if u.significance == "medium"],
            "low_updates": [asdict(u) for u in self.updates if u.significance == "low"],
            "competitors": {},
            "summary": {
                "by_type": {},
                "by_priority": {},
                "by_category": {}
            }
        }

        # Group updates by competitor
        for update in self.updates:
            update_dict = asdict(update)
            if update.name not in report["competitors"]:
                report["competitors"][update.name] = []
            report["competitors"][update.name].append(update_dict)

            # Count by type
            report["summary"]["by_type"][update.update_type] = report["summary"]["by_type"].get(update.update_type, 0) + 1
            report["summary"]["by_priority"][update.priority] = report["summary"]["by_priority"].get(update.priority, 0) + 1
            report["summary"]["by_category"][update.category] = report["summary"]["by_category"].get(update.category, 0) + 1

        return report

    def format_telegram_message(self, report: Dict) -> str:
        """Format report for Telegram notification."""
        msg = "\U0001f50d OpenSIN Competitor Intelligence Report\n"
        msg += f"\U0001f4c5 {report['last_scan'][:10]}\n"
        msg += f"\U0001f4ca {report['total_updates']} updates found\n\n"

        if report["critical_updates"]:
            msg += "\U0001f6a8 CRITICAL:\n"
            for u in report["critical_updates"]:
                msg += f"  \u2022 {u['name']}: {u['title']}\n"
            msg += "\n"

        if report["high_updates"]:
            msg += "\u26a0\ufe0f HIGH:\n"
            for u in report["high_updates"]:
                msg += f"  \u2022 {u['name']}: {u['title']}\n"
            msg += "\n"

        if report["medium_updates"]:
            msg += f"\U0001f536 MEDIUM ({len(report['medium_updates'])} updates):\n"
            for u in report["medium_updates"][:10]:
                msg += f"  \u2022 {u['name']}: {u['title']}\n"
            if len(report["medium_updates"]) > 10:
                msg += f"  ... and {len(report['medium_updates']) - 10} more\n"
            msg += "\n"

        msg += "\U0001f4dd Summary by type:\n"
        for type_name, count in report["summary"]["by_type"].items():
            msg += f"  \u2022 {type_name}: {count}\n"

        msg += "\n\U0001f4bb Full report: competitor-research-results.json"
        return msg

    def format_discord_embed(self, report: Dict) -> Dict:
        """Format report for Discord embed."""
        embed = {
            "title": "\U0001f50d OpenSIN Competitor Intelligence Report",
            "color": 0x5865F2,
            "timestamp": report["last_scan"],
            "fields": [
                {
                    "name": "\U0001f4ca Summary",
                    "value": f"{report['total_updates']} total updates",
                    "inline": True
                }
            ],
            "footer": {
                "text": "OpenSIN Competitor Scanner"
            }
        }

        if report["critical_updates"]:
            embed["fields"].append({
                "name": "\U0001f6a8 Critical Updates",
                "value": "\n".join(f"**{u['name']}**: {u['title']}" for u in report["critical_updates"]),
                "inline": False
            })

        if report["high_updates"]:
            embed["fields"].append({
                "name": "\u26a0\ufe0f High Priority Updates",
                "value": "\n".join(f"**{u['name']}**: {u['title']}" for u in report["high_updates"]),
                "inline": False
            })

        type_summary = "\n".join(f"{t}: {c}" for t, c in report["summary"]["by_type"].items())
        embed["fields"].append({
            "name": "\U0001f4dd Updates by Type",
            "value": type_summary,
            "inline": True
        })

        return embed

    def save_results(self, report: Dict):
        """Save scan results to file."""
        with open("competitor-research-results.json", "w") as f:
            json.dump(report, f, indent=2)


if __name__ == "__main__":
    scanner = CompetitorScanner()

    # Support command-line filtering
    if len(sys.argv) > 1:
        if sys.argv[1].startswith("--priority="):
            priority = sys.argv[1].split("=")[1]
            scanner.scan_by_priority(priority)
        elif sys.argv[1].startswith("--category="):
            category = sys.argv[1].split("=")[1]
            scanner.scan_by_category(category)
        else:
            scanner.scan_all()
    else:
        scanner.scan_all()

    report = scanner.generate_report()
    scanner.save_results(report)

    # Print Telegram message
    print(scanner.format_telegram_message(report))
