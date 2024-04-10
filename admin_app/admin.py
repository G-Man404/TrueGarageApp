from openpyxl import Workbook
from django.contrib import admin
from django.http import HttpResponse

from .models import Order, Task, Supplies, Client, Engineer, Motorcycle, Work, Supply, User


def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{modeladmin.model._meta}.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.append([field.verbose_name for field in modeladmin.model._meta.fields])  # заголовки столбцов

    for obj in queryset:
        row = []
        for field in modeladmin.model._meta.fields:
            value = getattr(obj, field.name)
            if callable(value):
                value = value()
            row.append(str(value))
        ws.append(row)

    wb.save(response)
    return response


class SuppliesInline(admin.TabularInline):
    model = Supplies
    extra = 1


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    actions = [export_to_excel]
    list_display = ['get_user_name', 'get_user_phone_number']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_user_name.short_description = 'Name'

    def get_user_phone_number(self, obj):
        return obj.user.phone_number
    get_user_phone_number.short_description = 'Phone Number'


class EngineerAdmin(admin.ModelAdmin):
    actions = [export_to_excel]


class MotorcycleAdmin(admin.ModelAdmin):
    actions = [export_to_excel]
    list_display = ['name', 'model', 'owner', 'mfg_year', 'state_number', 'vin']


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline,
        SuppliesInline,
    ]
    list_display = ['number', 'created_at', 'client', 'engineer', 'motorcycle', 'status']
    list_filter = ['status']
    exclude = ["number", ]

    actions = [export_to_excel]


class SupplyAdmin(admin.ModelAdmin):
    actions = [export_to_excel]
    list_display = ['name', 'price']


class UserAdmin(admin.ModelAdmin):
    actions = [export_to_excel]


class WorkAdmin(admin.ModelAdmin):
    actions = [export_to_excel]
    list_display = ['name', 'price']


admin.site.register(Client, ClientAdmin)
admin.site.register(Engineer, EngineerAdmin)
admin.site.register(Motorcycle, MotorcycleAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Work, WorkAdmin)
