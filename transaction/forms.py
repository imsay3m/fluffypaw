from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['amount','transaction_type']
    def __init__(self,*args,**kwargs):
        self.account=kwargs.pop('account')
        super().__init__(*args,**kwargs)
        self.fields['transaction_type'].disabled=True #this field will be disabled
        self.fields['transaction_type'].widget=forms.HiddenInput() #it will be hidden from user
    
    def save(self,commit=True):
        try:
            self.instance.account=self.account
            self.instance.balance_after_transaction=self.account.balance
            return super().save()
        except Exception as e:
            print(f"Error in save function: {e}")


class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount=100
        amount=self.cleaned_data.get('amount')
        if amount<min_deposit_amount:
            raise forms.ValidationError(
                f"You need to deposit at least {min_deposit_amount} $"
            )
        return amount