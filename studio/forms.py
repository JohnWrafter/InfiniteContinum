from django import forms

from studio.models import MemberInquiry


class MemberInquiryForm(forms.ModelForm):
    class Meta:
        model = MemberInquiry
        fields = ["name", "email", "focus"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "focus": forms.Select(),
        }