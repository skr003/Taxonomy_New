#!/usr/bin/env python3
import argparse
import json
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--output", required=True, help="Path to Loki output JSON")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = json.load(f)

    streams = []
    for entry in data:
        log_line = json.dumps(entry)
        streams.append({
            "stream": {"job": "forensic-collector"},
            "values": [[str(int(time.time() * 1e9)), log_line]]
        })

    loki_payload = {"streams": streams}

    with open(args.output, "w") as f:
        json.dump(loki_payload, f, indent=2)

    print("✅ Loki payload generated")

if __name__ == "__main__":
    main()
