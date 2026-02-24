import json
import logging

def read_json(file_path):
    try:
        with open(file_path) as f:
            data = json.load(f)
        logging.info("JSON file loaded successfully")
        return data
    except Exception as e:
        logging.error(f"Failed to read JSON: {e}")
        raise


def print_summary(data):
    print("\nApplication:", data.get("application"))
    print("Environment:", data.get("environment"))

    print("\nServices:")
    for service in data.get("services", []):
        print(f"- {service['name']} ({service['region']}) → {service['status']}")
