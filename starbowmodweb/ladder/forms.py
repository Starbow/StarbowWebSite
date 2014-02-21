from django import forms
from starbowmodweb.ladder.models import CrashReport
from django.core.exceptions import ValidationError


class CrashReportForm(forms.ModelForm):
    class Meta:
        model = CrashReport
        fields = ['client_version', 'os', 'description', 'dump']

    def clean_dump(self):
        dump = self.cleaned_data.get('dump', False)
        if dump:
            if dump._size > 204800:
                raise ValidationError("No way the dump is more than 200kb. Did you pick the right file?")
            return dump

        else:
            raise ValidationError("Couldn't find an attached dump. Did you select one?")


