from django.contrib import admin
from django.urls import path
from billing import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('get_post_calls/', views.get_post_calls.as_view(), name='get_post_calls'),
    #path('snippets/<int:pk>/', views.SnippetDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
