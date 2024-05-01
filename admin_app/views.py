from rest_framework import generics
from rest_framework.response import Response

from .models import User, Order, Client


from django.shortcuts import get_object_or_404

from .serializers import OrderSerializer


class ClientOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        phone_number = self.kwargs['phone_number']
        client = get_object_or_404(Client, user__phone_number=phone_number)
        return Order.objects.filter(client=client)