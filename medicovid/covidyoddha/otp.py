import twilio
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import random # generate random number
otp = random.randint(1000,9999)

account_sid = ''
auth_token = ''
def send_otp(account_sid, auth_token, body, from_, to_):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        #body='Hello Mr. Datta Your Secure Device OTP is - ' + str(otp) + 'now your mobile is hacked!\n Byby...',
        body = body,
        from_='+#',
        to=to_
    )

    return otp

# def generate_otp():
#     import math, random
#     digits = "0123456789"
#     OTP = ""
#     for i in range(6):
#         OTP += digits[math.floor(random.random()*10)]
#
#     return OTP
