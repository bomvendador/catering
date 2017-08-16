# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from dashboard import views
from main import views as main_views

app_name = 'dashboard'

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', views.index_view, name='index_view'),
    url(r'^$', views.login_view, name='login_view'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    # url(r'^$', views.index_view, name='index_view'),

    url(r'^menu_standart/$', views.standart_menu, name='menu_standart'),
    url(r'^get_menu_items/$', views.get_menu_items, name='get_menu_items'),
    url(r'^meals_menu/$', views.meals_menu, name='meals_menu'),

    url(r'^add_new_meal/$', views.add_new_meal, name='add_new_meal'),
    url(r'^meal_details/(?P<meal_id>.*)/$', views.meal_details, name='meal_details'),

    url(r'^add_new_meal_by_date/$', views.add_new_meal_by_date, name='add_new_meal_by_date'),
    url(r'^standart_menu_by_date/(?P<date>.*)/$', views.standart_menu_by_date, name='standart_menu_by_date'),
    url(r'^del_meal_by_date/$', views.del_meal_by_date, name='del_meal_by_date'),

    url(r'^ingredients/$', views.ingredients, name='ingredients'),
    url(r'^del_ingredient/$', views.del_ingredient, name='del_ingredient'),

    url(r'^active_dates/$', views.active_dates, name='active_dates'),

# заказы
    url(r'^orders/$', views.orders, name='orders'),
    url(r'^orders_total_info/$', views.orders_total_info, name='orders_total_info'),
    url(r'^change_order_status/$', views.change_order_status, name='change_order_status'),
    url(r'^order/(?P<order_id>\d+)/$', views.order, name='order'),
    url(r'^order_to_pdf/(?P<order_id>\d+)/$', views.order_to_pdf, name='order_to_pdf'),

# комплексное меню
    url(r'^add_complex_menu/(?P<data>.*)/$', views.add_complex_menu, name='add_complex_menu'),
    url(r'^complex_menu_details/(?P<menu_id>.*)/$', views.complex_menu_details, name='add_complex_menu_details'),
    url(r'^complex_menu/(?P<menu_type_get>.*)/$', views.complex_menu, name='complex_menu'),
    url(r'^complex_menu_by_date/(?P<menu_date>.*)/$', views.complex_menu_by_date, name='complex_menu_by_date'),
    url(r'^save_complex_menu/$', views.save_complex_menu, name='save_complex_menu'),
    url(r'^del_meal_from_complex_menu/$', views.del_meal_from_complex_menu, name='del_meal_from_complex_menu'),
    url(r'^del_image_from_complex_menu/$', views.del_image_from_complex_menu, name='del_image_from_complex_menu'),
    url(r'^del_complex_menu/$', views.del_complex_menu, name='del_complex_menu'),

# иконки
    url(r'^icons/$', views.icons, name='icons'),

# кейтеринг
    url(r'^places_list/$', views.places_list, name='places_list'),
    url(r'^add_place/$', views.add_place, name='add_place'),
    url(r'^delete_image_from_gallery/$', views.delete_image_from_gallery, name='delete_image_from_gallery'),
    url(r'^delete_place/$', views.delete_place, name='delete_place'),
    url(r'^place_details/(?P<place_id>\d+)/$', views.place_details, name='place_details'),
    url(r'^client_requests/$', views.client_requests, name='client_requests'),
    url(r'^new_client_requests/$', views.new_client_requests, name='new_client_requests'),
    url(r'^client_request_details/(?P<request_id>\d+)/$', views.client_request_details, name='client_request_details'),

# теги
    url(r'^tags_list/$', views.tags_list, name='tags_list'),
    url(r'^add_tag/$', views.add_tag, name='add_tag'),
    url(r'^del_tag/$', views.del_tag, name='del_tag'),
    url(r'^edit_tag/$', views.edit_tag, name='edit_tag'),

# отзывы
    url(r'^testimonials_list/$', views.testimonials_list, name='testimonials_list'),
    url(r'^save_testimonial/$', views.save_testimonial, name='save_testimonial'),
    url(r'^testimonial_details/(?P<test_id>\d+)/$', views.testimonial_details, name='testimonial_details'),

# цитаты
    url(r'^quotes_list/$', views.quotes_list, name='quotes_list'),
    url(r'^add_quote/$', views.add_quote, name='add_quote'),
    url(r'^quote_details/(?P<quote_id>\d+)/$', views.quote_details, name='quote_details'),

# портфолио
    url(r'^portfolio_items_list/$', views.portfolio_list, name='portfolio_list'),
    url(r'^add_portfolio_item/$', views.add_portfolio_item, name='add_portfolio_item'),
    url(r'^delete_portfolio_item/$', views.delete_portfolio_item, name='delete_portfolio_item'),
    url(r'^portfolio_item_details/(?P<item_id>\d+)/$', views.portfolio_item_details, name='portfolio_item_details'),
    url(r'^delete_image_from_gallery_portfolio/$', views.delete_image_from_gallery_portfolio, name='delete_image_from_gallery_portfolio'),

# персонал
    url(r'^staff_list/$', views.staff_list, name='staff_list'),
    url(r'^add_staff/$', views.add_staff, name='add_staff'),
    url(r'^staff_details/(?P<staff_id>\d+)/$', views.staff_details, name='staff_details'),
    url(r'^del_image_from_staff/$', views.delete_image_from_staff, name='delete_image_from_staff'),
    url(r'^del_staff/$', views.delete_staff, name='delete_staff'),

# контактное лицо
    url(r'^add_contact_person/$', views.add_contact_person, name='add_contact_person'),
    url(r'^contact_person_details/$', views.contact_person_details, name='contact_person_details'),


]