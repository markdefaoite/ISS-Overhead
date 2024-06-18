import smtplib

import requests
from datetime import datetime

MY_LAT = 40.774097  # Your latitude
MY_LONG = -73.971723  # Your longitude
MY_EMAIL = "someone@gmail.com"
MY_PASSWORD = "################"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


# Your position is within +5 or -5 degrees of the ISS position.
def is_iss_close():
    lat_within_5 = (MY_LAT - 5) < iss_latitude < (MY_LAT + 5)
    lng_within_5 = (MY_LONG - 5) < iss_longitude < (MY_LONG + 5)

    if lat_within_5 and lng_within_5:
        return True
    else:
        return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = int(str(datetime.now()).split(" ")[1].split(":")[0])

is_dark = sunset < time_now or time_now < sunrise
iss_close = is_iss_close()


if is_dark and iss_close:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                            msg=f"Subject: Look up in the sky!\n\nThe ISS is currently nearby!")

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
