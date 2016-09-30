from django import forms

class PressReleaseURLForm(forms.Form):
    press_release_url = forms.URLField(label='Press Release URL', initial='http://', required=True)