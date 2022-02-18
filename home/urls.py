from django.contrib import admin
from django.urls import path,register_converter
from django.urls import include
from . import views
import datetime
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home',views.signup,name='signup'),
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('handleSignup/',views.handleSignup,name='handleSignup'),
    path('handlelogin/',views.handlelogin,name='handlelogin'),
    path('handlelogout/',views.handlelogout,name='handleLogout'),
    path('addmoney/',views.addmoney,name='addmoney'),
    path('addmoney_submission/',views.addmoney_submission,name='addmoney_submission'),
    path('expense_edit/<int:id>',views.expense_edit,name='expense_edit'),
    path('<int:id>/addmoney_update/', views.addmoney_update, name="addmoney_update") ,
    path('expense_category_sumary/',views.expense_category_sumary, name = 'expense_category_sumary'),
    path('income_category_sumary/',views.income_category_sumary, name = 'income_category_sumary'),
    path('<int:id>/profile_edit/',views.profile_edit,name="profile_edit"),
    path('expense_category_weekly/',views.expense_category_weekly, name = 'expense_category_date'),
    path('income_category_weekly/',views.income_category_weekly, name = 'income_category_date'),
    path('expense_category_month/',views.expense_category_month, name = 'expense_category_date'),
    path('income_category_month/',views.income_category_month, name = 'income_category_date'),
    path('expense_category_half_year/',views.expense_category_half_year, name = 'expense_category_date'),
    path('income_category_half_year/',views.income_category_half_year, name = 'income_category_date'),
    path('expense_category_year/',views.expense_category_year, name = 'expense_category_date'),
    path('income_category_year/',views.income_category_year, name = 'income_category_date'),
    path('<int:id>/profile_update/',views.profile_update,name="profile_update"),
    path('expense_delete/<int:id>',views.expense_delete,name='expense_delete'),
    path('profile/',views.profile,name='profile'),
    path('export_csv/',views.export_csv,name='export_csv'),
    path('date_stats/',views.date_stats,name='date_stats'),
    path('month_stats/',views.month_stats,name='month_stats'),
    path('half_year_stats/',views.half_year_stats,name='half_year_stats'),
    path('year_stats/',views.year_stats,name='year_stats'),
    path('stats/',views.stats_view,name='stats'),
    path('reports/',views.reports,name='reports'),
    path('search/',views.search,name='search'),
    
]
