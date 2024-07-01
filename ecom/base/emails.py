




from django.core.mail import send_mail
from django.conf import settings

def send_account_activation_email(email, email_token):
    email_receiver = email
    subject = 'Activate Your Account'
    activation_link = f'http://127.0.0.1:8000/accounts/activate/{email_token}/'
    body = f'This is your account activation link: <a href="{activation_link}">{activation_link}</a>'
    
    send_mail(
        subject,
        '',
        settings.EMAIL_HOST_USER,
        [email_receiver],
        html_message=body,  # Use html_message to include HTML content
        fail_silently=False,
    )








# # from  django.conf import settings
# # from django.core.mail import send_mail
# # import requests
# from email.message import EmailMessage
# import os
# from twilio.rest import Client
# import ssl
# import smtplib

# def send_account_activation_email(email,email_token):
   
#     email_sender='patel.prerak2798@gmail.com'
#     email_password='zoqj hguo hxsd lxur'
    
#     email_receiver=email
#     subject='Activate Your account'
#     body=f'this is your account activation link http://127.0.0.1:8000:/accounts/activate/{email_token} '
#     em=EmailMessage()
#     em['From']=email_sender
#     em['To']=email_receiver
#     em['Subject']=subject
#     em.set_content(body)
#     context=ssl.create_default_context()        
#     with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
#         smtp.login(email_sender,email_password)
#         smtp.sendmail(email_sender,email_receiver,em.as_string())
    
    

#     # # your API secret from (Tools -> API Keys) page
#     # apiSecret = "b3b0716d8e4c346f7b4ca801e355da8388307b63"
#     # deviceId = "DEVICE-Id"
#     # phone = '+91**********'
#     # message = 'Hello! messy programmer, sending from python'

#     # message = {
#     #     "secret": apiSecret,
#     #     "mode": "devices",
#     #     "device": deviceId,
#     #     "sim": 1,
#     #     "priority": 1,
#     #     "phone": phone,
#     #     "message": message
#     # }

#     # r = requests.post(url = "https://www.cloud.smschef.com/api/send/sms", params = message)
    
#     # # do something with response object
#     # result = r.json()

#     # print(result)
   
   
   
   
   
   
   