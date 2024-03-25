from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    description = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(default=None)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Engineer(models.Model):
    description = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        choices=(
            ("works", "Работает"),
            ("on_holiday", "В отпуске"),
            ("medical_leave", "На больничном")
        ),
        max_length=100
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Motorcycle(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    vin = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Work(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        choices=(
            ("at_work", "В работе"),
            ("waiting_to_start", "Ожидает начала"),
            ("waiting_to_details", "Ожидает детали"),
            ("requires_clarification", "Требует уточнения деталий")
        ),
        max_length=100
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    engineer = models.ForeignKey(
        Engineer,
        on_delete=models.CASCADE
    )
    motorcycle = models.ForeignKey(
        Motorcycle,
        on_delete=models.CASCADE
    )
    works = models.ManyToManyField(
        Work
    )

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
