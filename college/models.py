from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from core.time_utils import n_days_from_now


class College(models.Model):
    price = models.IntegerField(default=60_000)
    is_open = models.BooleanField(default=True)
    open_at = models.DateTimeField(default=timezone.now)
    close_at = models.DateTimeField(default=n_days_from_now(60))
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    is_hidden = models.BooleanField(default=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    @property
    def is_free(self) -> bool:
        return self.price == 0

    def has_member(self, user) -> bool:
        return self.users.filter(user=user).exists()

    def add_member(self, user) -> tuple[str, bool]:
        with transaction.atomic():
            if user.balance >= self.price:
                user.balance -= self.price
                self.users.add(user)
                self.save()
                return 'registered successfully', True

        return 'you have insufficient balance', False


class Lesson(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_hidden = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    text = models.TextField()
