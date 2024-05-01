from rest_framework import serializers
from .models import Order, Motorcycle, Work, Task, Supply, Supplies


class MotorcycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorcycle
        fields = ('model', 'mfg_year', 'vin', 'state_number')


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('name', 'price')


class TaskSerializer(serializers.ModelSerializer):
    work = WorkSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('work', 'count', 'status', 'created_at')


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = ('name', 'price')


class SuppliesSerializer(serializers.ModelSerializer):
    supply = SupplySerializer(read_only=True)

    class Meta:
        model = Supplies
        fields = ('supply', 'count')


class OrderSerializer(serializers.ModelSerializer):
    motorcycle = MotorcycleSerializer(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    supplies = SuppliesSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('motorcycle', 'created_at', 'status', 'tasks', 'supplies')
