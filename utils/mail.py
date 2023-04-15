from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email(title: str, tpl_name: str, ctx: dict, recipients: list) -> None:
    tpl = render_to_string(tpl_name, ctx)
    print(tpl)
    email = EmailMessage(subject=title, body=tpl, from_email=settings.DEFAULT_FROM_EMAIL, to=recipients)
    email.content_subtype = "html"  # Main content is now text/html
    email.send()
    return None
