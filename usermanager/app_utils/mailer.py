import smtplib
from email.message import EmailMessage
from django.conf import settings

def send_mail(to,subject,message,cc=None,bcc=None):
    emailmessage = EmailMessage()
    emailmessage['To'] = to
    emailmessage['Subject'] = subject
    emailmessage.set_content(message)
    emailmessage['From'] = settings.EMAIL_SENDER
    if cc!=None:
        emailmessage['Cc'] = cc
    if bcc!=None:
        emailmessage['Bcc'] = bcc
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(settings.EMAIL_SENDER, settings.PASS_SENDER)
        server.send_message(emailmessage)
        return True
    except:
        return False


def SubjectAndMessageGenSignup(first_name,otp):
    subject = f"Welcome {first_name} to cttt.com"

    message = f"Your one Time Password {otp} is valid till 5 minutes please do not share this otp with anyone.\n\n\n Thanks\nRegards\ncttt.com"

    return (subject,message)


def SubjectAndMessageGenLogin(otp):
    subject = f"Login Attempt on cttt.com"

    message = f"Your one Time Password {otp} is valid till 5 minutes for login please do not share this otp with anyone.\n\n\n Thanks\nRegards\ncttt.com"

    return (subject,message)

def SubjectAndMessageGenFP(username,token):
    subject = f"Password Change Attempt on cttt.com"

    message = f"Your one Time Password change link is \n\n\n {settings.BASE_URL}forgetpass/user={username}/token={token} is valid till 5 minutes. please do not share this link with anyone.\n\n\n Thanks\nRegards\ncttt.com"


    return (subject,message)


def send_room_token_message(first_name,token):
    subject = f"Welcome {first_name}! to cttt.com Your game token is here!"

    message = f"Hello {first_name} Your Permanent Game token is\n\n\n{token} please keep the record of game token else you'll not be able to play. please <a href='http://cttt.herokuapp.com/play/{token}'>click here to play a game</a> \n\n\n Thanks\nRegards\ncttt.com"

    return (subject,message)



def ConfirmationCPLogin(username,is_fp=True):
    if is_fp:
        subject = "Password Has been Successfully Changed on cttt.com"

        message = f"Hello {username} your password has been successfully changed on cttt.com \n\n\n Thanks\nRegards\ncttt.com"

    else:
        subject = "Successfully Login on cttt.com"

        message = f"Hello {username} You have successfully logged into cttt.com If this is Not You Please Change Password Immediately.\n\n\n Thanks\nRegards\ncttt.com"

    return (subject,message)