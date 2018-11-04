from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.record, name='record'),
    url(r'^recorded$', views.index, name='index'),
    url(r'^analyze_text', views.analyze, name='analysis'),
    url(r'^curr_record', views.currently_recording, name='recording_now')
]
