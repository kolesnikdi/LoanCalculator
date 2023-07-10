from django.db import models


class TimePeriod(models.IntegerChoices):
    """types of time intervals"""
    DAY = 1
    WEEK = 2
    MONTH = 3
