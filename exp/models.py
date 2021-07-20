from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class WhereCategory(models.Model):
    name = models.CharField(max_length=100, default="LOCALSHOP", unique=True)

    def __str__(self):
        return self.name
    
    def __lt__(self, other):
        return self.__str__() < other.__str__()
    
class HowCategory(models.Model):
    name = models.CharField(max_length=100, default="CASH", unique=True)

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.__str__() < other.__str__()

class Expense(models.Model):
    date = models.DateField(default=timezone.now)
    # where = models.CharField(max_length=100)
    where = models.ForeignKey(WhereCategory, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    tags = models.CharField(max_length=500)
    # how = models.CharField(max_length=100, default="")
    how = models.ForeignKey(HowCategory, on_delete=models.CASCADE, related_name="how")

    def __str__(self):
        return "{}-{} {} {}".format(self.date, self.amount, self.where, self.tags, self.how)

    def get_absolute_url(self):
        return reverse('update-view', args=[str(self.id)])

    def get_where_url(self):
        return reverse('where-view', args=[str(self.where)])

    def get_month_year_url(self):
        return reverse('year-month', args=[str(self.date.year), str(self.date.month)])

    def get_month_year_export_url(self):
        return reverse("ym-export-view", args=[str(self.date.year), str(self.date.month)])
    
    def get_month_year_dash_url(self):
        return reverse("ym-dash-view", args=[str(self.date.year), str(self.date.month)])
