from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import index

urlpatterns = [
    url(r'^$', index.index),
    url(r'^v2rayHas$', index.v2rayHas),
    url(r'^updateUUID$', index.updateUUID),
    url(r'^updateConfig$', index.updateConfig),
    url(r'^updateShadowsocks$', index.updateShadowsocks)
]
