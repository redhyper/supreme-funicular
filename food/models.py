import jwt
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import models, transaction
from datetime import datetime, timedelta
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class Role(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):

    def _create_user(self, login, password, **extra_fields):

        if not login:
            raise ValueError('The given login must be set')
        try:
            with transaction.atomic():
                user = self.model(login=login, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login, password, **extra_fields)

    def create_superuser(self, login, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(login, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Логин', default='')
    email = models.EmailField(db_index=True, max_length=50, unique=True, verbose_name='Email')
    name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
    surname = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Должность', null=True)
    phone = models.CharField(max_length=100, verbose_name='Телефон')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_of_add = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.login

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')


class Table(models.Model):
    name = models.CharField(max_length=200, default='')


class Department(models.Model):
    name = models.CharField(max_length=200, default='')


class MealsCategory(models.Model):
    name = models.CharField(max_length=100, default='')
    departmentid = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')


class Status(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ServicePercentage(models.Model):
    percentage = models.FloatField()

    def __str__(self):
        return self.percentage


class Meal(models.Model):
    category = models.ForeignKey(MealsCategory, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    waiterid = models.IntegerField(default=0)
    tableid = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='table', null=True)
    isitopen = models.BooleanField(default=0)
    date = models.CharField(max_length=200, default='')

    def get_total_sum(self):
        return sum(item.get_sum() for item in self.orderid.all())


class OrderContent(models.Model):
    order = models.ForeignKey(Order, related_name='meals', on_delete=models.CASCADE, null=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=True)
    count = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.meal.price * self.count


class Check(models.Model):
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order', null=True)
    servicefee = models.ForeignKey(ServicePercentage, on_delete=models.CASCADE, related_name='servicefee', null=True)
    date = models.CharField(max_length=100, default='')

    def get_total(self):
        return self.orderid.get_total_sum() * (1 + (self.servicefee.percentage / 100))
