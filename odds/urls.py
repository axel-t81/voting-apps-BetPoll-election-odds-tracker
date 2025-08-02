from django.urls import path
from . import views

app_name = 'odds'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('odds/', views.OddsListView.as_view(), name='odds_list'),
    path('api/chart-data/', views.chart_data, name='chart_data'),
]