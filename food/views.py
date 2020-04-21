import json

from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, filters, status
from .models import *
from .serializers import *
from .renderers import UserJSONRenderer


class TablesListView(APIView):
    serializer_class = TablesSerializer
    queryset = Table.objects.all()

    def get(self, request):
        tables = Table.objects.all()
        serializer = TablesSerializer(tables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = TablesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = json.loads((request.body).decode("utf-8"))
        Table.objects.filter(id=data['id']).delete()
        return Response(status=status.HTTP_201_CREATED)


class RolesListView(APIView):
    queryset = Role.objects.all()
    serializer_class = RolesSerializer

    def get(self, request):
        roles = Role.objects.all()
        serializer = RolesSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = RolesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = json.loads((request.body).decode("utf-8"))
        Role.objects.filter(id=data['id']).delete()
        return Response(status=status.HTTP_201_CREATED)


class DepartmentsListView(APIView):
    serializer_class = DepartmentsSerializer
    queryset = Department.objects.all()

    def get(self, request):
        department = Department.objects.all()
        serializer = DepartmentsSerializer(department, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = DepartmentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = json.loads((request.body).decode("utf-8"))
        Department.objects.filter(id=data['id']).delete()
        return Response(status=status.HTTP_201_CREATED)


class MealCategoriesListView(APIView):
    serializer_class = MealCategoriesSerializer
    queryset = MealsCategory.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['departmentid__name', ]

    def get(self, request):
        meal_category = MealsCategory.objects.all()
        serializer = MealCategoriesSerializer(meal_category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = MealCategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = json.loads((request.body).decode("utf-8"))
        MealsCategory.objects.filter(id=data['id']).delete()
        return Response(status=status.HTTP_201_CREATED)


class MealCategoriesByDepartmentListView(APIView):

    def get(self, request, id):
        obj = MealsCategory.objects.filter(departmentid=id)
        serializer = MealCategoriesSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatusListView(APIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

    def get(self, request):
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = json.loads((request.body).decode("utf-8"))
        Status.objects.filter(id=data['id']).delete()
        return Response(status=status.HTTP_201_CREATED)


class ServicePercentageListView(APIView):
    serializer_class = ServicePercentageSerializer
    queryset = ServicePercentage.objects.all()
    def get(self, request):
        percentage = ServicePercentage.objects.all()
        serializer = ServicePercentageSerializer(percentage, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ServicePercentageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = json.loads((request.body).decode("utf-8"))
        ServicePercentage.objects.filter(id=data['id']).delete()
        return Response(status=status.HTTP_201_CREATED)


class MealsListView(APIView):
    serializer_class = MealsSerializer
    queryset = Meal.objects.all()

    def get(self, request):
        serializer = MealsSerializer(Meal.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MealsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = json.loads((request.body).decode("utf-8"))
        obj = Meal.objects.filter(id=data['id'])
        obj.update(name=data['name'], price=data['price'], description=data['description'])

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        data = json.loads((request.body).decode("utf-8"))
        Meal.objects.filter(id=data['id']).delete()

        return Response(status=status.HTTP_201_CREATED)


class MealsByCategoryListView(APIView):
    def get(self, request, id):
        obj = Meal.objects.filter(categoryid=id)
        serializer = MealsSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrdersListView(APIView):
    serializer_class = OrdersSerializer
    queryset = Order.objects.all()

    def get(self, request):
        order = Order.objects.all()
        serializer = OrdersSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrdersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = json.loads((request.body).decode("utf-8"))
        Order.objects.filter(id=data['id']).delete()

        return Response(status=status.HTTP_201_CREATED)


class ActiveOrdersListView(APIView):
    def get(self, request):
        orders = Order.objects.filter(isitopen=1)
        serializer = OrdersSerializer(orders, many=True)

        return Response(serializer.data)


class MealsToOrderListView(APIView):
    def get(self, request):
        order = Order.objects.filter(id=request.data['orderid'])
        serializer = OrdersSerializer(order, many=True)
        return Response(serializer.data)

    def post(self, request):
        order = Order.objects.filter(id=request.data['orderid'])
        data = request.data['meals']
        meal = OrderContent.objects.filter(id=data['id'])
        OrderContent.objects.create(order=order, meal=meal, count=data['count'])

    def delete(self, request):
        data = request.data
        order = Order.objects.filter(id=request.data['orderid'])
        meal = Order.objects.filter(id=data['meaidid'])


class CheckListView(APIView):
    serializer_class = CheckSerializer
    queryset = Check.objects.all()

    def get(self, request):
        checks = Check.objects.all()
        serializer = CheckSerializer(checks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        data = json.loads((request.body).decode("utf-8"))
        Check.objects.filter(id=data['id']).delete()

        return Response(status=status.HTTP_201_CREATED)


class ActiveOrderListView(APIView):
    def get(self, request):
        orders = Order.objects.filter(isitopen=1)
        serializer = OrdersSerializer(orders, many=True)

        return Response(serializer.data)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer

    def retrieve(self, request):
        serializer = UserSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request):
        serializer_data = request.data.get('user')

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)