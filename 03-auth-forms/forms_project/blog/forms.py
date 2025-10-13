from django import forms
from .models import Comment


# 1. A simple standalone form (not tied to model)
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not email.endswith('@example.com'):
            raise forms.ValidationError("Please use an @example.com email.")
        return email


# 2. A ModelForm for comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
        # you can supply custom widgets, labels, help_texts, error_messages, etc.
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if "spam" in text.lower():
            raise forms.ValidationError("Spam content is not allowed.")
        return text
