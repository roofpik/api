import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('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'))
from_email = Email("no-reply@roofpik.com")
subject = "Hello World from the SendGrid Python Library!"
to_email = Email("arpit@roofpik.com")
content = Content("text/plain", "Hello, Email!")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
