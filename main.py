import boto3
import uuid
import os
import json
import math
from secrets import randbelow
from multiprocessing import Pool
import time

bracelet_count = 5
bracelet_send_delay_in_seconds = 1
bracelet_message_limit = 1_000_000

stream_name = os.environ.get("AWS_KINESIS_STREAM_NAME", None)

kinesis = boto3.client('kinesis', region_name="eu-west-1")


def simulate_smart_bracelet(_):
    customer_id = str(uuid.uuid4())
    device_id = str(uuid.uuid4())

    # Random number between 50 and 120
    a = randbelow(70) + 50
    # Random number between 70 and 120
    b = randbelow(50) + 70

    for i in range(bracelet_message_limit):
        payload = dict(
            device_id=device_id,
            customer_id=customer_id,
            measured_at=time.time_ns(),
            serendipity=(10.0 + 5.0 * math.sin(i)),
            battery=float(a * math.sin(i // b) + b)
        )
        kinesis.put_record(
            StreamName=stream_name,
            Data=json.dumps(payload),
            PartitionKey=device_id
        )

        time.sleep(bracelet_send_delay_in_seconds)

    return device_id

def bootchecks():
    if not os.getenv("AWS_KINESIS_STREAM_NAME", False):
        print("Set AWS_KINESIS_STREAM_NAME env var first!")
        exit()

def main():
    with Pool(bracelet_count) as pool:
        pool.map(
            simulate_smart_bracelet,
            list(range(bracelet_count))
        )

if __name__ == "__main__":
    bootchecks()
    main()
