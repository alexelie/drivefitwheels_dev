from django.conf.urls import url
from drivefitwheelsapp.views import AddSetup
from drivefitwheelsapp.views import Search
from drivefitwheelsapp.views import Succeed
from . import views
from drivefitwheelsapp.views import Home

urlpatterns = [
    url(r'^$', Home.as_view()),
	url(r'^addSetup/$', AddSetup.as_view()),
	url(r'^search/$', Search.as_view()),
	url(r'^succeed/$', Home.as_view(),{'succeed':'Thank you for your support. We will validate your setup and put it online shortly.'}),
] 
