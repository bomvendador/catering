# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, render_to_response
from main.models import Meal, ActiveDates, MealByDate, Cart, CartType, CartMeals, MinSum, OrderStatus, Order, Client, Company, City, UserProfile, Role, MealImage, IngredientsForMeal, ComplexMenu, ComplexMenuByDate, MealForComplexMenu, Place, PlaceImage, InfrastructureItem, PlaceGreyOption, PlaceOption, ClientRequest, TagPlace, Tag, Testimonial, Quote, PortfolioItem, PortfolioItemImage, Staff
# Create your views here.
import json
from django.core.serializers.json import DjangoJSONEncoder

from catering import settings
from django.db.models import Sum
from datetime import date, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@property
def is_past(self):
    return date.today() > self.date


def get_info():
    context = {
        'min_sum': MinSum.objects.get(id=1).sum,
        'testimonials': Testimonial.objects.all(),
        'food_smile_phone': settings.PHONE_NUMBER,
        'food_smile_email': settings.CONTACT_EMAIL
    }
    return context


def index_view(request):
    context = get_info()
    min_sum = get_info()['min_sum']
    # print(min_sum)
    context.update({
        'min_sum': min_sum,
        'portfolio_items': PortfolioItem.objects.filter(index=True),
        'staffs': Staff.objects.filter(index=True)

    })
    return render(request, 'index.html', context)


def gallery_portfolio(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id').split('_')[1]
        # slide_id = request.POST.get('slide_id').split('_')[1]
        images = PortfolioItemImage.objects.filter(portfolio_item=PortfolioItem.objects.get(id=item_id))

        record = []
        for image in images:
            record.append(image.name_watermark)
        response = {'response': record}
        return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))


def convert_date_to_db(date):
    menu_date_split = date.split('.')
    menu_date = menu_date_split[2] + '-' + menu_date_split[1] + '-' + menu_date_split[0]
    return menu_date


def convert_date_from_db(date):
    menu_date_split = date.split('-')
    menu_date = menu_date_split[2] + '.' + menu_date_split[1] + '.' + menu_date_split[0]
    return menu_date


def lunches_index(request):
    context = get_info()
    try:
        quote = Quote.objects.get(date=date.today())
    except Quote.DoesNotExist:
        quote = ''
    context.update({
        'quote': quote
    })
    return render(request, 'lunches.html', context)


def standart_menu(request):
    # if request.method == 'POST':

    active_dates = ActiveDates.objects.filter(date__gte=date.today() + timedelta(days=1)).order_by('date')
    # print(active_dates[:1].get().date)
    if active_dates:
        meals = MealByDate.objects.filter(date=active_dates[0].date)
        # meals = MealByDate.objects.filter(date=active_dates[:1].get().date)
    else:
        meals = None
    # for i in active_dates:
    #     print(str(i.date))
    context = {
        'active_dates': active_dates,
        'meals': meals,
        'min_sum': MinSum.objects.all()[0].sum,
        'menu_type': 'standart_menu',
        'url_redirect': 'standart_menu'

    }
    return render(request, 'standart_menu.html', context)


# получение блюд по дате
def standart_menu_by_date(request, menu_date_raw):
    context = {}
    # if request.method == 'POST':
    menu_date_split = menu_date_raw.split('.')
    menu_date = menu_date_split[2] + '-' + menu_date_split[1] + '-' + menu_date_split[0]

    active_dates = ActiveDates.objects.filter(date__gte=date.today() + timedelta(days=1)).order_by('date')
    meals = MealByDate.objects.filter(date=menu_date)

    # for i in active_dates:
    #     print(str(i.date))
    print('redir')
    # if check_cart_for_date(cart_id):
    context.update(get_info())

    context.update({
        'menu_date': menu_date_raw,
        'active_dates': active_dates,
        'meals': meals,
        'date_redirected': 'yes',
        'menu_type': 'standart_menu'
    })
    return render(request, 'standart_menu.html', context)


