from django import forms
from django.forms import ModelForm
from django.forms.widgets import DateInput
from .models import Schedule

class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['date','time', 'place', 'StudentNum','organization']
        widgets = {
            'date': forms.DateInput(attrs={'hidden':'hidden'}),
        }

class tSealForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['teacherSeal']

class aSealForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['affairsSeal']

class rSealForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['roomSeal']


class StateForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['state']
        widgets = {
            'state': forms.Select(attrs={'class':'forms','title':'使用状況'}),
        }