from django.shortcuts import render, redirect
from django.views.decorators.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMessage
from gmailapi_backend import mail

from portfolio_backend.settings import EMAIL_HOST_USER

backend = mail.GmailBackend()


# Create your views here.
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})


@csrf_exempt
def submit_form(request):
    print("reached")
    if request.method == "POST":
        print(request.POST)
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        # email form processing
        subject = f"PORTFOLIO CONTACT {first_name} {last_name}"
        sender_email = EMAIL_HOST_USER
        recipient_email = 'tnyadza@gmail.com'

        # Send email
        message = EmailMessage(
            subject=subject,
            body=request.POST["message"] + '\n\n' + 'email:\n' + request.POST["email"],
            to=[recipient_email],
        )
        try:
            backend.send_messages([message])
            return JsonResponse({'success': True, 'formsubmitted': True, 'message': 'Form submitted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        data = {'error': 'Only POST requests are allowed'}
        return JsonResponse(data, status=400)
