import math
import os
import time
from dotenv import load_dotenv
import boto3
import json
from datetime import datetime
import uuid
load_dotenv()

"""
Formule:

funzione battito(int) cardiaco f(x)=sin(((x)/(100)))*60+120
funzione velocità(int) f(x)=sin(((x)/(100)))*6+6
funzione passi(double) f(x)=((x^(2))/(10))

"""

client = boto3.client('kinesis')


# setup variable
try:
    timetosleep = int(os.getenv('MY_ENV_TIMETOSLEEP'))

except:
    print("error get variable MY_ENV_TIMETOSLEEP, missing or error type")
    exit()


def beat(x):
    return int(math.sin(x/100+30)*60+120)


def velocity(x):
    return math.sin(x/100)*6+6


def steps(x):
    return int((x ^ 2)/10)


def main():
    x = 0
    while (True):
        # get parameters
        print(beat(x))
        print(velocity(x))
        print(steps(x))

        # pause
        time.sleep(1)
        data = {
            "beat": beat(x),
            "velocity": velocity(x),
            "steps": steps(x)
        }
   #     base64_bytes= str(data).encode('base64','strict')
        b64data=json.dumps(data).encode('utf-8')
        print(
            client.put_record(
            StreamName='clod2021-gruppo5-smart-bracelet',
            Data=b64data,
            PartitionKey=str(uuid.uuid4())

            )
        )

        # next
        x += 1


if __name__ == "__main__":
    main()
