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








# # Download the helper library from https://www.twilio.com/docs/python/install
# from twilio.rest import Client
#
#
# # Your Account Sid and Auth Token from twilio.com/console
# # DANGER! This is insecure. See http://twil.io/secure
# account_sid = 'AC2ada64bbf0631ec1ec778efcb405c1b3'
# auth_token = '804b432d43528cbacda1af5ec166b7f5'
# client = Client(account_sid, auth_token)
#
# service = client.verify.services.create(
#                                      friendly_name='My First Verify Service'
#                                  )
#
# print(service.sid)
#
#
# # Download the helper library from https://www.twilio.com/docs/python/install
# from twilio.rest import Client
#
#
# # Your Account Sid and Auth Token from twilio.com/console
# # DANGER! This is insecure. See http://twil.io/secure
# account_sid = 'AC2ada64bbf0631ec1ec778efcb405c1b3'
# auth_token = '804b432d43528cbacda1af5ec166b7f5'
# client = Client(account_sid, auth_token)
#
# verification_check = client.verify.services('VA58f31fc08ffd785d17a95b8b1e73f6a2').verification_checks.create(to='+14158775175', code='123456')
#
# print(verification_check.status)