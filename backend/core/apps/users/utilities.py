from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from core.config.settings import DOMAIN

def send_welcome_email(to_email, referral_id):

    context = {
        "referral_code": referral_id,
        "domain": DOMAIN
    }

    text_content = render_to_string("mail/welcome.txt", context=context)
    msg = EmailMultiAlternatives(
        subject="Welcome to the Two Cents waitlist",
        from_email="Malfy from Two Cents <malfy@two-cents.ca>",
        body=text_content,
        to=(to_email,)
    )
    html_content = render_to_string("mail/welcome.html", context)
    msg.attach_alternative(html_content, "text/html")
    msg.send()