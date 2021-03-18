"""expense URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from exp import views

urlpatterns = [
    path('', views.ExpenseListView.as_view(), name="index"),
    path('dashboard', views.ExpenseAggView.as_view(), name="dashboard"),
    path('exp/<int:pk>/', views.ExpenseDetailView.as_view(), name="detail-view"),
    path('add/', views.ExpenseCreateView.as_view(), name="create-view"),
    path('exp/<int:pk>/update', views.ExpenseUpdateView.as_view(), name="update-view"),
    path('exp/<str:where>', views.ExpenseWhereView.as_view(), name="where-view"),
    path('export', views.export_view, name="export-view"),
    path('how', views.ExpenseHowView.as_view(), name="how"),
    path('exp/<int:year>/<int:month>',
         views.YearMonthView.as_view(), name="year-month"),
    path('exp/<int:year>/<int:month>/export',
         views.export_view, name="ym-export-view"),
    path('exp/<int:year>/<int:month>/dashboard',
         views.YearMonthExpenseAggView.as_view(), name="ym-dash-view"),
    path('api/expenses/', views.ExpenseAPIView.as_view()),

]
