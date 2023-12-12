from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

MIN_USER_AGE = 9
FORBIDDEN_DOMEN = ["rambler.ru"]

def check_birth_date(value):
    # Эта запись вычисляет разницу между сегодняшней датой и value(date(Г, М, Д))
    diff = relativedelta(date.today(), value).years
    if diff < MIN_USER_AGE:
        raise ValidationError(f"User with age {diff} is too young!")


def check_email_address(value):
    mail_domen = value.split("@")[-1]
    if mail_domen in FORBIDDEN_DOMEN:
        raise ValidationError(f"{mail_domen} is too forbidden!")
