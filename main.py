import requests
import smtplib
from datetime import datetime

MY_LAT = #  Your latitude #
MY_LONG = # Your longitude #
MY_EMAIL = # your email #
PASSWORD = # your password #

# ---------------ISS Location--------------#

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()
iss_lat = float(data['iss_position']['latitude'])
iss_long = float(data['iss_position']['longitude'])


# ----------------My Location-------------#
parameters = {
    'lat': MY_LAT,
    'lng': MY_LONG,
    'formatted': 0,
    'tzid': 'America/Los_Angeles'
}

# ---------------Sunrise and Sunset--------#
response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
response.raise_for_status()
data = response.json()

sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

# -------------Email Logic-----------------#
now = datetime.now()
message = 'The ISS space station is over you and is observable. You can go outside and try to find it.'
if (now.hour >= sunset or now.hour <= sunrise) and (MY_LAT - 5 < iss_lat < MY_LAT + 5) and (MY_LONG - 5 < iss_long < MY_LONG + 5):
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f'Subject: ISS Space Station\n\n{message}'
        )

