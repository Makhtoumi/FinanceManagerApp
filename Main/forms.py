from django import forms
from .models import * 



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class BalanceForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['balance']  
        
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model = BalanceTransaction
        fields = ['amount', 'description']
        
class UnitForm(forms.ModelForm):
    class Meta: 
        model = Categorie
        fields = ['name']

class SouscategorieForm(forms.ModelForm):
    class Meta: 
        model = SousCategorie
        fields = ['name']