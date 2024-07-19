import requests
import os
from flask import Flask

import time
import threading
# ---- สำหรับ Investor ---
from settrade_v2 import Investor


LINE_TOKEN = os.environ['LINE_TOKEN']
LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
WAITTIME = 30
DIFF_THRESOLD = 1.2


investor_set = Investor(
    app_id=os.environ['SETTRADE_APP_ID'],
    app_secret=os.environ['SETTRADE_APP_SECRET'],
    broker_id=os.environ['SETTRADE_BROKER_ID'],
    app_code=os.environ['SETTRADE_APP_CODE'],
    is_auto_queue=False
)
realtime_set = investor_set.RealtimeDataConnection()


def notify_line(text: str)-> None:
    headersAuth = {
        'Authorization': 'Bearer '+ LINE_TOKEN,
    }
    post_result = requests.post(LINE_NOTIFY_URL, {"message": text}, headers=headersAuth)
    return post_result


def initialize_globals():
    global latest_prices, stop_event, subscriber1, subscriber2
    latest_prices = {
        "INTUCH": None,
        "GULF": None
    }
    stop_event = threading.Event()
    subscriber1 = None
    subscriber2 = None


def stop_subscribers():
    global subscriber1, subscriber2, stop_event
    if subscriber1:
        subscriber1.stop()
    if subscriber2:
        subscriber2.stop()
    stop_event.set()
    print("Stopped subscribers")


def subscribe_intuch(message):
    speical_dividend = 4.5
    new_shares_conversion_rate = 1.69335
    current_price = message['data']['ask_price1']
    adj_price = current_price - speical_dividend
    price_per_new_share = adj_price / new_shares_conversion_rate
    latest_prices["INTUCH"] = price_per_new_share
    calculate_difference()

def subscribe_gulf(message):
    speical_dividend = 0
    new_shares_conversion_rate = 1.02974
    current_price = message['data']['ask_price1']
    adj_price = current_price - speical_dividend
    price_per_new_share = adj_price / new_shares_conversion_rate
    latest_prices["GULF"] = price_per_new_share
    calculate_difference()

def calculate_difference():
    intuch_price = latest_prices.get("INTUCH")
    gulf_price = latest_prices.get("GULF")
    if intuch_price is not None and gulf_price is not None:
        price_difference_short_gulf = (gulf_price - intuch_price)/gulf_price
        price_difference_short_intuch = (intuch_price - gulf_price)/intuch_price
        diff_max = max(abs(price_difference_short_gulf), abs(price_difference_short_intuch))
        print(f"Price Difference: GULF/INTUCH = {diff_max * 100}")
        if diff_max > DIFF_THRESOLD:
            if price_difference_short_gulf > price_difference_short_intuch:
                notify_line(f"price_difference: {diff_max * 100}\n Suggestion: S GULF, L INTUCH")
            else:
                notify_line(f"price_difference: {diff_max * 100}\n Suggestion: L GULF, S INTUCH")
            stop_subscribers()


def start_subscribers():
    global subscriber1, subscriber2, stop_event
    subscriber1 = realtime_set.subscribe_bid_offer("INTUCH", subscribe_intuch)
    subscriber1.start() 
    subscriber2 = realtime_set.subscribe_bid_offer("GULF", subscribe_gulf)
    subscriber2.start()

    def stop_after_timeout():
        stop_subscribers()
        

    timer = threading.Timer(WAITTIME, stop_after_timeout)
    timer.start()

    while not stop_event.is_set():
        time.sleep(0.1)

    timer.cancel()

app = Flask(__name__)



@app.route("/")
def hello_world():
    initialize_globals()

    thread = threading.Thread(target=start_subscribers)
    thread.start()

    thread.join(timeout=5)  # Wait for the thread to finish

    return 'finish'


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))