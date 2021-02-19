from django import forms
from django.core.validators import FileExtensionValidator

from .models import Teacher


class UploadFileForm(forms.Form):
    names = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    images = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['zip'])])

    def clean(self):
        pass


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
