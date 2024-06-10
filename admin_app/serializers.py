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
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('work', 'count', 'status', 'created_at')

    def get_status(self, obj):
        return obj.get_status_display()


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
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('motorcycle', 'status', 'number')

    def get_status(self, obj):
        return obj.get_status_display()


class ByNumberSerializer(serializers.ModelSerializer):
    motorcycle = MotorcycleSerializer(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    supplies = SuppliesSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('motorcycle', 'created_at', 'status', 'tasks', 'supplies', 'number')

    def get_status(self, obj):
        return obj.get_status_display()