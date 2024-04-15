from django.utils import timezone
from django.db import models


class User(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Client(models.Model):
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="UserList"
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Engineer(models.Model):
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        choices=(
            ("work", "Работает"),
            ("not_work", "Не работает"),
        ),
        default="work",
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
    mfg_year = models.IntegerField()
    vin = models.CharField(max_length=100)
    state_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.state_number}"


class Work(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Supply(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    number = models.CharField(max_length=20, default=None)
    created_at = models.DateTimeField(default=timezone.now)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="ClientList"
    )
    engineers = models.ManyToManyField(
        Engineer
    )
    motorcycle = models.ForeignKey(
        Motorcycle,
        on_delete=models.CASCADE,
        related_name="Motorcycle"
    )
    deposit = models.FloatField(default=0, verbose_name="Предоплата (Руб.):")
    task_discount = models.FloatField(default=0, verbose_name="Скидка на работы (%):")
    supply_discount = models.FloatField(default=0, verbose_name="Скидка на запчасти (%):")
    description = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    status = models.CharField(
        choices=(
            ("in_queue", "В очереди"),
            ("in_progress", "В работе"),
            ("ready", "Готов")
        ),
        default="in_queue",
        max_length=100
    )

    def save(self, *args, **kwargs):
        if not self.number:
            last_object = Order.objects.last()
            last_id = last_object.id if last_object else 0
            self.number = f"24-{last_id + 99:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.number


class Task(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE
    )
    count = models.FloatField(default=1)
    status = models.CharField(
        choices=(
            ("in_queue", "В очереди"),
            ("in_progress", "В работе"),
            ("awaiting_approval", "На согласовании"),
            ("waiting_for_delivery", "Ожидает поставку"),
            ("ready", "Готов")
        ),
        default="in_queue",
        max_length=100
    )

    def __str__(self):
        return self.work.name


class Supplies(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    supply = models.ForeignKey(
        Supply,
        on_delete=models.CASCADE
    )
    count = models.FloatField(default=1)

    def __str__(self):
        return f"{self.supply.name} - {self.count}"



