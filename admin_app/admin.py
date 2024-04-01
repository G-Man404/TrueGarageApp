from django.contrib import admin
from .models import Order, Task, Supplies, Client, Engineer, Motorcycle, Work, Supply, User


class SuppliesInline(admin.TabularInline):
    model = Supplies
    extra = 1


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline,
        SuppliesInline,
    ]
    list_display = ['number', 'created_at', 'client', 'engineer', 'motorcycle', 'status']
    list_filter = ['status']


admin.site.register(Order, OrderAdmin)
admin.site.register(Client)
admin.site.register(Engineer)
admin.site.register(Motorcycle)
admin.site.register(Work)
admin.site.register(Supply)
admin.site.register(User)
