from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

# Create your models here.


class MinSum(models.Model):
    sum = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class Role(models.Model):
    name = models.CharField(max_length=20)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    role = models.ForeignKey(Role)


class MealType(models.Model):
    name = models.CharField(max_length=20)


class MenuType(models.Model):
    name = models.CharField(max_length=30)


class Ingredients(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=200, null=True)
    added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)


class Meal(models.Model):
    name = models.CharField(max_length=50)
    weight = models.CharField(max_length=10)
    meal_type = models.ForeignKey(MealType)
    description = models.CharField(max_length=100)
    short_description = models.CharField(max_length=300, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image_name = models.CharField(max_length=100, null=True, blank=True)


class IngredientsForMeal(models.Model):
    ingredient = models.ForeignKey(Ingredients)
    meal = models.ForeignKey(Meal)
    weight = models.CharField(max_length=10)


class MealImage(models.Model):
    meal = models.ForeignKey(Meal)
    image_70_70 = models.ImageField(upload_to=settings.BASE_DIR + '/main/static/images/meals', null=True, blank=True)
    image_350_350 = models.ImageField(upload_to=settings.BASE_DIR + '/main/static/images/meals', null=True, blank=True)
    image_name = models.CharField(max_length=100, null=True, blank=True)


class MealByDate(models.Model):
    date = models.DateField(null=True, blank=True)
    meal = models.ForeignKey(Meal)


class ComplexMenu(models.Model):
    name = models.CharField(max_length=50)
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    menu_type = models.ForeignKey(MenuType, null=True, blank=True)
    image_246_246 = models.ImageField(upload_to='menu', null=True, blank=True)
    image_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)


class ComplexMenuByDate(models.Model):
    date = models.DateField(null=True, blank=True)
    menu = models.ForeignKey(ComplexMenu)
    menu_type = models.ForeignKey(MenuType, null=True, blank=True)


class MealForComplexMenu(models.Model):
    meal = models.ForeignKey(Meal)
    menu = models.ForeignKey(ComplexMenu)
    qnt = models.IntegerField(blank=True, null=True)
    menu_by_date = models.ForeignKey(ComplexMenuByDate, blank=True, null=True)


class ActiveDates(models.Model):
    date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)


class CartType(models.Model):
    name = models.CharField(max_length=20)


class Cart(models.Model):
    cart_type = models.ForeignKey(CartType)
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    meals_qnt = models.IntegerField(null=True)
    menu_date = models.DateField(null=True, blank=True)
    cutlery = models.IntegerField(null=True, blank=True)


class CartMeals(models.Model):
    meal = models.ForeignKey(Meal, null=True, blank=True)
    cart = models.ForeignKey(Cart, null=True, blank=True)
    meal_qnt = models.IntegerField(null=True, blank=True)
    menu = models.ForeignKey(ComplexMenu, null=True, blank=True)


class City(models.Model):
    name = models.CharField(max_length=20)


class Company(models.Model):
    name = models.CharField(max_length=100)


class Client(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    tel = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    company = models.ForeignKey(Company, null=True, blank=True)


class OrderStatus(models.Model):
    name = models.CharField(max_length=50)


class Order(models.Model):
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    delivery_time = models.TimeField(null=True, blank=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False)
    client = models.ForeignKey(Client)
    status = models.ForeignKey(OrderStatus)
    cart = models.ForeignKey(Cart)
    ad_info = models.CharField(max_length=200, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    house = models.CharField(max_length=50, null=True, blank=True)
    flat = models.CharField(max_length=50, null=True, blank=True)


# catering

class Icon(models.Model):
    name = models.CharField(max_length=20)


class Place(models.Model):
    name = models.CharField(max_length=150, null = True, blank = True)
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    main_image = models.CharField(max_length=150, null=True, blank=True)


class PlaceGreyOption(models.Model):
    name = models.CharField(max_length=150)
    icon = models.ForeignKey(Icon)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)


class Option(models.Model):
    name = models.CharField(max_length=150)
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False)


class InfrastructureItem(models.Model):
    name = models.CharField(max_length=150)
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, null=True, blank=True)


class PlaceOption(models.Model):
    name = models.CharField(max_length=150)
    place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.CASCADE)
    infrastructure_item = models.ForeignKey(InfrastructureItem, null=True, blank=True)
    value = models.CharField(max_length=50, null=True, blank=True)


class PlaceImage(models.Model):
    name = models.CharField(max_length=150)
    name_watermark = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to=settings.BASE_DIR + '/main/static/images/places', null=True, blank=True)
    image_watermark = models.ImageField(upload_to=settings.BASE_DIR + '/main/static/images/places/watermark/', null=True, blank=True)
    place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.CASCADE)
    infrastructure_item = models.ForeignKey(InfrastructureItem, null=True, blank=True)
    main = models.BooleanField(default=False)


class PlaceContactPerson(models.Model):
    added = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
    place = models.ForeignKey(Place, null=True, blank=True)
    ad_info = models.CharField(max_length=1000, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)


class PhoneNumber(models.Model):
    phone = models.CharField(max_length=20)
    person = models.ForeignKey(PlaceContactPerson, null=True, blank=True)


class UserEmail(models.Model):
    email = models.CharField(max_length=20)
    person = models.ForeignKey(PlaceContactPerson, null=True, blank=True)


class UserPaymentDetails(models.Model):
    name = models.CharField(max_length=100)
    val = models.CharField(max_length=100)
    person = models.ForeignKey(PlaceContactPerson, null=True, blank=True)


class ClientRequest(models.Model):
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
    client_name = models.CharField(max_length=100, null=True, blank=True)
    client_phone = models.CharField(max_length=50, null=True, blank=True)
    client_email = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=1000, null=True, blank=True)
    status = models.ForeignKey(OrderStatus, null=True, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=100)


class TagPlace(models.Model):
    place = models.ForeignKey(Place, null=True, blank=True)
    tag = models.ForeignKey(Tag, null=True, blank=True)


class Testimonial(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    text = models.CharField(max_length=2000, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    status = models.ForeignKey(OrderStatus, null=True, blank=True)
    approved = models.BooleanField(default=False)


class Quote(models.Model):
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    text = models.CharField(max_length=2000, null=True, blank=True)
    author = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(null=True, blank=True)


class PortfolioItem(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    main_image = models.CharField(max_length=150, null=True, blank=True)
    index = models.BooleanField(default=False)
    slider = models.CharField(max_length=50, null=True, blank=True)


class PortfolioItemImage(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=settings.BASE_DIR + '/main/static/images/portfolio', null=True, blank=True)
    image_watermark = models.ImageField(upload_to=settings.BASE_DIR + '/main/static/images/portfolio/watermark', null=True, blank=True)
    portfolio_item = models.ForeignKey(PortfolioItem, on_delete=models.CASCADE)
    main_image = models.BooleanField(default=False)
    name_watermark = models.CharField(max_length=150, null=True, blank=True)


class Staff(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=settings.BASE_DIR + '/main/static/images/staff', null=True, blank=True)
    image_name = models.CharField(max_length=150, null=True, blank=True)
    add_info = models.CharField(max_length=2000, null=True, blank=True)
    added = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
    index = models.BooleanField(default=False)


