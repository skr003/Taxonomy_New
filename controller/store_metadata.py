#!/usr/bin/env python3
import argparse
import json
from pymongo import MongoClient

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-uri", required=True, help="MongoDB Atlas URI")
    parser.add_argument("--input", required=True, help="Path to JSON file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = json.load(f)

    client = MongoClient(args.mongo_uri)
    db = client.forensic
    collection = db.metadata

    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

    print("✅ Metadata pushed to MongoDB Atlas")

if __name__ == "__main__":
    main()
