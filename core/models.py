import uuid
import re
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from stdimage import JPEGField
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .utils.index import set_key

ESTADO_CHOICES = (
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins"),
)


# CUSTOM FIELDS
class UsernameField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 32
        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        value = super().clean(value, model_instance)
        if not re.match(r"[a-zA-Z]+[a-zA-Z_0-9]*$", value):
            raise ValidationError(
                "Username deve iniciar com uma letra. Não deve ter acentuação e pode conter números ou underscore _"  # noqa
            )

        if len(value) < 6:
            raise ValidationError(
                "Username muito curto. Mínimo de 6 caracteres"
            )
        return value


class PhoneField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 14
        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        value = super().clean(value, model_instance)

        # Check if the phone number matches the allowed formats
        if not re.match(
            r"^\((?:1[1-9]|9[1-9]|[2-8][0-9])\)(?:9\d{8}|\d{8})$", value
        ):
            raise ValidationError(
                "Formato Inválido. Use (xx)xxxxxxxx ou (xx)9xxxxxxxx."
            )

        return value


class DocumentField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 14
        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        value = super().clean(value, model_instance)

        if not value.isdigit():
            raise ValidationError("Apenas dígitos numéricos.")

        return value


# MODELS
class Base(models.Model):
    user = models.ForeignKey(
        get_user_model(), verbose_name="Autor(a)", on_delete=models.PROTECT
    )
    createdAt = models.DateField("Data de criação", auto_now_add=True)
    updatedAt = models.DateField("Data de atualização", auto_now=True)
    active = models.BooleanField("Ativo?", default=True)

    class Meta:
        abstract = True


class Company(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Nome", max_length=40)
    razao = models.CharField("Razao Social", max_length=100, unique=True)
    document = DocumentField(
        "Nº Documento",
        max_length=14,
        unique=True,
        help_text="CNPJ ou CPF. Apenas dígitos.",
    )
    is_cpf = models.BooleanField("CPF?", default=False)
    email = models.EmailField("Email", max_length=100)
    tel1 = PhoneField(
        "Telefone 1", help_text="Ex: (85)988887777 ou (85)32221111."
    )
    uf = models.CharField("Estado", choices=ESTADO_CHOICES, max_length=3)
    cidade = models.CharField("Cidade", max_length=20)
    tel2 = PhoneField("Telefone 2", blank=True)
    endereco = models.CharField("Endereço", max_length=200, blank=True)
    categoria1 = models.ForeignKey(
        "core.Category",
        on_delete=models.PROTECT,
        related_name="category1_set",
    )
    categoria2 = models.ForeignKey(
        "core.Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="category2_set",
    )

    class Meta:
        verbose_name = "Entidade"
        verbose_name_plural = "Entidades"

    def clean(self):
        if self.is_cpf:
            if len(self.document) != 11:
                raise ValidationError("CPF precisa de 11 dígitos")
        else:
            if len(self.document) != 14:
                raise ValidationError("CNPJ precisa de 14 dígitos")

        super().clean()

    def __str__(self):
        return self.razao[:30]


class Subscriber(Base):
    company = models.OneToOneField(
        "core.Company", verbose_name="Entidade", on_delete=models.PROTECT
    )
    in_charge = models.CharField("Responsável", max_length=20)
    desc = models.TextField("Descrição", max_length=500, blank=True)
    opening_h = models.CharField(
        "Horário funcionamento", max_length=100, blank=True
    )
    opening_d = models.DateField("Data de aberura", null=True, blank=True)
    wpp = models.URLField("Whatsapp", max_length=200, blank=True)
    website = models.URLField("Site", max_length=100, blank=True)
    instagram = models.URLField("Instagram", max_length=200, blank=True)
    facebook = models.URLField("Facebook", max_length=200, blank=True)
    iframe = models.CharField("Iframe Google Maps", max_length=600, blank=True)
    ytb_id = models.CharField("Youtube ID", max_length=16, blank=True)
    username = UsernameField(
        max_length=30,
        unique=True,
    )
    logo = JPEGField(
        upload_to="logos/",
        delete_orphans=True,
        help_text="Max size 200KB",
    )
    photo1 = JPEGField(
        upload_to="photos/",
        delete_orphans=True,
        blank=True,
        help_text="Max size 500KB",
    )
    photo2 = JPEGField(
        upload_to="photos/",
        delete_orphans=True,
        blank=True,
        help_text="Max size 500KB",
    )
    photo3 = JPEGField(
        upload_to="photos/",
        delete_orphans=True,
        blank=True,
        help_text="Max size 500KB",
    )
    photo4 = JPEGField(
        upload_to="photos/",
        delete_orphans=True,
        blank=True,
        help_text="Max size 500KB",
    )

    obs = models.CharField("Observações", max_length=120, blank=True)

    def __str__(self):
        return f"Assinante {self.company.name[:30]}"

    class Meta:
        verbose_name = "Assinante"
        verbose_name_plural = "Assinantes"


class Category(Base):
    name = models.CharField("Nome", max_length=20, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


# SIGNALS
@receiver(pre_save, sender=Company)
@receiver(pre_save, sender=Category)
def set_uppercase(sender, instance, **kwargs):
    instance.name = instance.name.upper()

    if hasattr(instance, "razao"):
        instance.razao = instance.razao.upper()


@receiver(pre_save, sender=Subscriber)
def set_pathfile(sender, instance, **kwargs):
    instance.username = instance.username.lower()
    set_key(instance, "logo", Subscriber)
    for i in range(4):
        photo_key = "photo" + str(i + 1)
        if bool(getattr(instance, photo_key)):
            set_key(instance, photo_key, Subscriber)
