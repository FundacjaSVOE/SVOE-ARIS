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
    """Load ARIS configuration using dynamic base path resolution."""
    # Получаем абсолютный путь к папке, где находится сам скрипт collector.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Файл конфигурации находится в папке docs на уровень выше
    config_path = os.path.join(base_dir, "..", "docs", "project.yaml")
    config_path = os.path.normpath(config_path)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():
    print("=" * 40)
    print("ARIS Collector started")
    print("=" * 40)

    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading configuration: {e}")
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
