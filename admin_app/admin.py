from django.contrib import admin
from .models import User, Engineer, Client, Motorcycle, Order, Work, Supplies, Supply, Task

admin.site.register(Engineer)
admin.site.register(Client)
admin.site.register(Motorcycle)
admin.site.register(Work)
admin.site.register(User)
admin.site.register(Supplies)
admin.site.register(Supply)
admin.site.register(Task)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', "client", "engineer", "motorcycle")
    list_filter = ('client', 'engineer')
    exclude = ('number',)


admin.site.register(Order, OrderAdmin)
