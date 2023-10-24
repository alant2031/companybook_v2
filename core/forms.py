from django import forms
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        logo = cleaned_data.get("logo", False)
        if logo:
            logo_max_size = 200  # Maximum size in kilobytes
            max_size_bytes = logo_max_size * 1024  # Convert to bytes
            if logo.size > max_size_bytes:
                self.add_error(
                    "logo",
                    f"The image size exceeds the maximum allowed size of {logo_max_size}KB.",  # noqa
                )
        for i in range(4):
            photo_key = "photo" + str(i + 1)
            photo = cleaned_data.get(photo_key, False)
            if photo:
                photo_max_size = 500
                max_size_bytes = photo_max_size * 1024  # Convert to bytes
                if photo.size > max_size_bytes:
                    self.add_error(
                        photo_key,
                        f"The image size exceeds the maximum allowed size of {photo_max_size}KB.",  # noqa
                    )

        return cleaned_data
