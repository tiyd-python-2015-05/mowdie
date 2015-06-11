from django import forms
from updates.models import Update


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = ('text',)