from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^game$', views.game, name='game'),
    url(r'^move$', views.move, name='move'),
    url(r'^acquire$', views.acquire, name='acquire'),
    url(r'^damage$', views.damage, name='damage'),
    url(r'^eat$', views.eat, name='eat'),
    url(r'^put$', views.put, name='put'),
    url(r'^use$', views.use, name='use'),
    url(r'^quit$', views.quit, name='quit'),
    url(r'^merge$', views.merge, name='merge'),
    url(r'^refresh$', views.refresh, name='refresh'),
    url(r'^tutorial$', views.tutorial, name='tutorial'),
]