# проверка даты корзины
def check_cart_for_date(cart_id):
    cart = Cart.objects.get(id=cart_id)
    if cart.menu_date > date.today():
        return True
    else:
        return False


# первоначальная проверка корзины
def check_cart(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        cart_id = json_data['cart_id']
        response = {}
        if cart_id != 'no_cart':
            try:
                cart = Cart.objects.get(id=cart_id)
                cutlery = cart.cutlery
            except Cart.DoesNotExist:
                cart = None
            if cart:
                if check_cart_for_date(cart_id):
                    if cart.meals_qnt > 0:
                        cart_meals_dict = {}
                        cart_meals_records = []
                        # cart_meals = CartMeals.objects.filter(cart=cart).values_list('meal', flat=True).distinct()
                        cart_meals = CartMeals.objects.filter(cart=cart)
                        print(cart_meals)
                        for cart_meal in cart_meals:
                            # try:
                            #     meal = Meal.objects.get(id=cart_meal.meal.id)
                            # except Meal.DoesNotExist:
                            #     meal = None
                            if cart_meal.meal:
                            # if meal:
                                meal = Meal.objects.get(id=cart_meal.meal.id)
                                meal_cart = CartMeals.objects.get(meal=meal, cart=cart)
                                meal_price = meal.price
                                meal_qnt = meal_cart.meal_qnt

                                meal_sum = meal_qnt * meal_price
                                if len(meal.name) > 15:
                                    meal_name = meal.name[:15] + '...'
                                else:
                                    meal_name = meal.name
                                full_meal_name = meal.name
                                meal_img = meal.image_name
                                meal_id = meal.id
                                meal_img_url = 'meals'
                                item_type = 'meal'
                            else:
                                menu = ComplexMenu.objects.get(id=cart_meal.menu.id)
                                meal_cart = CartMeals.objects.get(menu=ComplexMenu.objects.get(id=cart_meal.menu.id), cart=cart)
                                meal_qnt = meal_cart.meal_qnt
                                meal_price = menu.price
                                meal_sum = meal_qnt * meal_price
                                if len(menu.name) > 15:
                                    meal_name = menu.name[:15] + '...'
                                else:
                                    meal_name = menu.name
                                full_meal_name = menu.name
                                meal_img = menu.image_name
                                meal_id = menu.id
                                meal_img_url = 'menu'
                                item_type = 'menu'

                            record = {
                                'meal_price': meal_price,
                                'meal_id': meal_id,
                                'meal_qnt': meal_qnt,
                                'meal_sum': meal_sum,
                                'meal_img': meal_img,
                                'meal_name': meal_name,
                                'full_meal_name': full_meal_name,
                                'meal_img_url': meal_img_url,
                                'item_type': item_type
                            }
                            cart_meals_records.append(record)
                            print(cart_meals_records)
                            # for k in cart_meals_records:
                            #     for mk, mv in k:
                            #         print(mk + ':' + mv)
                        # cart_meals_records = json.dumps({'cart_meals': cart_meals_records}, cls=DjangoJSONEncoder)
                        # cart_meals_dict['cart_meals'] = cart_meals_records
                        if date.today() < cart.menu_date:
                            allowed_menu = 1
                        else:
                            allowed_menu = 0
                            active_dates = ActiveDates.objects.filter(date__gte=date.today() + timedelta(days=1)).order_by(
                                'date')
                            response.update({
                                'redirect': convert_date_from_db(str(active_dates[0]))

                            })

                        response.update({'cart_meal': cart_meals_records, 'cart_meals_qnt': cart.meals_qnt, 'cart_amount': cart.amount, 'allowed_menu': allowed_menu, 'menu_date': convert_date_from_db(str(cart.menu_date)), 'min_sum': MinSum.objects.all()[0].sum, 'cutlery': cutlery})
                    else:
                        response = 'no_data'
                    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))
                else:
                    return HttpResponse(json.dumps({'cart_meal': 0}))
            else:
                response = 'no_data'
                return HttpResponse(json.dumps({'response': response}))
        else:
            active_dates = ActiveDates.objects.filter(date__gte=date.today() + timedelta(days=1)).order_by(
                'date')
            response.update({
                'redirect': convert_date_from_db(str(active_dates[0]))

            })

            return HttpResponse(json.dumps(response))


