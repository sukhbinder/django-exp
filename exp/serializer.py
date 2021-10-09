from rest_framework import serializers
from exp.models import Expense, WhereCategory, HowCategory


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class WhereCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WhereCategory
        fields = '__all__'

class HowCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HowCategory
        fields = '__all__'