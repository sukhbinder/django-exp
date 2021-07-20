from django.contrib import admin

# Register your models here.
from exp.models import Expense, HowCategory,WhereCategory

admin.site.register(Expense)
admin.site.register(HowCategory)
admin.site.register(WhereCategory)
