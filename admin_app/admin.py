import os
import tempfile

from django.shortcuts import render
from django.urls import path
from docxtpl import DocxTemplate
from openpyxl import Workbook

from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin.models import LogEntry

from .models import Order, Task, Supplies, Client, Engineer, Motorcycle, Work, Supply, User


def print_order(modeladmin, request, queryset):
    for obj in queryset:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = (f'attachment; filename=order'
                                           f'_{obj.motorcycle.model}'
                                           f'_{obj.client.user.first_name}'
                                           f'_{obj.client.user.last_name}.docx')
        full_task_price = sum([task.work.price * task.count for task in obj.tasks.all()])
        full_supply_price = sum([supply.supply.price * supply.count for supply in obj.supplies.all()])
        context = {
            'client': obj.client,
            'motorcycle': obj.motorcycle,
            'tasks': obj.tasks.all(),
            'supplies': obj.supplies.all(),
            'full_task_price': full_task_price,
            'full_task_price_with_discount': full_task_price * (1 - obj.task_discount / 100),
            'full_supply_price': full_supply_price,
            'full_supply_price_with_discount': full_supply_price * (1 - obj.supply_discount / 100),
            'deposit': obj.deposit,
            'full_price_with_discount': (full_task_price * (1 - obj.task_discount / 100)) +
                                        (full_supply_price * (1 - obj.supply_discount / 100)),
            'full_price_with_deposit': round((full_task_price * (1 - obj.task_discount / 100)) +
                                             (full_supply_price * (1 - obj.supply_discount / 100)) - obj.deposit, 2),
            'number': obj.number,
            'created_at': obj.created_at.date(),

        }
        file = DocxTemplate('templates/template.docx')
        file.render(context)
        file.save(response)

    return response


def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={modeladmin.model._meta}.xlsx'

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
    extra = 0
    autocomplete_fields = ['supply']


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    autocomplete_fields = ['work', 'engineer']


class ClientAdmin(admin.ModelAdmin):
    actions = [export_to_excel]
    search_fields = ['user__first_name', 'user__last_name']
    list_display = ['get_user_name', 'get_user_phone_number']

    def get_user_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    get_user_name.short_description = 'Name'

    def get_user_phone_number(self, obj):
        return obj.user.phone_number

    get_user_phone_number.short_description = 'Phone Number'


class EngineerAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name']
    actions = [export_to_excel]


class MotorcycleAdmin(admin.ModelAdmin):
    actions = [export_to_excel]
    search_fields = ['name']
    list_display = ['name', 'model', 'owner', 'mfg_year', 'state_number', 'vin']


class OrderAdmin(admin.ModelAdmin):
    change_form_template = 'admin_app/order_change_form.html'
    autocomplete_fields = ['client', 'engineers', 'motorcycle']
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        order = Order.objects.get(pk=object_id)
        extra_context['total_work_price'] = sum(task.work.price * task.count for task in order.tasks.all())
        extra_context['total_work_price_with_discount'] = (extra_context['total_work_price'] *
                                                           (1 - order.task_discount / 100))
        extra_context['total_supply_price'] = sum(
            supply.supply.price * supply.count for supply in order.supplies.all())
        extra_context['total_supply_price_with_discount'] = (extra_context['total_supply_price'] *
                                                             (1 - order.supply_discount / 100))
        extra_context['total_price_with_discount'] = (extra_context['total_work_price_with_discount'] +
                                                      extra_context['total_supply_price_with_discount'])

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    inlines = [
        TaskInline,
        SuppliesInline,
    ]
    list_display = ['number', 'created_at', 'client', 'engineers', 'motorcycle', 'status']
    list_filter = ['status', 'engineers']
    search_fields = ['number', 'client__user__first_name', 'engineers__user__first_name',
                     'motorcycle__vin', 'motorcycle__state_number']
    exclude = ['number', ]

    actions = [export_to_excel, print_order]


class SupplyAdmin(admin.ModelAdmin):
    actions = [export_to_excel]
    list_display = ['name', 'price']
    search_fields = ['name']


class UserAdmin(admin.ModelAdmin):
    actions = [export_to_excel]


class WorkAdmin(admin.ModelAdmin):
    actions = [export_to_excel]
    list_display = ['name', 'price']
    search_fields = ['name']


class LogAdmin(admin.ModelAdmin):
    list_display = ["action_time", "user", "content_type", "action_flag", "object_repr", "change_message"]
    search_fields = ["object_repr", "change_message"]
    list_filter = ["user", "action_flag", "content_type"]


admin.site.register(Client, ClientAdmin)
admin.site.register(Engineer, EngineerAdmin)
admin.site.register(Motorcycle, MotorcycleAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(LogEntry, LogAdmin)