# добавление блюд в карзину
def add_to_cart(request):
    if request.method == 'POST':
        response = {}
        json_data = json.loads(request.body.decode('utf-8'))
        # meal_id_raw = json_data['meal_id']
        print(json_data)
        meal_id = json_data['meal_id']
        try:
            complex_menu_id = json_data['menu_id']
        except:
            pass
        # meal_id = meal_id_raw.split('_')[1]
        cart_id = json_data['cart_id']
        meal_qnt = int(json_data['meal_qnt'])
        menu_date = json_data['menu_date']
        print(json_data)
        # print(meal_id)
        if meal_id != '':
            meal = Meal.objects.get(id=meal_id)
        else:
            menu = ComplexMenu.objects.get(id=str(complex_menu_id))
        if cart_id == 'no_cart':
            cart_meals = CartMeals()
            cart = Cart()
            cart.cart_type = CartType.objects.get(name=u'Текущая')
            cart.meals_qnt = meal_qnt
            if meal_id != '':
                cart.amount = meal.price * meal_qnt
                cart_meals.meal = meal
            else:
                cart.amount = menu.price * meal_qnt
                cart_meals.menu = menu
            cart.menu_date = convert_date_to_db(menu_date)
            cart.save()
            cart_meals.cart = cart
            cart_meals.meal_qnt = meal_qnt

            cart_meals.save()
        else:
            cart = Cart.objects.get(id=cart_id)
            cart.meals_qnt += meal_qnt
            if meal_id != '':
                cart.amount += meal.price * meal_qnt
                meal = Meal.objects.get(id=meal_id)
                cart.save()
                try:
                    cart_meal_qnt = CartMeals.objects.filter(cart=cart, meal=meal).count()
                except CartMeals.DoesNotExist:
                    cart_meal_qnt = 0

            else:
                cart.amount += menu.price * meal_qnt
                cart.save()
                try:
                    cart_meal_qnt = CartMeals.objects.filter(cart=cart, menu=menu).count()
                except CartMeals.DoesNotExist:
                    cart_meal_qnt = 0

            if cart_meal_qnt > 0:
                if meal_id != '':
                    cart_meals = CartMeals.objects.get(meal=meal, cart=cart)
                else:
                    cart_meals = CartMeals.objects.get(menu=menu, cart=cart)

                cart_meals.meal_qnt += meal_qnt
            else:
                cart_meals = CartMeals()
                cart_meals.cart = cart
                if meal_id != '':
                    cart_meals.meal = meal
                else:
                    cart_meals.menu = menu

                cart_meals.meal_qnt = meal_qnt

            # try:
            #     cart_menu_qnt = CartMeals.objects.filter(cart=cart, menu=menu).count()
            # except CartMeals.DoesNotExist:
            #     cart_menu_qnt = 0
            # if cart_menu_qnt > 0:
            #     cart_menus = CartMeals.objects.get(menu=menu, cart=cart)
            #     cart_menus.meal_qnt += meal_qnt
            # else:
            #     cart_meals = CartMeals()
            #     cart_meals.cart = cart
            #     cart_meals.menu = menu
            #     cart_meals.meal_qnt = meal_qnt
            cart_meals.save()
        if meal_id != '':
            response.update({
                'meal_price': meal.price,
                'meal_qnt': CartMeals.objects.get(cart=cart, meal=meal).meal_qnt,
                'meal_sum': meal.price * CartMeals.objects.filter(cart=cart, meal=meal).count(),
                'meal_img': meal.image_name,
                'meal_name': meal.name,
                'meal_id': meal_id,
                'item_type': 'meal'

            })
        else:
            response.update({
                'menu_qnt': CartMeals.objects.get(cart=cart, menu=menu).meal_qnt,
                'menu_price': menu.price,
                'menu_sum': menu.price * CartMeals.objects.filter(cart=cart, menu=menu).count(),
                'menu_img': menu.image_name,
                'menu_name': menu.name,
                'menu_id': complex_menu_id,
                'item_type': 'menu'

            })
        response.update({
            'total_amount': cart.amount,
            'cart_id': cart.id,
            'cart_meals_qnt': cart.meals_qnt,
            'min_sum': MinSum.objects.all()[0].sum,
        })

        return HttpResponse(json.dumps({'response': response}, cls=DjangoJSONEncoder))
    else:
        return HttpResponse(json.dumps({'response': 'no_data'}))


