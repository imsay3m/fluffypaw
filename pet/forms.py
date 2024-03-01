from django import forms
from .models import Review,Pet
class PetCreateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'description', 'date_of_birth', 'image', 'price', 'categories']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.added_by = kwargs.pop('added_by', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.added_by = self.added_by
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'rows': '3'})

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        pet = cleaned_data.get('pet')

        if user and pet:
            if user != pet.adopter:
                raise forms.ValidationError("Only the adopter of the pet can write a review.")

        return cleaned_data

