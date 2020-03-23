from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^client_score/$', views.ClientScoreViewSet.as_view(), name='client_score'),
]