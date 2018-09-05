from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
	url(r"^$", views.redirect_to_default_search, name="redirect_to_default_search"),
	url(r"^activities/$", views.search_activities, name="search_activities"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
