from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about.html', views.about, name="about"),
    path('add_stock.html', views.add_stock, name="add_stock"),
    path('delete/<stock_id>', views.delete, name="delete"),
    path('delete_stock.htm>', views.delete_stock, name="delete_stock"),
    path('stock_info/<ticker>', views.stock_info, name="stock_info"),
    path('chart.html', views.chart, name="chart"),




]
