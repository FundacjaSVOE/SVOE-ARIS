"""
ARIS Collector
Animal Rescue Intelligence System

First prototype:
- starts collector
- reads project configuration
- checks system status
"""

import os
import sys
import yaml
from datetime import datetime


def load_config():
    """Load ARIS configuration searching in probable directories."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(base_dir, ".."))

    # Варианты возможных путей к конфигу
    possible_paths = [
        os.path.join(repo_root, "docs", "project.yaml"),
        os.path.join(repo_root, "config", "project.yaml"),
        os.path.join(repo_root, "project.yaml"),
    ]

    config_path = None
    for path in possible_paths:
        if os.path.exists(path):
            config_path = path
            break

    if not config_path:
        print(f"[ERROR] Configuration file 'project.yaml' not found!")
        print(f"[ERROR] Searched locations:")
        for path in possible_paths:
            print(f" - {path}")
        raise FileNotFoundError("Unable to locate project.yaml")

    print(f"[INFO] Loading configuration from: {config_path}")
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():
    print("=" * 40)
    print("ARIS Collector started")
    print("=" * 40)

    try:
        config = load_config()
    except Exception as e:
        print(f"[FATAL] Error loading configuration: {e}")
        sys.exit(1)

    project = config.get("project", {})

    print(f"Project: {project.get('name', 'N/A')}")
    print(f"Version: {project.get('version', 'N/A')}")

    print()
    print("Languages:")
    for lang in config.get("languages", []):
        print("-", lang)

    print()
    print("Collector time:", datetime.now())

    print()
    print("Checking sources...")
    sources = config.get("sources", {})
    countries = sources.get("countries", [])

    for country in countries:
        print("Source region:", country)

    print()
    print("Found articles: 0")
    print("Collector finished successfully")


if __name__ == "__main__":
    main()
