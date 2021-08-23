from django import forms

from app_animals.models import Animals


class AnimalForm(forms.ModelForm):
    date_arrival = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y',
                                                          attrs={'class': 'datepicker', 'placeholder': 'Select a date',
                                                                 'type': 'date'}))

    class Meta:
        model = Animals
        fields = '__all__'
