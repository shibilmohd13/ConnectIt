from django import forms
from App.models import Customer

class Customerform(forms.ModelForm):
    file = forms.FileField(required=False)
    class Meta:
        model = Customer
        fields = "__all__"

# Reply mails
class EmailForm(forms.Form):
    email = forms.EmailField(required=True)
    cc = forms.EmailField(required=False)
    subject = forms.CharField(max_length=100)
    attach = forms.FileField(required=False)
    message = forms.CharField(required=True, widget=forms.Textarea)

