import yaml
import json
from pathlib import Path
from src.dev_hostname.device_manager import get_hostname
from src.dev_hostname.log_config import setup_logging


INVENTORY_PATH = Path("../inventory")
OUTPUT_PATH = Path("output")


def load_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)["devices"]


def load_all_devices():
    all_devices = []
    files = ["ios-devices.yml", "ocnos-devices.yml"]

    for file in files:
        full_path = INVENTORY_PATH / file

        try:
            devices = load_yaml(full_path)
            all_devices.extend(devices)

        except FileNotFoundError:
            print(f"Missing inventory files: {file}")

    return all_devices


def main():
    logger = setup_logging()
    devices = load_all_devices()

    results = {}

    for device in devices:
        if not isinstance(device, dict):
            logger.error(f"Invalid device entry: {device}")
            continue

        try:
            hostname = get_hostname(device)
            results[device["host"]] = hostname

        except Exception as e:
            logger.error(f"Skipping {device['host']} - {e}")

    print("\n=== Hostname Results ===")
    for ip, hostname in results.items():
        print(f"{ip} -> {hostname}")

    OUTPUT_PATH.mkdir(exist_ok=True)

    output_file = OUTPUT_PATH / "hostnames.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()
