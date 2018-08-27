from django.contrib import admin
from django.urls import path
from billing import views
from rest_framework.urlpatterns import format_suffix_patterns

# IDEA: maybe create a get calls by id and by number in the path

urlpatterns = [
    path('calls/', views.get_post_calls.as_view(), name='get_post_calls'),
    path('incomplete_calls/', views.get_incomplete_calls.as_view(),
         name='get_incomplete_calls'),
    path('bills/<int:year>/<int:month>/',
         views.get_bills.as_view(), name='get_bills')
]

urlpatterns = format_suffix_patterns(urlpatterns)