# удаление блюд из карзины
def del_from_minicart(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        meal_id_raw = json_data['meal_id']
        meal_id = meal_id_raw.split('_')[3]
        type = meal_id_raw.split('_')[1]
        cart_id = json_data['cart_id']
        cart = Cart.objects.get(id=cart_id)
        if type == 'meal':
            meal = Meal.objects.get(id=meal_id)
            cart_meals_amount = CartMeals.objects.get(cart=cart, meal=meal).meal_qnt * meal.price
            CartMeals.objects.get(cart=cart, meal=meal).delete()
        else:
            menu = ComplexMenu.objects.get(id=meal_id)
            cart_meals_amount = CartMeals.objects.get(cart=cart, menu=menu).meal_qnt * menu.price
            CartMeals.objects.get(cart=cart, menu=menu).delete()
        cart.amount -= cart_meals_amount

        response = {}
        min_sum = get_info()['min_sum']
        # print(min_sum)
        response.update({'min_sum': min_sum})
        cart_meals_qnt = CartMeals.objects.filter(cart=cart).aggregate(Sum('meal_qnt'))['meal_qnt__sum']
        if cart_meals_qnt:
            cart.meals_qnt = cart_meals_qnt
        else:
            cart.meals_qnt = 0
        print('qqq' + str(CartMeals.objects.filter(cart=cart).aggregate(Sum('meal_qnt'))))
        cart.save()
        response.update({
            'total_amount': cart.amount,
            'type': type,
            'meal_id': meal_id,
            'cart_meals_qnt': cart.meals_qnt

        })
        return HttpResponse(json.dumps({'response': response}, cls=DjangoJSONEncoder))


# изменение кол-ва блюд в карзине
def change_meals_qnt(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        meal_id_raw = json_data['meal_id']


def cart_for_checkout(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    context = {'min_sum': get_info()['min_sum']}
    return render(request, 'cart.html', context)


def to_checkout(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        cart_id = request.POST.get('cart_id')
        cutlery = request.POST.get('cutlery')
        print('cut = ' + str(cutlery))
        cart = Cart.objects.get(id=cart_id)
        cart_amount = 0
        cart_meals_qnt = 0
        for k, v in request.POST.items():
            if 'qnt' in k:
                # print(k + ' - ' + v)
                meal_id_split = k.split('_')
                meal_id = meal_id_split[2]
                type = meal_id_split[0]
                # print('id = ' + meal_id)
                if type == 'meal':
                    meal = Meal.objects.get(id=meal_id)
                    cart_meals = CartMeals.objects.get(meal=meal, cart=cart)
                else:
                    meal = ComplexMenu.objects.get(id=meal_id)
                    cart_meals = CartMeals.objects.get(menu=meal, cart=cart)

                cart_meals.meal_qnt = v
                cart_meals.save()
                cart_amount += int(v) * meal.price
                cart_meals_qnt += int(v)
        cart.amount = cart_amount
        cart.meals_qnt = cart_meals_qnt
        cart.cutlery = cutlery
        cart.save()
        return HttpResponse(cart_id)


def checkout(request, cart_id):
    return render(request, 'checkout.html')


def save_order(request):
    if request.method == 'POST':
        name = request.POST.get('billing_first_name')
        company_name = request.POST.get('billing_company')
        phone = request.POST.get('billing_phone')
        last_name = request.POST.get('billing_last_name')
        address = request.POST.get('billing_address')
        email = request.POST.get('billing_email')
        house = request.POST.get('billing_house')
        flat = request.POST.get('billing_flat')
        additional_info = request.POST.get('additional_info')
        cart_id = request.POST.get('cart_id')
        cart = Cart.objects.get(id=cart_id)
        order = Order()
        client = Client()
        company = Company()
        company.name = company_name
        company.save()

        client.name = name
        client.surname = last_name
        client.tel = phone
        client.email = email
        client.company = company

        # client.user_profile = UserProfile.objects.get(role=Role.objects.get(name=u'Клиент'))
        client.save()

        order.address = address
        order.house = house
        order.flat = flat
        order.city = City.objects.get(name=u'Москва')
        order.cart = Cart.objects.get(id=cart_id)
        order.client = client
        order.status = OrderStatus.objects.get(name=u'Новый')
        order.cart = cart
        order.ad_info = additional_info
        order.save()

        cart.cart_type = CartType.objects.get(name='Оформленная')

    return HttpResponse(order.id)


def product_details(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    meal_imgs = MealImage.objects.filter(meal=meal, image_name__isnull=False)
    print(meal_imgs.__len__())
    context = {
        'meal': meal,
        'meal_imgs': meal_imgs,
        'meal_ingredients': IngredientsForMeal.objects.filter(meal=meal)
    }
    return render_to_response('product-detail-popup.html', context)


def product_details_complex(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    meal_imgs = MealImage.objects.filter(meal=meal, image_name__isnull=False)
    print(meal_imgs.__len__())
    context = {
        'meal': meal,
        'meal_imgs': meal_imgs,
        'meal_ingredients': IngredientsForMeal.objects.filter(meal=meal)
        # 'menu_id'
    }
    return render_to_response('product-detail-popup_complex.html', context)


def complex_menu_details(request, menu_id):
    menu = ComplexMenu.objects.get(id=menu_id)
    meals = MealForComplexMenu.objects.filter(menu=menu)
    # menu_img = MealImage.objects.filter(meal=meal, image_name__isnull=False)
    context = {
        'meals': meals,
        # 'meal_imgs': meal_imgs,
        'menu': menu,
        'menu_id': menu.id
    }
    return render_to_response('complex-menu-detail-popup.html', context)


def complex_standart_menu(request):
    active_dates = ActiveDates.objects.filter(date__gte=date.today() + timedelta(days=1)).order_by('date')
    print(active_dates[0].date)
    context = get_info()
    context.update({
        'redirect': convert_date_from_db(str(active_dates[0].date)),
        'url_redirect': 'complex_standart_menu_by_date',

    })
    context.update({
        'active_dates': active_dates,

    })
    # if date.today() < cart.menu_date:
    #     allowed_menu = 1
    # else:
    #     allowed_menu = 0

    if request.method == 'POST':
        menu_date = request.POST.get('menu_date')
        menus = ComplexMenuByDate.objects.filter(date=convert_date_to_db(menu_date))
        context.update({
            'menus': menus,
        })

    return render(request, 'complex_menu.html', context)


def complex_standart_menu_by_date(request, menu_date):
    active_dates = ActiveDates.objects.filter(date__gte=date.today() + timedelta(days=1)).order_by('date')
    context = get_info()
    context.update({
        'active_dates': active_dates,
        'url_redirect': 'complex_standart_menu_by_date',
        'date_redirected': 'yes',

    })

    menus = ComplexMenuByDate.objects.filter(date=convert_date_to_db(menu_date))
    menu_meals = MealForComplexMenu.objects.filter(menu_by_date__in=menus)
    context.update({
        'menus': menus,
        'menu_meals': menu_meals,
        'menu_date': menu_date
    })

    return render(request, 'complex_menu.html', context)


def catering_index_page(request):
    context = get_info()

    return render(request, 'catering_index.html', context)


def place_details(request, place_id):
    context = get_info()
    place = Place.objects.get(id=place_id)
    options = PlaceOption.objects.filter(place=place)
    infrastructures = InfrastructureItem.objects.filter(place=place)
    images = PlaceImage.objects.filter(place=place)
    grey_options = PlaceGreyOption.objects.filter(place=place)
    places = Place.objects.all().exclude(id=place.id)[0:5]
    context.update({
        'place': place,
        'infrastructures': infrastructures,
        'images': images,
        'grey_options': grey_options,
        'options': options,
        'places': places,
        'place_tags': TagPlace.objects.filter(place=place),
        'tags': Tag.objects.filter(tagplace__in=TagPlace.objects.all()).distinct()

    })
    return render(request, 'place_details.html', context)


def place_client_request(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        place_id = data.get('place_id')
        message = data.get('message')
        client_request = ClientRequest()
        if place_id:
            place = Place.objects.get(id=place_id)
            client_request.place = place
        client_request.client_name = name
        client_request.client_email = email
        client_request.client_phone = phone
        client_request.message = message
        client_request.status = OrderStatus.objects.get(name=u'Новый')
        client_request.save()
        return HttpResponse()


def places_list_main(request):
    context = get_info()
    tag_id = request.POST.get('tag_id')
    if tag_id:
        places_list_ = Place.objects.filter(id=TagPlace.objects.get(tag_id=tag_id))
    else:
        places_list_ = Place.objects.all()
    paginator = Paginator(places_list_, 3)
    page = request.POST.get('page')
    if not page:
        places = paginator.page(1)
    try:
        places = paginator.page(page)
        context = {'places': places}
        return render_to_response('places_list_content.html', context)
    except PageNotAnInteger:
        places = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        places = paginator.page(paginator.num_pages)

    # try:
    #     places = paginator.page(page)
    # except PageNotAnInteger:
    context.update({
        'places': places,
        'pages_qnt': paginator.count,
        'pages_num': paginator.page_range,
        'cur_page_number': 1,
        'tags': Tag.objects.filter(tagplace__in=TagPlace.objects.all()).distinct()
        # 'place_tags': TagPlace.obje   cts.filter(place=places)
    })
    return render(request, 'places_list_main.html', context)


def places_list_main_by_tag(request, tag_id):
    context = get_info()
    places_list_ = Place.objects.filter(tagplace__in=TagPlace.objects.filter(tag_id=tag_id))
    paginator = Paginator(places_list_, 1)
    page = request.POST.get('page')
    context.update({'tag': Tag.objects.get(id=tag_id)})
    if not page:
        places = paginator.page(1)
    try:
        places = paginator.page(page)
        context = {'places': places}
        return render_to_response('places_list_content.html', context)
    except PageNotAnInteger:
        places = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        places = paginator.page(paginator.num_pages)

    # try:
    #     places = paginator.page(page)
    # except PageNotAnInteger:
    context.update({
        'places': places,
        'pages_qnt': paginator.count,
        'pages_num': paginator.page_range,
        'cur_page_number': 1,
        'tags': Tag.objects.filter(tagplace__in=TagPlace.objects.all()).distinct()

        # 'place_tags': TagPlace.obje   cts.filter(place=places)
    })
    return render(request, 'places_list_main.html', context)


def get_place_tags(request):
    place_id = request.POST.get('place_id')
    place = Place.objects.get(id=place_id)
    place_tags = TagPlace.objects.filter(place=place)

    place_tags_arr = {}
    for place_tag in place_tags:
        key = 'tag_' + str(place_tag.tag.id)
        place_tags_arr.update({
            key: place_tag.tag.name
        })
    response = {'id': place.id, 'place_tags_arr': place_tags_arr}
    print('r' + str(response))
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))


# меропрития
def events_index(request):
    context = get_info()
    portfolio = PortfolioItem.objects.get(slider=u'Блюда на странице кейтеринга')
    portfolio_for_slider = portfolio
    context.update({
        'portfolio': portfolio,
        'slides': PortfolioItemImage.objects.filter(portfolio_item=portfolio_for_slider)
    })
    return render(request, 'events_index.html', context)


#контакты
def contacts(request):
    context = get_info()
    return render(request, 'contacts.html', context)