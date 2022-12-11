from mailing.models import Mailing, Message
import datetime


def generate_message_string() -> str:
    """
    Return new message, for send_email
    """
    mailings = Mailing.objects.filter(created_at__gt=datetime.date.today())
    str_message = ''
    for index, mailing in enumerate(mailings, start=1):
        msgs = Message.objects.filter(mailing_id_id=mailing.pk)
        if index == 1:
            str_message += f'\n{index} mailing: send {len(msgs)}\n'
        str_message += f'{index} mailing: send {len(msgs)} message\n'
    return f'Today we run {len(mailings)} mailing:' \
           f'{str_message}'
