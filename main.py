import math
import os
from dotenv import load_dotenv

import time

load_dotenv()


timetosleep = int(os.getenv('MY_ENV_TIMETOSLEEP'))

#battito(int), passi(int), velocità(double)


def main():
    while (True):
        y = 0
        x = 1000
        for y in range(x):
            battito=int(math.sin(y/100+30)*60+120)
            Velocità=math.sin(y/100)*6+6
            passi=int(y+y/50)
            print(battito)
            print(Velocità)
            print(passi)

            time.sleep(timetosleep)


if __name__ == "__main__":
    main()

"""
funzione battito cardiaco f(x)=sin(((x)/(100)))*60+120
funzione velocità f(x)=sin(((x)/(100)))*6+6
funzione passi f(x)=((x^(2))/(50))


"""
