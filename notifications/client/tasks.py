from django.utils import timezone, dateparse
from django.core.mail import send_mail

import os

from core.celery import app
from celery import group

from .models import Client
from .utils import generate_message_string
from mailing.models import Message, Mailing

import requests


@app.task
def send_client_mailing(
        client_phone_number,
        client_id,
        mailing_text,
        end_mailing,
        mailing_id,
        task_id=None
):
    """
    Sends a notification to the client,
    store the response data to :model:`mailing.Mailing`.
    """
    if timezone.now() > dateparse.parse_datetime(end_mailing):
        return 'Time is over'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("TOKEN")}'
    }
    json = {
        'id': task_id,
        'phone': client_phone_number,
        'text': mailing_text,
    }
    endpoint = f"{os.getenv('ENDPOINT')}/{task_id}"
    response = requests.post(endpoint, json=json, headers=headers)
    Message.objects.create(
        mailing_send=timezone.now(),
        mailing_status=response.status_code,
        mailing_id_id=mailing_id,
        client_id_id=client_id
    )


@app.task
def run_client_mailing(pk):
    """
    Groups `send_client_mailing` tasks  and run it
    """
    mail = Mailing.objects.get(pk=pk)

    if mail.client_filter.filter_type == mail.client_filter.TAG:
        clients = Client.objects.filter(
            tag__tag_name=mail.client_filter.filter_value)
    else:
        clients = Client.objects.filter(
            operator_code=mail.client_filter.filter_value)
    return group(
        send_client_mailing.s(
            client.phone_number,
            client.pk,
            mail.message_text,
            mail.end_mailing_time,
            mail.pk,
            task_id=index)
        for index, client in enumerate(clients)
    )()


@app.task
def send_mail_every_day():
    """
    Sends a mail with statistic about mailings launched today
    """
    send_mail(
        f'Hello, it\'s every day statistics.',
        generate_message_string(),
        os.getenv('EMAIL_HOST_USER'),
        [os.getenv('EMAIL_USER')],
        fail_silently=False
    )
