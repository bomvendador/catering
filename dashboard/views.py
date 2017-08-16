# -*- coding: utf-8 -*-

import json

import base64
import os, re
from django.shortcuts import render, redirect, HttpResponse, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from main.models import UserProfile, User, Meal, MenuType, Role, MealImage, MealType, MealByDate, Ingredients, IngredientsForMeal, ActiveDates, Order, OrderStatus, CartMeals, CartType, Cart, ComplexMenu, ComplexMenuByDate, MealForComplexMenu, Icon, Place, PlaceGreyOption, PlaceImage, PlaceOption, InfrastructureItem, ClientRequest, Tag, TagPlace, Testimonial, Quote, PortfolioItem, PortfolioItemImage, Staff, PlaceContactPerson, UserEmail, PhoneNumber, UserPaymentDetails

from main import views as main_view

from datetime import date, timedelta

from decimal import Decimal
from django.core.files.base import ContentFile
from io import StringIO, BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_xhtml2pdf.utils import generate_pdf, generate_pdf_template_object
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.utils.html import escape

from django.contrib.staticfiles.templatetags.staticfiles import static
# Create your views here.

from catering import settings
# @login_required(redirect_field_name=None, login_url='/dashboard/login')
# def add_watermark(image, watermark):
#     rgba_image = image.con


from PIL import Image, ImageEnhance

import PIL

from django.core.files.images import get_image_dimensions

sliders = [u'Блюда на странице кейтеринга', u'Главная страница']


