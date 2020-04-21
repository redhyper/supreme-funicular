from django.urls import path
from django.conf.urls import url
from food import views
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('table/', views.TablesListView.as_view()),
    #path('role', views.RoleListView.as_view()),
    path('department', views.DepartmentsListView.as_view()),
    path('categories', views.MealCategoriesListView.as_view()),
    path('status', views.StatusListView.as_view()),
    path('service', views.ServicePercentageListView.as_view()),
    path('meal', views.MealsListView.as_view()),
    path('check', views.CheckListView.as_view()),
    path('order', views.OrdersListView.as_view()),
    path('active_orders/', views.ActiveOrderListView.as_view()),
    path('users', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('user', UserRetrieveUpdateAPIView.as_view()),
]