from django import forms
from .models import PasswordEntry

class PasswordEntryForm(forms.ModelForm):
    plain_password = forms.CharField(
        label="Password",
        required=False,
        widget=forms.PasswordInput(
            render_value=True,
            attrs={
                'id': 'id_plain_password',
                'placeholder': 'Enter password'
            }
        )
    )

    class Meta:
        model = PasswordEntry
        fields = ['site_name', 'site_url', 'username', 'notes']

    def __init__(self, *args, **kwargs):
        self.master_password = kwargs.pop('master_password', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.master_password:
            try:
                self.fields['plain_password'].initial = self.instance.get_password(self.master_password)
            except Exception:
                self.fields['plain_password'].initial = '[Could not decrypt]'

    def save(self, commit=True):
        entry = super().save(commit=False)
        if commit:
            entry.save()
        return entry
