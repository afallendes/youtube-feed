from django import forms

class AddChannelForm(forms.Form):
    url = forms.URLField(label='Enter a Youtube channel', max_length=100)
