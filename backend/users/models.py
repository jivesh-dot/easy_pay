from django.contrib.auth.models import AbstractUser
from django.db import models


from core import models as core_models


class User(AbstractUser):
    pass


class Merchant(core_models.BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='merchant_profile')
    business_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"
