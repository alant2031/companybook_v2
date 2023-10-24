from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Subscriber, Category, Company
from .forms import SubscriberForm


class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.unregister(User)


@admin.register(User)
class GPUserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))

        for fieldset in fieldsets:
            fieldset[1]["fields"] = tuple(
                filter(
                    lambda f: f not in ("is_superuser", "user_permissions"),
                    fieldset[1]["fields"],
                )
            )
        return fieldsets

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_staff:
            return qs.filter(is_superuser=False)
        else:
            return qs.none()


@admin.register(Subscriber)
class SubscriberAdmin(BaseAdmin):
    search_fields = ["company__name"]
    exclude = ("user",)
    list_display = ("company", "in_charge", "active", "user")
    form = SubscriberForm


@admin.register(Company)
class CompanyAdmin(BaseAdmin):
    search_fields = ["name", "razao"]
    exclude = ("active", "user")
    list_display = ("razao", "document", "uf", "tel1", "user")

    def get_queryset(self, request):
        qs = super(CompanyAdmin, self).get_queryset(request)
        if (
            request.user.is_superuser
            or request.user.groups.filter(name="jedi").exists()
        ):
            return qs

        return qs.filter(user=request.user)


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    exclude = ("active", "user")
    list_display = ("name", "user", "createdAt")
