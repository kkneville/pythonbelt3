from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name="home"),
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^showtrip$', views.showtrip, name="showtrip"),
    url(r'^add$', views.add, name="add"),
    url(r'^addtrip$', views.addtrip, name="addtrip"),
    url(r'^jointrip$', views.jointrip, name="jointrip"),
    url(r'^logout$', views.logout, name="logout"),
]
