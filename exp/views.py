from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView

from django.db.models import Sum

from exp.generate_plots import generate_plots_with_data, generate_plot
from exp.models import Expense, HowCategory, WhereCategory

from exp.serializer import ExpenseSerializer, WhereCategorySerializer, HowCategorySerializer

import csv
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, filters


def get_plot_data(year=None, month=None):
    if year is None and month is None:
        alldata = Expense.objects.all().order_by("-date")
    else:
        alldata = Expense.objects.filter(
            date__year=year, date__month=month).order_by('-date')
    df = generate_plots_with_data(alldata)
    dd = generate_plot(df)
    return dd


class HowCategoryCreateView(CreateView):
    model = HowCategory
    fields = "__all__"
    success_url = "/"


class WhereCategoryCreateView(CreateView):
    model = WhereCategory
    fields = "__all__"
    success_url = "/"


class ExpenseAPIView(generics.ListCreateAPIView):
    search_fields = ["where", "amount", "tags", "how"]
    filter_backends = (filters.SearchFilter,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class WhereCategoryAPIView(generics.ListCreateAPIView):
    queryset = WhereCategory.objects.all()
    serializer_class = WhereCategorySerializer


class HowCategoryAPIView(generics.ListCreateAPIView):
    queryset = HowCategory.objects.all()
    serializer_class = HowCategorySerializer

class ExpenseAPIUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class ExpenseListView(ListView):
    model = Expense
    template_name = "exp/index.html"
    ordering = ['-date']
    # paginate_by = 60


class ExpenseAggView(ListView):
    model = Expense
    template_name = "exp/agg.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["aggdata"] = Expense.objects.values("where").annotate(
            total_amount=Sum('amount')).order_by('-total_amount')
        context["imgdata"] = get_plot_data()
        return context


class YearMonthExpenseAggView(ListView):
    model = Expense
    template_name = "exp/agg.html"

    def get_context_data(self, **kwargs):
        year = self.kwargs['year']
        month = self.kwargs['month']
        context = super().get_context_data(**kwargs)
        context["aggdata"] = Expense.objects.values("where").annotate(
            total_amount=Sum('amount')).order_by('-total_amount')
        context["imgdata"] = get_plot_data(year, month)
        return context


class YearMonthView(ListView):
    model = Expense
    template_name = "exp/yearmonthindex.html"

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Expense.objects.filter(date__year=year,
                                      date__month=month).order_by('-date')


class ExpenseHowView(ListView):
    model = Expense
    template_name = "exp/how.html"

    def get_queryset(self):
        return Expense.objects.values("how").annotate(total_amount=Sum('amount')).order_by('-total_amount')


class ExpenseWhereView(ListView):
    model = Expense
    template_name = "exp/where.html"

    def get_queryset(self):
        where = self.kwargs['where']
        return Expense.objects.filter(where__name__iexact=where).order_by('-date')


class ExpenseDetailView(DetailView):
    model = Expense
    template_name = "exp/detail_view.html"


class ExpenseCreateView(CreateView):
    model = Expense
    fields = "__all__"
    success_url = "/"


class ExpenseUpdateView(UpdateView):
    model = Expense
    template_name = "exp/update_form.html"

    fields = "__all__"

    success_url = "/"


def export_view(request, year=None, month=None):
    if year is None and month is None:
        data = Expense.objects.all().order_by('date')
        filename = "expense_export.csv"
    else:
        data = Expense.objects.filter(
            date__year=year, date__month=month).order_by('date')
        filename = "expense_export_{}_{}.csv".format(year, month)

    return export_view_internal(data, filename)


def export_view_internal(data, filename="expense_export.csv"):

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        filename)
    writer = csv.writer(response)
    writer.writerow(['DATE', 'WHERE', 'AMOUNT', 'TAGS', 'HOW'])
    for row in data:
        writer.writerow([row.date, row.where, row.amount,  row.tags, row.how])
    return response


def json_where(request):
    return JsonResponse(list(set([exp1.where for exp1 in Expense.objects.all()])), safe=False)
