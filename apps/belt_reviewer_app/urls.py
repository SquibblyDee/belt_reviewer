from django.conf.urls import url
from . import views

urlpatterns = [
    # root goes to the index
    url(r'^$', views.loginandreg),
    url(r'^process_register$', views.process_register),
    url(r'^process_login$', views.process_login),
    url(r'^books$', views.books),
    url(r'^books/add$', views.addbook),
    url(r'^books/processbook$', views.processbook),
    url(r'^books/process_review$', views.process_review),
    url(r'^books/(?P<num>\d+)$', views.showbook),
    url(r'^delete/(?P<num>\d+)$', views.delete),
    url(r'^users/(?P<num>\d+)$', views.users),
    url(r'^logout$', views.logout),
]
