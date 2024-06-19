#!/usr/bin/env python3
import sys
import json
import argparse
from .executor import executor


def load_json(filename: str) -> dict:
    with open(filename, encoding="utf-8") as fh:
        return json.load(fh)


def run():
    parser = argparse.ArgumentParser(description="Finance Reporter for Titan")
    parser.add_argument("-s", "--service", required=True, type=str, help="service name")
    parser.add_argument("-j", "--json", required=True, type=str, help="json file")
    args = parser.parse_args()
    service = args.service
    filename = args.json
    params = load_json(filename)
    executor(service, params)


if __name__ == "__main__":
    sys.exit(run())
