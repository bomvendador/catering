# -*- coding: utf-8 -*-
"""catering URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from main import views as main_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main_view.index_view, name='index'),

    url(r'^lunches_index/$', main_view.lunches_index, name='lunches_index'),

    url(r'^standart_menu/$', main_view.standart_menu, name='standart_menu'),
    url(r'^standart_menu/(?P<menu_date_raw>.*)$', main_view.standart_menu_by_date, name='standart_menu_by_date'),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),

    url(r'^add_to_cart/$', main_view.add_to_cart, name='add_to_cart'),
    url(r'^check_cart/$', main_view.check_cart, name='check_cart'),
    url(r'^del_from_minicart/$', main_view.del_from_minicart, name='del_from_minicart'),

    url(r'^cart_for_checkout/(?P<cart_id>\d+)/$', main_view.cart_for_checkout, name='cart_for_checkout'),

    url(r'^to_checkout/$', main_view.to_checkout, name='to_checkout'),
    url(r'^checkout/(?P<cart_id>\d+)/$', main_view.checkout, name='checkout'),

    url(r'^save_order/$', main_view.save_order, name='save_order'),

    url(r'^product_details/(?P<meal_id>\d+)/$', main_view.product_details, name='product_details'),
    url(r'^product_details_complex/(?P<meal_id>\d+)/$', main_view.product_details_complex, name='product_details_complex'),

    url(r'^complex_standart_menu/$', main_view.complex_standart_menu, name='complex_standart_menu'),
    url(r'^complex_standart_menu_by_date/(?P<menu_date>.*)/$', main_view.complex_standart_menu_by_date, name='complex_standart_menu_by_date'),
    url(r'^complex_menu_details/(?P<menu_id>.*)/$', main_view.complex_menu_details, name='complex_menu_details'),

    url(r'^catering_index/$', main_view.catering_index_page, name='catering_index'),
    url(r'^place/(?P<place_id>\d+)/$', main_view.place_details, name='place_details'),
    url(r'^places_list_by_tag/(?P<tag_id>\d+)/$', main_view.places_list_main_by_tag, name='places_list_main_by_tag'),
    url(r'^place_client_request/$', main_view.place_client_request, name='place_client_request'),
    url(r'^places_list/$', main_view.places_list_main, name='places_list_main'),
    url(r'^get_place_tags/$', main_view.get_place_tags, name='get_place_tags'),

    url(r'^gallery_portfolio/$', main_view.gallery_portfolio, name='gallery_portfolio'),

    # events
    url(r'^events_index/$', main_view.events_index, name='events_index'),

    # contacts
    url(r'^contacts/$', main_view.contacts, name='contacts'),


]
