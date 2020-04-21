from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import *


class TablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class MealCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealsCategory
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class ServicePercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePercentage
        exclude = ('id',)


class MealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'


class OrderContentSerializer(serializers.ModelSerializer):
    mealsid = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all(), source='mealsid.id')
    name = serializers.CharField(source='mealsid.name', read_only=True)

    class Meta:
        model = OrderContent
        fields = ('mealsid', 'name', 'count')


class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all(), source='meal.id', )
    name = serializers.CharField(source='meal.name', read_only=True)
    price = serializers.CharField(source='meal.price', read_only=True)
    total = serializers.FloatField(source='get_cost', read_only=True)

    class Meta:
        model = OrderContent
        fields = ('id', 'name', 'count', 'price', 'total')


class OrdersSerializer(serializers.ModelSerializer):
    mealsid = OrderContentSerializer(many=True, required=False, source='orderid')
    tableid = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all())
    tablename = serializers.CharField(source='tableid.name', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'waiterid', 'tableid', 'tablename', 'isitopen', 'date', 'mealsid')


class MealsInCheckSerializer(serializers.ModelSerializer):
    meals_order = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('meals_order',)


class CheckSerializer(serializers.ModelSerializer):
    orderid = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), source='orderid.id')
    servicefee = serializers.FloatField(source='servicefee.percentage', read_only=True)
    meals = MealsInCheckSerializer(many=True, required=False)
    totalsum = serializers.FloatField(source='get_total', read_only=True)

    class Meta:
        model = Check
        fields = ['id', 'orderid', 'date', 'servicefee', 'totalsum', 'meals']


class RegistrationSerializer(serializers.ModelSerializer):
    roleid = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role.id'
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )


token = serializers.CharField(max_length=255, read_only=True)


class Meta:
    model = User
    fields = ['roleid', 'name', 'surname', 'email', 'created_at', 'token', 'phone']
    read_only_fields = ('create_at', 'token')


def create(self, validated_data):
    username = validated_data['name'] + "_user"
    password = validated_data['phone']
    return User.objects.create_user(
        role=validated_data.pop('role')['id'],
        username=username,
        password=password,
        **validated_data
    )


class LoginSerializer(serializers.Serializer):
    role_id = serializers.IntegerField(
        source='role.id',
        read_only=True
    )
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This user has been deactivated."
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('role', 'name', 'surname', 'email', 'username', 'created_at', 'password', 'token')
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
