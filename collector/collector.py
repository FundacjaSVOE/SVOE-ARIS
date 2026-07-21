
"""
ARIS Collector
Animal Rescue Intelligence System

First prototype:
- starts collector
- reads project configuration
- checks system status
"""

import os
import yaml
from datetime import datetime


def load_config():
    """Load ARIS configuration"""

    path = "../config/project.yaml"

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():

    print("=" * 40)
    print("ARIS Collector started")
    print("=" * 40)

    config = load_config()

    project = config["project"]

    print(f"Project: {project['name']}")
    print(f"Version: {project['version']}")

    print()
    print("Languages:")

    for lang in config["languages"]:
        print("-", lang)

    print()
    print("Collector time:", datetime.now())

    print()
    print("Checking sources...")

    countries = config["sources"]["countries"]

    for country in countries:
        print("Source region:", country)

    print()
    print("Found articles: 0")
    print("Collector finished")


if __name__ == "__main__":
    main()