def add_watermark(image, watermark, opacity=1, wm_interval=0):
    assert 0 <= opacity <= 1
    image_size = get_image_dimensions(image)
    watermark_size = get_image_dimensions(watermark)
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    layer = Image.new('RGBA', image_size, (0, 0, 0, 0))
    for y in range(0, image_size[1], watermark.size[1] + wm_interval):
        for x in range(0, image.size[0], watermark_size[0] + wm_interval):
            layer.paste(watermark, (x, y))
    return Image.composite(layer, image, layer)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def info(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
        'user': request.user,
        'standart': 'standart',
        'business': 'business',
        'new_requests': ClientRequest.objects.filter(status__name=u'Новый').count()
    }
    return context


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def index_view(request, user_id):
    context = info(request)
    # if req
    context.update({
        'user_id': user_id,
    })
    return render(request, 'base_dashboard.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def logout_view(request):
    context = info(request)
    user = request.user
    logout(request)
    return render(request, 'sign_in_board.html')


def login_view(request):
    if request.user.is_authenticated():
        # print('not logged')
        return redirect('dashboard:index_view', user_id=request.user.id)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # logger.debug(email + password)
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                # print('logged')
                login(request, user)
                user_profile = UserProfile.objects.get(user=user)
                # if user_profile.role.name == u'Клиент':
                    # client = Client.objects.get(user=user)
                    # client.visited_times += 1
                    # client.save()
                # logger.debug('id = ' + str(user.id))
                # return redirect('ru:dashboard_ru:base_board', user_id=user.id)
                return HttpResponse(user.id)
        else:
            return HttpResponse('error')

    return render(request, 'sign_in_board.html')


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def standart_menu(request):
    context = info(request)
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        menu_date_raw = json_data['menu_date']
        menu_date_split = menu_date_raw.split('.')
        menu_date = menu_date_split[2] + '-' + menu_date_split[1] + '-' + menu_date_split[0]
        meals = MealByDate.objects.filter(date=menu_date)
        if meals:
            response = menu_date
        else:
            response = 'no'
        return HttpResponse(response)
    first_meals = Meal.objects.filter(meal_type=MealType.objects.get(name=u'Первые блюда'))
    second_meals = Meal.objects.filter(meal_type=MealType.objects.get(name=u'Вторые блюда'))
    salads = Meal.objects.filter(meal_type=MealType.objects.get(name=u'Салаты'))
    drinks = Meal.objects.filter(meal_type=MealType.objects.get(name=u'Напитки'))

    context.update({
        'first_meals': first_meals,
        'second_meals': second_meals,
        'salads': salads,
        'drinks': drinks,
        'active_dates': ActiveDates.objects.all()
    })
    return render(request, 'standart_menu_d.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def get_meals_list(request):
    context = info(request)
    first_meals = Meal.objects.filter(meal_type=MealType.objects.get(name=u'Первые блюда'))
    second_meals = Meal.objects.filter(meal_type=MealType.objects.get(name=u'Вторые блюда'))
    salads = Meal.objects.filter(meal_type=MealType.objects.get(name=u'Салаты'))
    drinks = Meal.objects.filter(meal_type=MealType.objects.get(name=u'Напитки'))
    context.update({
            'first_meals': first_meals,
            'second_meals': second_meals,
            'salads': salads,
            'drinks': drinks
           })
    return context


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def standart_menu_by_date(request, date):
    context = info(request)
    context.update(get_meals_list(request))
    menu_date_split = date.split('-')
    menu_date = menu_date_split[2] + '.' + menu_date_split[1] + '.' + menu_date_split[0]

    meals = MealByDate.objects.filter(date=date)
    # for m in meals:
    #     for mm in MealImage.objects.filter(meal=m.meal):
    #         print(mm.image_350_350)
    context.update({
        'meals': meals,
        'date': menu_date,
        'active_dates': ActiveDates.objects.all(),


    })
    return render(request, 'standart_menu_d.html', context)


# меню
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def get_menu_items(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        menu_date_raw = json_data['menu_date']
        menu_type = json_data['menu_type']
        menu_date_split = menu_date_raw.split('.')
        menu_date = menu_date_split[2] + '-' + menu_date_split[1] + '-' + menu_date_split[0]
        if menu_type == 'standart':
            print('standart')
            try:
                menu_items = MenuStandart.objects.filter(date=menu_date)
            except MenuStandart.DoesNotExist:
                menu_items = None
            if menu_items:
                return render(request, 'standart_menu_d.html', {'menu_items': menu_items})

        print(menu_date)
        return HttpResponse(json.dumps({'response': 'no_data'}))


# список всех блюд
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def meals_menu(request):
    context = info(request)
    meals = Meal.objects.all()
    context.update({
        'meals': meals
    })
    return render(request, 'meals.html', context)


#детали блюда
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def meal_details(request, meal_id):
    context = info(request)
    meal = Meal.objects.get(id=meal_id)
    meal_imgs = MealImage.objects.filter(meal=meal)
    for img in meal_imgs:
        if img.image_70_70:
            image_70 = str(img.image_70_70).split('/')[-1:][0]
        if img.image_350_350:
            image_350 = img.image_350_350
    print(IngredientsForMeal.objects.filter(meal=meal).count())
    context.update({'meal': meal,
                    'meal_types': MealType.objects.all(),
                    'image_70': image_70,
                    'image_350': image_350,
                    'ingredients': Ingredients.objects.all().exclude(name__in=IngredientsForMeal.objects.filter(
                        meal=meal)),
                    'edit': 1,
                    'meal_ingredients': IngredientsForMeal.objects.filter(meal=meal)

                    })
    return render(request, 'add_new_meal.html', context)


# добавление нового блюда
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def add_new_meal(request):
    context = info(request)
    if request.method == 'POST':
        data = request.POST
        print(data)
        meal_name = data['meal_name']
        meal_description = data['meal_description']
        meal_short_description = data['meal_short_description']
        meal_price = data['meal_price']
        meal_type = data['meal_type']
        meal_weight = data['meal_weight']
        meal = Meal()

        meal.name = meal_name
        meal.description = meal_description
        meal.short_description = meal_short_description
        meal.price = meal_price
        meal.meal_type = MealType.objects.get(name=meal_type)
        meal.weight = meal_weight
        meal.save()

        # meal_image = MealImage()
        for k in request.POST.keys():
            if 'ingredient' in k:
                ingredient = request.POST.get(k).strip()
                print('ing_name = ' + str(ingredient))
                ingredient_for_meal = IngredientsForMeal()
                ingredient_for_meal.meal = meal
                ingredient_for_meal.ingredient = Ingredients.objects.get(name=ingredient)
                ingredient_for_meal.save()

        for k in request.FILES.keys():
            # print('key = ' + str(k))
            if k != 'meal_foto':
                for file in request.FILES.getlist(k):
                    meal_image = MealImage()
                    meal_image.image_350_350 = file
                    meal_image.meal = meal
                    meal_image.save()
                    db_file_name = meal_image.image_350_350
                    db_file_name_split = str(db_file_name).split('/')
                    final_file_name = db_file_name_split[db_file_name_split.__len__() - 1]
                    meal_image.image_name = final_file_name
                    meal_image.save()
                    # meal_image.image_350_350.file

                    # new_file_name = update_filename(s, f.name)
                    # logger.debug(str(new_file_name))

                    # s = SentFiles(file=f, sent_doc=doc_sent, file_name=unicodedata.normalize('NFKD', f.name).encode('utf-8', 'ignore'))
                    # s.save()
        files = request.FILES.getlist('meal_foto')

        if files:
            for file in files:
                meal_image = MealImage()
                meal_image.image_70_70 = file
                meal_image.meal = meal
                meal_image.save()
                db_file_name = meal_image.image_70_70
                db_file_name_split = str(db_file_name).split('/')
                final_file_name = db_file_name_split[db_file_name_split.__len__() - 1]
                meal.image_name = final_file_name
                meal.save()

    user_profile = UserProfile.objects.get(user=request.user)

    context.update({
        'user_profile': user_profile,
        'meal_types': MealType.objects.all(),
        'ingredients': Ingredients.objects.all()
    })
    return render(request, 'add_new_meal.html', context)


# добавление нового блюда на дату
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def add_new_meal_by_date(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        menu_date_raw = json_data['menu_date']
        print(menu_date_raw)
        menu_type = json_data['menu_type']
        menu_level = json_data['menu_level']
        meal_id_raw = json_data['meal_id']
        meal_id_split = meal_id_raw.split('_')
        meal_id = meal_id_split[1]
        meal = Meal.objects.get(id=meal_id)
        # menu_date_split = menu_date_raw.split('.')
        menu_date = main_view.convert_date_to_db(menu_date_raw)
        if menu_type == 'standart' and menu_level == 'single':
            meal_by_date = MealByDate()
            meal_by_date.meal = meal
            meal_by_date.date = menu_date
            meal_by_date.save()
            return HttpResponse('ok')
        if menu_type == 'standart' and menu_level == 'complex':
            response = json.dumps({
                'meal_name': meal.name,
                'meal_price': str(meal.price),
                'meal_weight': meal.weight,
                'meal_id': meal.id,
                'meal_image': meal.image_name,

            })
            return HttpResponse(response)

    return HttpResponse()


# удаление блюда из меню для даты
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def del_meal_by_date(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        meal_id = json_data['meal_id']
        try:
            meal = MealByDate.objects.get(id=meal_id)
        except MealByDate.DoesNotExist:
            meal = None
        if meal:
            meal.delete()
            response = meal_id
        else:
            response = 'error'
        return HttpResponse(response)


# добавление, получение, изменение ингредиентов
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def ingredients(request):
    context = info(request)
    if request.method == 'POST':
        ingr_name = request.POST.get('ingredient_name')
        ingr_icon = request.POST.get('ingredient_icon')
        ingr_id = request.POST.get('ingredient_id')
        print('id = ' + str(ingr_id))
        if ingr_id:
            ingr = Ingredients.objects.get(id=ingr_id)
        else:
            ingr = Ingredients()
        ingr.name = ingr_name
        ingr.icon = ingr_icon
        ingr.save()
        return HttpResponse('ok')
    ingreds = Ingredients.objects.all()
    context.update({
        'ingredients': ingreds
    })
    return render(request, 'ingredients.html', context)


# добавление, получение, изменение ингредиентов
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def del_ingredient(request):
    if request.method == 'POST':
        ingr_id = request.POST.get('ingr_id')
        ingr = Ingredients.objects.get(id=ingr_id)
        ingr.delete()
        return HttpResponse()


# активные даты
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def active_dates(request):
    context = info(request)
    if request.method == 'POST':
        data_post = request.POST
        if data_post.get('operation') == 'date_status':
            print(request.POST)

            for k in data_post.keys():
                print(k)
                if 'dates' in k:
                    data = request.POST.get(k)
                    data_split = data.split('_')
                    date_id = data_split[0]
                    date_status = data_split[1]
                    date_to_change = ActiveDates.objects.get(id=date_id)
                    if date_status == 'true':
                        date_to_change.active = True
                    else:
                        date_to_change.active = False
                    date_to_change.save()
            return HttpResponse(u'Изменение статуса')
        json_data = json.loads(request.body.decode('utf-8'))
        operation = json_data['operation']
        if operation == 'del':
            date_id = json_data['date_id']
            ActiveDates.objects.get(id=date_id).delete()
        if operation == 'add':
            dates = json_data['dates']
            dates_split = dates.split(',')
            start_date = main_view.convert_date_to_db(dates_split[0])
            finish_date = main_view.convert_date_to_db(dates_split[1])
            start_date_split = start_date.split('-')
            finish_date_split = finish_date.split('-')

            start_day = int(start_date_split[2])
            start_month = int(start_date_split[1])
            start_year = int(start_date_split[0])

            finish_day = int(finish_date_split[2])
            finish_month = int(finish_date_split[1])
            finish_year = int(finish_date_split[0])

            date_start = date(start_year, start_month, start_day)
            date_finish = date(finish_year, finish_month, finish_day)
            delta = date_finish - date_start
            for i in range(delta.days + 1):
                active_date = date_start + timedelta(days=i)
                if active_date.weekday() != 5 and active_date.weekday() != 6:
                    new_active_date = ActiveDates(date=active_date, active=False)
                    new_active_date.save()
            return HttpResponse(u'Добавление')

        return HttpResponse(u'Удаление')
    context.update({
        'dates': ActiveDates.objects.all()
    })
    return render(request, 'active_dates.html', context)


# заказы
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def orders(request):
    context = info(request)
    context.update({
        'orders': Order.objects.all().order_by('-added')
    })
    return render(request, 'orders.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def order(request, order_id):
    context = info(request)
    order_ = Order.objects.get(id=order_id)
    meals = CartMeals.objects.filter(cart=order_.cart)
    cart = Cart.objects.get(id=order_.cart_id)
    context.update({
        'order': order_,
        'meals': meals,
        'cart': cart,
        'order_status': OrderStatus.objects.all()
    })
    return render(request, 'order_details.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def orders_total_info(request):
    context = info(request)
    if request.method == 'POST':
        data_post = request.POST
        print(data_post)
    #     if data_post.get('operation') == 'date_status':
    #         print(request.POST)
    #
    #         for k in data_post.keys():
    #             print(k)
    #             if 'dates' in k:
    #                 data = request.POST.get(k)
    #                 data_split = data.split('_')
    #                 date_id = data_split[0]
    #                 date_status = data_split[1]
    #                 date_to_change = ActiveDates.objects.get(id=date_id)
    #                 if date_status == 'true':
    #                     date_to_change.active = True
    #                 else:
    #                     date_to_change.active = False
    #                 date_to_change.save()
    #         return HttpResponse(u'Изменение статуса')
    #     json_data = json.loads(request.body.decode('utf-8'))
    #     operation = json_data['operation']
    #     if operation == 'del':
    #         date_id = json_data['date_id']
    #         ActiveDates.objects.get(id=date_id).delete()
    #     if operation == 'add':
    #         dates = json_data['dates']
    #         dates_split = dates.split(',')
    #         start_date = main_view.convert_date_to_db(dates_split[0])
    #         finish_date = main_view.convert_date_to_db(dates_split[1])
    #         start_date_split = start_date.split('-')
    #         finish_date_split = finish_date.split('-')
    #
    #         start_day = int(start_date_split[2])
    #         start_month = int(start_date_split[1])
    #         start_year = int(start_date_split[0])
    #
    #         finish_day = int(finish_date_split[2])
    #         finish_month = int(finish_date_split[1])
    #         finish_year = int(finish_date_split[0])
    #
    #         date_start = date(start_year, start_month, start_day)
    #         date_finish = date(finish_year, finish_month, finish_day)
    #         delta = date_finish - date_start
    #         for i in range(delta.days + 1):
    #             active_date = date_start + timedelta(days=i)
    #             if active_date.weekday() != 5 and active_date.weekday() != 6:
    #                 new_active_date = ActiveDates(date=active_date, active=False)
    #                 new_active_date.save()
    #         return HttpResponse(u'Добавление')
    #
    #     return HttpResponse(u'Удаление')
    # context.update({
    #     'dates': ActiveDates.objects.all()
    # })
    return render(request, 'orders_total_info.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def change_order_status(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        order_id = json_data['order_id']
        status_name = json_data['status_name']
        print(status_name)
        order_ = Order.objects.get(id=order_id)
        order_.status = OrderStatus.objects.get(name=status_name)
        order_.save()
        return HttpResponse('ok')


def render_to_pdf(template_src, context_dict):

    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO()

    pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def order_to_pdf(request, order_id):

    order_ = Order.objects.get(id=order_id)
    cart = order_.cart
    cart_meals = CartMeals.objects.filter(cart=cart)
    resp = HttpResponse(content_type='application/pdf')
    for i in cart_meals:
        try:
            print(i.meal.name)
            name = i.meal.name.encode('utf-8')
        except:
            name = i.menu.name
    context = {
        'order': order_,
        'cart': cart,
        'cart_meals': u'ыквнапнл',
    }
    result = generate_pdf('order_pdf.html', file_object=resp, context=context)
    return result
    # return render_to_pdf(
    #         'order_pdf.html',
    #         {
    #             str('pagesize'): str('A4'),
    #             # 'order': order_,
    #             # 'cart': cart,
    #             # 'cart_meals': cart_meals,
    #         }
    #     )


# комплексное меню
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def complex_menu(request, menu_type_get):
    context = info(request)
    if menu_type_get == 'standart':
        menu_type = MenuType.objects.get(name=u'Стандартное')
    else:
        menu_type = MenuType.objects.get(name=u'Бизнес')

    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        menu_date_raw = json_data['menu_date']
        menu_type = menu_type_get
        menu_date = ComplexMenuByDate.objects.filter(date=main_view.convert_date_to_db(menu_date_raw))
        if menu_type == 'standart':
            menu_type = MenuType.objects.get(name=u'Стандартное')
        else:
            menu_type = MenuType.objects.get(name=u'Бизнес')

        if menu_date:
            response = menu_type_get + '_' + main_view.convert_date_to_db(menu_date_raw)
        else:
            response = 'no'
        return HttpResponse(response)
    active_dates = ActiveDates.objects.filter(date__gte=date.today() + timedelta(days=1)).order_by('date')
    context.update({
        # 'menus': ComplexMenu.objects.all(),
        'active_dates': active_dates,
        'menu_type': menu_type,
        # 'standart': 'standart',
        # 'business': 'business',
        'cur_type': menu_type_get
    })
    return render(request, 'complex_menu_d.html', context)


# комплексное меню на дату
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def complex_menu_by_date(request, menu_date):
    context = info(request)
    menu_date_split = menu_date.split('_')
    menu_type = menu_date_split[0]
    menu_date = menu_date_split[1]
    print(menu_type)
    if menu_type == 'standart':
        menu_type_ = MenuType.objects.get(name=u'Стандартное')

    menus = ComplexMenuByDate.objects.filter(date=menu_date, menu_type=menu_type_)
    active_dates = ActiveDates.objects.filter(date__gte=date.today() + timedelta(days=1)).order_by('date')
    context.update({
        'active_dates': active_dates,
        'menus': menus,
        'date': main_view.convert_date_from_db(menu_date),
        'menu_type': menu_type_,
        'cur_type': menu_type
    })

    if menu_date:
        return render(request, 'complex_menu_d.html', context)


# комплексное меню на дату
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def add_complex_menu(request, data):
    context = info(request)
    context.update(get_meals_list(request))

    print(data)
    data_split = data.split('_')
    menu_type = data_split[0]
    menu_date = data_split[1]
    if menu_type == 'standart':
        menu_type = MenuType.objects.get(name=u'Стандартное')
    else:
        menu_type = MenuType.objects.get(name=u'Бизнес')
    menu_by_date = ComplexMenuByDate.objects.filter(date=menu_date, menu_type=menu_type)
    if menu_by_date:
        context.update({'menu_by_date': menu_by_date})
    meals = Meal.objects.all()
    context.update({
        'menus': ComplexMenu.objects.all(),
        'menu_type': menu_type,
        'active_dates': ActiveDates.objects.all(),
        'date': main_view.convert_date_from_db(menu_date),
        'meals': meals
    })

    return render(request, 'add_complex_menu.html', context)


# комплексное меню детали
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def complex_menu_details(request, menu_id):
    context = info(request)
    context.update(get_meals_list(request))
    menu_id_split = menu_id.split('_')
    menu_id = menu_id_split[1]
    menu = ComplexMenu.objects.get(id=menu_id)
    menu_date = main_view.convert_date_from_db(str(ComplexMenuByDate.objects.get(menu=menu).date))
    menu_meals = MealForComplexMenu.objects.filter(menu=menu)
    meals = Meal.objects.all()

    context.update({
        'menus': ComplexMenu.objects.all(),
        'menu_type': menu.menu_type,
        'active_dates': ActiveDates.objects.all(),
        'date': menu_date,
        'meals': meals,
        'menu': menu,
        'menu_meals': menu_meals
    })

    return render(request, 'add_complex_menu.html', context)


# сохранение комплексного меню на дату
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def save_complex_menu(request):
    if request.method == 'POST':
        menu_type = request.POST.get('menu_type')
        menu_level = request.POST.get('menu_level')
        menu_date = request.POST.get('menu_date')
        menu_name = request.POST.get('name')
        menu_price = request.POST.get('price')
        menu_id = request.POST.get('menu_id')
        menu_description = request.POST.get('description')
        if menu_type == 'standart':
            menu_type = MenuType.objects.get(name='Стандартное')
        if menu_type == 'business':
            menu_type = MenuType.objects.get(name='Бизнес')
        print(request.POST)
        if menu_id:
            complex_menu_ = ComplexMenu.objects.get(id=menu_id)
            MealForComplexMenu.objects.filter(menu=complex_menu_).delete()
            ComplexMenuByDate.objects.get(menu=complex_menu_).delete()
        else:
            complex_menu_ = ComplexMenu()
        menu_by_date = ComplexMenuByDate()
        complex_menu_.name = menu_name
        complex_menu_.price = Decimal(menu_price)
        complex_menu_.description = menu_description
        complex_menu_.menu_type = menu_type
        complex_menu_.save()
        # menu_by_date.date = main_view.convert_date_to_db(menu_date)
        menu_by_date.date = menu_date
        menu_by_date.menu = complex_menu_
        menu_by_date.menu_type = menu_type
        menu_by_date.save()

        for k in request.POST.keys():
            if 'meal_' in k and '_qnt' not in k:
                meal_split = request.POST.get(k).split('_')
                meal_id = meal_split[0]
                meal_qnt = meal_split[1]
                meal = Meal.objects.get(id=meal_id)
                meal_for_complex_menu = MealForComplexMenu(meal=meal, menu=complex_menu_, qnt=int(meal_qnt), menu_by_date=menu_by_date)
                meal_for_complex_menu.save()

        for k in request.FILES.keys():
            print('key = ' + str(k))
            for file in request.FILES.getlist(k):
                complex_menu_.image_246_246 = file
                complex_menu_.save()
                db_file_name = complex_menu_.image_246_246
                db_file_name_split = str(db_file_name).split('/')
                final_file_name = db_file_name_split[db_file_name_split.__len__() - 1]
                complex_menu_.image_name = final_file_name
                complex_menu_.save()
        return HttpResponse('standart')


# удаление блюда из комплексного меню
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def del_meal_from_complex_menu(request):
    if request.method == 'POST':
        menu_id = request.POST.get('menu_id')
        meal_id = request.POST.get('meal_id')
        menu = ComplexMenu.objects.get(id=menu_id)
        meal = Meal.objects.get(id=meal_id)
        MealForComplexMenu.objects.get(meal=meal, menu=menu).delete()
        return HttpResponse('Удаление блюда из комплексного меню')


# удаление фото комплексного меню
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def del_image_from_complex_menu(request):
    if request.method == 'POST':
        menu_id = request.POST.get('menu_id')
        menu = ComplexMenu.objects.get(id=menu_id)
        menu.image_246_246 = None
        menu.image_name = None
        menu.save()
        return HttpResponse('ok')


# удаление комплексного меню
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def del_complex_menu(request):
    if request.method == 'POST':
        menu_id = request.POST.get('menu_id').split('_')[1]
        ComplexMenu.objects.get(id=menu_id).delete()
        return HttpResponse(menu_id)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def icons(request):
    icons_ = Icon.objects.all()
    context = {
        'icons': icons_
    }
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        if not Icon.objects.filter(name=class_name).exists():
            icon = Icon()
            icon.name = class_name
            icon.save()
            response = 'ok'
        else:
            response = 'class exists'
        return HttpResponse(response)

    return render(request, 'icons.html', context)


# КЕЙТЕРИНГ
# площадки
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def places_list(request):
    context = info(request)
    context.update({
        'places': Place.objects.all()
    })
    return render(request, 'places_list.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def place_details(request, place_id):
    context = info(request)
    place = Place.objects.get(id=place_id)
    grey_options = PlaceGreyOption.objects.filter(place=place)
    options = PlaceOption.objects.filter(place=place)
    infrastructures = InfrastructureItem.objects.filter(place=place)
    images = PlaceImage.objects.filter(place=place, main=False)
    main_image = PlaceImage.objects.get(place=place, main=True)
    tags = Tag.objects.all().exclude(name__in=TagPlace.objects.filter(place=place))

    context.update({
        'place': place,
        'grey_options': grey_options,
        'options': options,
        'infrastructures': infrastructures,
        'edit': 1,
        'images': images,
        'icons': Icon.objects.all(),
        'main_image': main_image,
        'tags': tags,
        'place_tags': TagPlace.objects.filter(place=place),
        'contact_persons': PlaceContactPerson.objects.filter(place=place)

    })
    return render(request, 'add_new_place.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def add_place(request):
    context = info(request)
    context.update({
        'icons': Icon.objects.all(),
        'tags': Tag.objects.all()
    })
    if request.method == 'POST':
        data = request.POST
        place_id = data.get('place_id')
        if place_id:
            place = Place.objects.get(id=place_id)
        else:
            place = Place()

        main_name = data.get('main_name')
        description = data.get('description')
        place.description = description
        place.name = main_name
        place.save()
        TagPlace.objects.filter(place=place).delete()

        for k in data.keys():
            if 'tag' in k:
                tag_name = data.get(k)
                tag = Tag.objects.get(name=tag_name)
                tag_place = TagPlace(tag=tag, place=place)
                tag_place.save()
            if 'grey_desc' in k:
                grey_option = PlaceGreyOption()
                k_split = k.split('_')
                icon_id = k_split[4]
                grey_option.place = place
                grey_option.name = data.get(k)
                grey_option.icon = Icon.objects.get(id=icon_id)
                grey_option.save()
            if 'option' in k:
                option = PlaceOption()
                name_val_split = data.get(k).split('_')
                name = name_val_split[0]
                val = name_val_split[1]
                option.name = name
                option.place = place
                option.value = val
                option.save()
            if 'infrastructure_name' in k:
                infrastructure = InfrastructureItem()
                name = data.get(k)
                infrastructure.name = name
                infrastructure.place = place
                infrastructure.save()
        for file_key in request.FILES.keys():
            print('fk' + str(file_key))
            for file in request.FILES.getlist(file_key):
                # if 'main_foto' in file_key:
                #     files = request.FILES.getlist(file_key)
                # else:
                #     files = request.FILES.getlist('place_fotos')
                # files = request.FILES.getlist()
                print(file)
                # if files:
                # for file in files:
                place_image = PlaceImage()
                place_image.image = file

                path = os.path.join(settings.BASE_DIR, 'main\static\images\\watermark_logo.png')
                watermark = Image.open(path, 'r')
                pil_image = Image.open(file)
                pil_image.thumbnail((600, 400), Image.ANTIALIAS)
                w_w, w_h = watermark.size
                img_w, img_h = pil_image.size
                offset = (int((img_w - w_w) / 2), int((img_h - w_h) / 2))
                pil_image.paste(watermark, offset, watermark)
                thumb_io = BytesIO()
                pil_image.save(thumb_io, format='JPEG')
                file_to_save = ContentFile(thumb_io.getvalue())
                print(file_to_save)
                place_image.image_watermark.save('111.jpg', file_to_save)

                place_image.save()
                db_file_name = place_image.image
                db_file_name_watermark = place_image.image_watermark
                db_file_name_split = str(db_file_name).split('/')
                db_file_name_split_w = str(db_file_name_watermark).split('/')
                print(db_file_name_split_w.__len__())
                final_file_name = db_file_name_split[db_file_name_split.__len__() - 1]
                final_file_name_w = db_file_name_split_w[db_file_name_split_w.__len__() - 1]
                place_image.name = final_file_name
                place_image.name_watermark = final_file_name_w

                place_image.place = place
                place_image.save()
                # db_file_name = place_image.image
                # db_file_name_split = str(db_file_name).split('/')
                # final_file_name = db_file_name_split[db_file_name_split.__len__() - 1]
                place_image.name = final_file_name
                if 'main_foto' in file_key:
                    place_image.main = True
                    place.main_image = final_file_name
                    place.save()
                place_image.save()
            # main_foto = request.FILES.getlist('main_foto')
            # if main_foto:
        return HttpResponse()
    return render(request, 'add_new_place.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def delete_image_from_gallery(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        print(image_id)
        image = PlaceImage.objects.get(id=image_id).delete()
        return HttpResponse()


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def delete_place(request):
    context = info(request)
    context.update({
        'icons': Icon.objects.all()
    })
    if request.method == 'POST':
        place_id = request.POST.get('place_id')
        place = Place.objects.get(id=place_id).delete()
        return HttpResponse()


#контактные лица
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def add_contact_person(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('contact_person_name')
        place_id = data.get('place_id')
        person_id = data.get('person_id')
        if person_id:
            person = PlaceContactPerson.objects.get(id=person_id.split('_')[1])
            PhoneNumber.objects.filter(person=person).delete()
            UserEmail.objects.filter(person=person).delete()
            UserPaymentDetails.objects.filter(person=person).delete()
        else:
            person = PlaceContactPerson()
        place = Place.objects.get(id=place_id)
        person.name = name
        position = data.get('contact_person_position')
        add_info = data.get('contact_person_add_info')
        person.ad_info = add_info
        person.position = position
        person.place = place
        person.save()
        for key in data.keys():
            if 'payment_' in key:
                payment_split = data.get(key).split('_')
                payment_name = payment_split[0]
                payment_val = payment_split[1]
                payment = UserPaymentDetails()
                payment.person = person
                payment.name = payment_name
                payment.val = payment_val
                payment.save()
            if 'phone_new' in key:
                number = data.get(key)
                phone = PhoneNumber()
                phone.phone = number
                phone.person = person
                phone.save()
            if 'phone_phone_' in key:
                phone = PhoneNumber()
                number = data.get(key)
                phone.phone = number
                phone.person = person
                phone.save()
            if 'email_new' in key:
                email_new = data.get(key)
                user_email = UserEmail()
                user_email.person = person
                user_email.email = email_new
                user_email.save()
            if 'email_email' in key:
                email_new = data.get(key)
                user_email = UserEmail()
                user_email.person = person
                user_email.email = email_new
                user_email.save()
        return HttpResponse(person.id)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def contact_person_details(request):
    if request.method == 'POST':
        data = request.POST
        person_id = data.get('person_id').split('_')[1]
        person = PlaceContactPerson.objects.get(id=person_id)
        phones = PhoneNumber.objects.filter(person=person)
        emails = UserEmail.objects.filter(person=person)
        payment_details = UserPaymentDetails.objects.filter(person=person)
        phones_dic = {}
        for phone in phones:
            phones_dic.update({phone.id: phone.phone})

        emails_dic = {}
        for email in emails:
            emails_dic.update({email.id: email.email})

        payment_details_dic = {}
        for payment_detail in payment_details:
            payment_details_dic.update({payment_detail.name: payment_detail.val})
        response = {
            'name': person.name,
            'position': person.position,
            'add_info': person.ad_info,
            'phones': phones_dic,
            'emails': emails_dic,
            'payment_details': payment_details_dic
        }

        return HttpResponse(json.dumps({'response': response}))


#запросы клиентов
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def client_requests(request):
    context = info(request)
    context.update({
        'requests': ClientRequest.objects.all()
    })
    return render(request, 'client_requests.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def client_request_details(request, request_id):
    client_request = ClientRequest.objects.get(id=request_id)
    client_request.status = OrderStatus.objects.get(name=u'Обработан')
    client_request.save()
    context = info(request)
    context.update({
        'request': client_request
    })
    return render(request, 'request_details.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def new_client_requests(request):
    context = info(request)
    context.update({
        'requests': ClientRequest.objects.filter(status__name=u'Новый')
    })
    return render(request, 'client_requests.html', context)


# теги
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def tags_list(request):
    context = info(request)
    context.update({
        'tags': Tag.objects.all()
    })
    return render(request, 'tags_list.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def add_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        tag = Tag(name=name)
        tag.save()
        return HttpResponse(tag.id)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def del_tag(request):
    if request.method == 'POST':
        id_tag = request.POST.get('tag_id')
        tag = Tag.objects.get(id=id_tag).delete()
        return HttpResponse()


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def edit_tag(request):
    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        tag_name = request.POST.get('tag_name')
        tag = Tag.objects.get(id=tag_id)
        print(tag_name)
        tag.name = tag_name
        tag.save()
        return HttpResponse(tag_id)


# отзывы
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def testimonials_list(request):
    context = info(request)
    context.update({
        'testimonials': Testimonial.objects.all()
    })
    return render(request, 'testimonials_list.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def testimonial_details(request, test_id):
    context = info(request)
    testimonial = Testimonial.objects.get(id=test_id)
    context.update({
        'testimonial': testimonial
    })
    return render(request, 'testimonial_details.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def save_testimonial(request):
    context = info(request)

    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        organization = data.get('organization')
        text = data.get('text')
        approved = data.get('approved')
        test_id = data.get('id')
        print(data)
        if test_id:

            testimonial = Testimonial.objects.get(id=test_id)
        else:
            testimonial = Testimonial()
            testimonial.status = OrderStatus.objects.get(name=u'Новый')
        testimonial.name = name
        testimonial.organization = organization
        testimonial.text = text
        if approved == 'true':
            testimonial.approved = True
        else:
            testimonial.approved = False
        testimonial.save()
        return HttpResponse()
    return render(request, 'testimonial_details.html', context)


# цитаты
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def quotes_list(request):
    context = info(request)
    context.update({
        'quotes': Quote.objects.all()
    })
    return render(request, 'quotes_list.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def add_quote(request):
    context = info(request)
    if request.method == 'POST':
        data = request.POST
        author = data.get('author')
        text = data.get('text')
        date_ = data.get('quote_date')
        print(data)
        try:
            quote_id = data.get('quote_id')
            quote = Quote.objects.get(id=quote_id)
        except:
            quote = Quote()
        quote.author = author
        quote.text = text
        if date_:
            quote.date = main_view.convert_date_to_db(date_)
        quote.save()
        return HttpResponse()
    return render(request, 'quote_details.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def quote_details(request, quote_id):
    context = info(request)
    quote = Quote.objects.get(id=quote_id)
    date_to_show = main_view.convert_date_from_db(str(quote.date))
    context.update({
        'quote': quote,
        'date': date_to_show
    })
    return render(request, 'quote_details.html', context)


# портфолио
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def portfolio_list(request):
    context = info(request)
    context.update({
        'items': PortfolioItem.objects.all()
    })
    return render(request, 'portfolio_items_list.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def add_portfolio_item(request):
    context = info(request)
    context.update({
        'sliders': sliders
    })
    if request.method == 'POST':
        data = request.POST
        item_id = data.get('item_id')
        if item_id:
            item = PortfolioItem.objects.get(id=item_id)
        else:
            item = PortfolioItem()
        print(data)
        main_name = data.get('main_name')
        description = data.get('description')
        index = data.get('index')
        slider = data.get('slider')
        date_ = data.get('date')
        print(index)

        if index == 'on':
            item.index = True
        else:
            item.index = False
        if slider != 'choose':
            items = PortfolioItem.objects.all()
            for i in items:
                i.slider = None
                i.save()
            item.slider = slider
        else:
            item.slider = None
        if date_:
            item.date = main_view.convert_date_to_db(date_)
        item.description = description
        item.name = main_name
        item.save()

        for file_key in request.FILES.keys():
            print('fk' + str(file_key))
            for file in request.FILES.getlist(file_key):
                # if 'main_foto' in file_key:
                #     files = request.FILES.getlist(file_key)
                # else:
                #     files = request.FILES.getlist('place_fotos')
                # files = request.FILES.getlist()
                # if files:
                # for file in files:
                item_image = PortfolioItemImage()
                item_image.image = file

                path = os.path.join(settings.STATIC_ROOT, 'images/watermark_logo.png')
                watermark = Image.open(path, 'r')
                pil_image = Image.open(file)
                pil_image.thumbnail((600, 400), Image.ANTIALIAS)
                w_w, w_h = watermark.size
                img_w, img_h = pil_image.size
                offset = (int((img_w - w_w) / 2), int((img_h - w_h) / 2))
                pil_image.paste(watermark, offset, watermark)
                thumb_io = BytesIO()
                pil_image.save(thumb_io, format='JPEG')
                file_to_save = ContentFile(thumb_io.getvalue())
                print(file_to_save)
                item_image.portfolio_item = item
                item_image.image_watermark.save('111.jpg', file_to_save)

                item_image.save()
                db_file_name = item_image.image
                db_file_name_watermark = item_image.image_watermark
                db_file_name_split = str(db_file_name).split('/')
                db_file_name_split_w = str(db_file_name_watermark).split('/')
                print(db_file_name_split_w.__len__())
                final_file_name = db_file_name_split[db_file_name_split.__len__() - 1]
                final_file_name_w = db_file_name_split_w[db_file_name_split_w.__len__() - 1]
                item_image.name = final_file_name
                item_image.name_watermark = final_file_name_w
                if 'main_foto' in file_key:
                    item.main_image = final_file_name_w
                    item_image.main_image = True
                    item.save()
                item_image.save()
            # main_foto = request.FILES.getlist('main_foto')
            # if main_foto:
        return HttpResponse()
    return render(request, 'add_new_portfolio_item.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def portfolio_item_details(request, item_id):
    context = info(request)
    item = PortfolioItem.objects.get(id=item_id)
    if item.date:
        date_to_show = main_view.convert_date_from_db(str(item.date))
    else:
        date_to_show = ''
    try:
        main_image = PortfolioItemImage.objects.get(portfolio_item=item, main_image=True)
    except PortfolioItemImage.DoesNotExist:
        main_image = None
    images = PortfolioItemImage.objects.filter(portfolio_item=item, main_image=False)
    context.update({
        'item': item,
        'date': date_to_show,
        'main_image': main_image,
        'images': images,
        'sliders': sliders
    })
    return render(request, 'add_new_portfolio_item.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def delete_image_from_gallery_portfolio(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')

        image = PortfolioItemImage.objects.get(id=image_id)
        path = image.image.url
        # print(path)
        # os.remove(path)
        image.delete()
        return HttpResponse()


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def delete_portfolio_item(request):
    if request.method == 'POST':
        data = request.POST
        item_id = data.get('item_id')
        item = PortfolioItem.objects.get(id=item_id)
        item.delete()
        return HttpResponse()


# персонал
@login_required(redirect_field_name=None, login_url='/dashboard/login')
def staff_list(request):
    context = info(request)
    context.update({
        'staffs': Staff.objects.all()
    })
    return render(request, 'staffs_list.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def add_staff(request):

    context = info(request)
    if request.method == 'POST':
        data = request.POST
        # print(data)
        staff_id = data.get('staff_id')
        if staff_id:
            staff = Staff.objects.get(id=staff_id)
        else:
            staff = Staff()
        name = data.get('name')
        position = data.get('position')
        phone = data.get('phone')
        email = data.get('email')
        add_info = data.get('add_info')
        index = data.get('index')
        image_uri = data.get('crop_image')
        image_base64 = image_uri.split('base64,')
        image_data = base64.b64decode(image_base64[1])
        # url_decoded = base64.b64encode(image_uri.encode())
        content = ContentFile(image_data)
        staff.image.save('1.png', content)

        if staff.image:
            db_file_name = staff.image
            db_file_name_split = str(db_file_name).split('/')
            final_file_name = db_file_name_split[db_file_name_split.__len__() - 1]
            staff.image_name = final_file_name
            staff.save()

        # print(request.FILES)

        # dataurlpattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        # imagedata = dataurlpattern.match(image_uri).group(2)

        # If none or len 0, means illegal image data
        # if imagedata == None or len(imagedata) == 0:
        # PRINT ERROR MESSAGE HERE
        #     pass

        # Decode the 64 bit string into 32 bit
        # imagedata = base64.b64decode(imagedata)

        # imgstr = re.search(r'base64,(.*)', image_uri).group(1)
        # output_file = open('111.jpg', 'wb')
        # output_file.write(image_data)
        # output_file.close()
        # with open('111.jpg') as file:
        #
        #     staff.image = file
        # image = request.FILES.get('image')
        staff.name = name
        staff.phone = phone
        staff.email = email
        staff.add_info = add_info
        if index == 'on':
            staff.index = True
        else:
            staff.index = False
        staff.position = position
        # if image:
        #     staff.image = image
        staff.save()
        # output_file.close()

        # if image:
        #     db_file_name = staff.image
        #     db_file_name_split = str(db_file_name).split('/')
        #     final_file_name = db_file_name_split[db_file_name_split.__len__() - 1]
        #     staff.image_name = final_file_name
        #     staff.save()
        return HttpResponse()
    return render(request, 'add_new_staff.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def staff_details(request, staff_id):
    context = info(request)
    staff = Staff.objects.get(id=staff_id)
    context.update({
        'staff': staff,
    })
    return render(request, 'add_new_staff.html', context)


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def delete_image_from_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        staff = Staff.objects.get(id=staff_id)
        staff.image = None
        staff.image_name = None
        staff.save()
        return HttpResponse()


@login_required(redirect_field_name=None, login_url='/dashboard/login')
def delete_staff(request):
    if request.method == 'POST':
        data = request.POST
        staff_id = data.get('staff_id')
        staff = Staff.objects.get(id=staff_id)
        staff.delete()
        return HttpResponse()


