from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import smtplib, ssl


@csrf_exempt

def SendEmail(email, leave):
    try:
        port = 587  # For starttls
        smtp_server = settings.EMAIL_HOST
        sender_email = settings.EMAIL_HOST_USER
        receiver_email = email
        password = settings.EMAIL_HOST_PASSWORD

        # message = f"""\
        # Subject: Leave Status

        # Leave Status : {leave_status}  """

        subject="Leave Status"
        text= f"""
        Leave Id: {leave.id}
        From date: {leave.from_date}
        Till date: {leave.till_date}
        Reason: {leave.reason}
        Leave Status: {leave.leave_status_text}

        """

        message= 'Subject: {}\n\n {}'.format(subject,text)

        context = ssl.create_default_context()

        with smtplib.SMTP(smtp_server, port) as server:
            # server.ehlo()  # To initiate communication between client and SMTP server
            server.starttls(context=context)
            # server.ehlo()  
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        return True
    except Exception as error:
        print("Error", error)
        return False
        # return JsonResponse({"error": str(error)})




# @csrf_exempt
# def email():
#     try:
#         port = 587  # For starttls
#         smtp_server = settings.EMAIL_HOST
#         sender_email = settings.EMAIL_HOST_USER
#         receiver_email = email
#         password = settings.EMAIL_HOST_PASSWORD

#         message = f"""\
#         Leave Status"""

#     except Exception as error:
#         print("Error", error)
#         return False
