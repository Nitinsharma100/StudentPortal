from django import forms
from .models import*
from django.contrib.auth.forms import UserCreationForm

class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields=['title','description']
        
class DateInput(forms.DateInput):
    input_type='date'

class Homeworkform(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=['subject','title','description','due','is_finished']
        
class Dashboardform(forms.Form):
    text=forms.CharField(max_length=100,label="Enter Your Search")


class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','desc','is_finished']

class Conversionform(forms.Form):
    CHOICES=[('length','Length'),('mass','Mass')]
    measurement=forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)


class ConversionLengthform(forms.Form):
    CHOICES = [('yard', 'Yard'), ('foot', 'Foot')]
    
    input = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter the Number'})
    )
    measure1 = forms.CharField(
        label='From',
        widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='To',
        widget=forms.Select(choices=CHOICES)
    )

# Mass Conversion Form
class ConversionMassform(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    
    input = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter the Number'})
    )
    measure1 = forms.CharField(
        label='From',
        widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='To',
        widget=forms.Select(choices=CHOICES)
    )


class Userregistrationform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']