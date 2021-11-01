from django.contrib.auth import models
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,BooleanField,TextField,
    EmailField,TextChoices
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for djvideomem.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    stripe_customer_id = CharField(max_length=50)
    is_member = BooleanField(default=False)
    is_minister = BooleanField(default=False)
    is_ministry = BooleanField(default=False)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


