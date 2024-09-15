"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json
import requests
import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests




N: int = 3
sample_ms = 10.0
on_ms = 500
database_api_url = 'https://ece463miniproject-default-rtdb.firebaseio.com/scores.json'

def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]
    
    max_val=-1
    min_val=-1
    avg_val=-1
    score=-1
    
    size = len(t_good)
    if size!=0:
        max_val = max(t_good)
        min_val = min(t_good)
        avg_val = (sum(t_good))/size
        score = size/len(t)

    print(t_good)
    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]
    data = {
        "minimum": min_val,
        "maximum":max_val,
        "average_response_time":avg_val,
        "score":score
        }
    
    #payload = dict(minimum=min_val, maximum=max_val, average_response_time=avg_val,score=score)
    #payload = json.dumps(data)
    
    #j = json.loads(payload)

    # %% make dynamic filename and write JSON

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    print("write", filename)

    write_json(filename, data)
    response = requests.post(database_api_url, json = data)
    print(response.status_code)


if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files

    # Connect to network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Fill in your network name (ssid) and password here:
    ssid = "BU Guest (unencrypted)"
    password = ""
    wlan.connect(ssid, password)
    
    #adding the following line;
    print("Am I Connected??")
    print(wlan.isconnected())
    
    x = requests.get('https://ece463miniproject-default-rtdb.firebaseio.com/')
    print(x.status_code)


    
    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)

