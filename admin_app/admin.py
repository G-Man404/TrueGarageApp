from django.contrib import admin
from .models import Engineer, Client, Motorcycle, Order, Work

admin.site.register(Engineer)
admin.site.register(Client)
admin.site.register(Motorcycle)
admin.site.register(Work)


class WorkInline(admin.TabularInline):
    model = Order.works.through
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [WorkInline]


admin.site.register(Order, OrderAdmin)
