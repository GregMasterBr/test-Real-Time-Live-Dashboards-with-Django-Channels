from django.urls import path
from  . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<slug>', views.dashboard, name='dashboard'),
    path('<slug>/chart/', views.chart_data, name='chart_data'),

]