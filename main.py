import requests
from datetime import datetime
import smtplib
import time
import os

MY_EMAIL = os.environ.get("SENDER_EMAIL")
PASSWORD = os.environ.get("SENDER_PASS")
EMAIL_TO = os.environ.get("RECEIVER_EMAIL")

ISS_URL = "http://api.open-notify.org/iss-now.json"
SUNRISE_SUNSET_URL = "https://api.sunrise-sunset.org/json"

LAT = 24.860735  # your latitude
LONG = 67.001137  # your longitude


def is_iss_overhead():

    # will return the live data from the following URL, by request API.
    response = requests.get(url=ISS_URL)

    # will show the specified error on console if there's any
    response.raise_for_status()

    # converts the data to json format
    data = response.json()

    # extracting longitude and latitude from dictionary
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    # if both longitude and latitude are in +/- 5 range, than visible condition is true
    if LAT - 5 <= iss_latitude <= LAT + 5 and LONG - 5 <= iss_longitude <= LONG + 5:
        return True


def is_night():
    # formatted 0, turns the 12 hours default time pattern to 24 hours  pattern
    parameters = {
        "lat": LAT,
        "lng": LONG,
        "formatted": 0,
    }

    # some API's requires parameters to run and operate, below will tell the sunrise and sunset time by taking
    # lat and lng
    response_2 = requests.get(url=SUNRISE_SUNSET_URL, params=parameters)
    response_2.raise_for_status()

    data_2 = response_2.json()

    sunrise = data_2["results"]["sunrise"]
    sunset = data_2["results"]["sunset"]
    # raw data without formatting
    # print(sunrise)
    # print(sunset)

    # adding 5 to convert the UTC time to karachi's local time
    local_sunrise = int(sunrise.split("T")[1].split(":")[0]) + 5
    local_sunset = int(sunset.split("T")[1].split(":")[0]) + 5

    # that's how we extract the hour from sunrise/sunset key's values, you can see above
    print(local_sunrise)
    print(local_sunset)

    time_now = datetime.now()
    # current hour
    print(time_now.hour)
    # if it's dark enough like after sunset and before sunrise, than it will return true
    if local_sunset <= time_now.hour or time_now.hour <= local_sunrise:
        return True


while True:
    # 1 sec of delay in every round
    time.sleep(60)

    if is_iss_overhead() and is_night():

        # builts a connection between email and email provider's server
        with smtplib.SMTP("smtp.gmail.com") as connection:
            # securing the connection we built, by transport layer security
            connection.starttls()
            # logging in
            connection.login(user=MY_EMAIL, password=PASSWORD)
            # sending mail, before \n\n there's a  subject and after there is a body of code
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=EMAIL_TO,
                                msg="Subject: ISS UP\n\nYou can see the ISS right now, it's above your head")
