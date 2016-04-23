"""recharge_panel_templates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from recharge_panel_app.views import views, create_campaign, create_user, dashboard

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',dashboard.index, name='dashboard.index'),
    url(r'^dashboard/$', dashboard.index, name='dashboard.index'),
    url(r'^logout/$', views.logout, name='view.logout'),
    # url(r'^get_recharge_counts/$', dashboard.get_recharge_counts, name='dashboard.get_recharge_counts'),
    url(r'^create_recharge_mobile/$', create_campaign.create_recharge_mobile, name='create_campaign.create_recharge_mobile'),
    url(r'^campaign/create_recharge_mobile/$', create_campaign.create_recharge_mobile, name='create_campaign.create_recharge_mobile'),
    url(r'^add_user$', create_user.add_user, name='create_user.add_user')

]
