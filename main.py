import json
import math
import os
import time
from multiprocessing import Pool
from secrets import randbelow

import boto3
import yaml

bracelet_send_delay_in_seconds = 1
bracelet_message_limit = 1_000_000

stream_name = os.environ.get("AWS_KINESIS_STREAM_NAME", None)

kinesis = boto3.client('kinesis', region_name="eu-west-1")


def simulate_smart_bracelet(bracelet: dict):
    customer_id = bracelet["user_id"]
    device_id = bracelet["bracelet_id"]

    # Random number between 50 and 120
    a = randbelow(70) + 50
    # Random number between 70 and 120
    b = randbelow(50) + 70

    for i in range(bracelet_message_limit):
        payload = dict(
            device_id=device_id,
            customer_id=customer_id,
            measured_at=time.time_ns(),
            serendipity=round(float(10.0 + 5.0 * math.sin(i)), 4),
            battery_level=round(float(a * math.sin(i // b) + b), 4)
        )
        kinesis.put_record(
            StreamName=stream_name,
            Data=json.dumps(payload),
            PartitionKey=device_id
        )

        time.sleep(bracelet_send_delay_in_seconds)

    return device_id


def read_config(filepath: str):
    with open(filepath, 'r') as file:
        config = yaml.safe_load(file)

    return config


def bootchecks():
    if not os.getenv("AWS_KINESIS_STREAM_NAME", False):
        print("Set AWS_KINESIS_STREAM_NAME env var first!")
        exit()


def main():
    config = read_config("config.yml")
    bracelets = config.get("bracelets")
    with Pool(len(bracelets)) as pool:
        pool.map(simulate_smart_bracelet, bracelets)


if __name__ == "__main__":
    bootchecks()
    main()
