from django import forms

class NameForm(forms.Form):
	equipe1 = forms.CharField(label='Nom equipe 1', max_length=15)
	equipe2 = forms.CharField(label='Nom equipe 2', max_length=15)
	