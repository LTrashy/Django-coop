from decimal import DefaultContext
import random
import string
from tabnanny import verbose

from autoslug import AutoSlugField
import autoslug
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries import CountryField
from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class PropertyPublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(PropertyPublishedManager, self)
            .get_queryset()
            .filter(published_status=True)
        )


class Property(TimeStampedUUIDModel):
    class AdveertType(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        FOR_RENT = "For Rent", _("For Rent")
        AUCTION = "Auction", _("Auction")

    class PropertyType(models.TextChoices):
        HOUSE = "House", ("House")
        APARTMENT = "Apartment", ("Apartment")
        OFFICE = "Office", ("Office")
        WAREHOUSE = "Warehouse", ("Warehouse")
        COMMERCIAL = "Commercial", ("Commercial")
        OTHER = "Other", ("Other")

    user = models.ForeignKey(
        User,
        verbose_name=_("Agent,Seller or Buyer"),
        related_name="agent_buyer",
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(
        verbose_name=_("Property Title"),
        max_length=250,
    )
    slug = AutoSlugField(
        populate_from="title",
        unique=True,
        always_update=True,
    )
    ref_code = models.CharField(
        verbose_name=_("Property Reference Code"),
        max_length=255,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        default="Default description...update me please...",
    )
    country = CountryField(
        verbose_name=_("Country"),
        default="CO",
        blank_label="(select country)",
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Bogota",
    )
    postal_code = models.CharField(
        verbose_name=_("Postal Code"),
        max_length=100,
        default="110111",
    )
    street_address = models.CharField(
        verbose_name=_("Street Adress"),
        max_length=150,
        default="AV68",
    )
    property_number = models.IntegerField(
        verbose_name=_("Property Number"),
        validators=[MinValueValidator(1)],
        default=112,
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=8,
        decimal_places=2,
        default=0.0,
    )
    tax = models.DecimalField(
        verbose_name=_("Property Tax"),
        max_digits=6,
        decimal_places=2,
        default=0.15,
        help_text="15% property tax charged",
    )
    plot_area = models.DecimalField(
        verbose_name=_("Plot Area(m^2)"),
        max_digits=8,
        decimal_places=2,
        default=0.0,
    )
    total_floors = models.IntegerField(
        verbose_name=_("Number of floors"),
        default=0,
    )
    bedrooms = models.IntegerField(
        verbose_name=_("Bedrooms"),
        default=1,
    )
    bathrooms = models.DecimalField(
        verbose_name=_("Bathrooms"),
        max_digits=4,
        decimal_places=2,
        default=1.0,
    )
