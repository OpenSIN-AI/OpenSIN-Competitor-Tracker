#!/usr/bin/env python3
"""Webhook handler for n8n competitor scanner."""

from flask import Flask, request, jsonify
from scanner import CompetitorScanner
import json
import os

app = Flask(__name__)

@app.route("/scan", methods=["POST"])
def trigger_scan():
    """Trigger a competitor scan."""
    data = request.json or {}
    priority_filter = data.get("priority")  # CRITICAL, HIGH, MEDIUM, LOW
    category_filter = data.get("category")  # AI Coding Agents, etc.

    scanner = CompetitorScanner()

    if priority_filter:
        scanner.scan_by_priority(priority_filter)
    elif category_filter:
        scanner.scan_by_category(category_filter)
    else:
        scanner.scan_all()

    report = scanner.generate_report()
    scanner.save_results(report)

    # Filter results if needed
    if priority_filter:
        report["competitors"] = {
            k: v for k, v in report["competitors"].items()
            if any(u["priority"] == priority_filter for u in v)
        }

    return jsonify(report)

@app.route("/report", methods=["GET"])
def get_report():
    """Get the latest scan report."""
    try:
        with open("competitor-research-results.json") as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({"error": "No scan results found. Run /scan first."}), 404

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "competitor-scanner"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
