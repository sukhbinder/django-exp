from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.


class Expense(models.Model):
    date = models.DateField(default=timezone.now)
    where = models.CharField(max_length=100)
    amount = models.FloatField(default=0.0)
    tags = models.CharField(max_length=500)
    how = models.CharField(max_length=100, default="")

    def __str__(self):
        return "{}-{} {} {}".format(self.date, self.amount, self.where, self.tags, self.how)

    def get_absolute_url(self):
        return reverse('update-view', args=[str(self.id)])

    def get_where_url(self):
        return reverse('where-view', args=[str(self.where)])

    def get_month_year_url(self):
        return reverse('year-month', args=[str(self.date.year), str(self.date.month)])
