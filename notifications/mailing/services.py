from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils import timezone
from datetime import timedelta


def create_periodical_task():
    """
    Create new periodical task if not exist, on send mail every day.
    Start time = time.now + 1 minute
    """
    task_name = 'send_mail_every_day'
    if PeriodicTask.objects.filter(
            task__exact=f'client.tasks.{task_name}'
    ).exists():
        return
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name='Send mail stats',
        task=f'client.tasks.{task_name}',
        start_time=timezone.now() + timedelta(minutes=1),
        last_run_at=timezone.now() - timedelta(days=1)
    )
