from django.views.generic import View,ListView,CreateView
from django.urls import reverse_lazy
from .forms import DepositForm
from .models import Transaction
from pet.models import Pet
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404,reverse
from django.http import HttpResponseRedirect
from django.db import transaction

class TransactionViewMixin(LoginRequiredMixin,CreateView):
    template_name='transaction/deposit_form.html'
    model=Transaction
    title=''
    success_url=reverse_lazy('account')

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account,
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title':self.title
        })
        return context

class DepositMoneyView(TransactionViewMixin):
    form_class=DepositForm
    title='Deposit'

    def get_initial(self):
        initial = {'transaction_type': 'Deposit'}
        return initial
    
    def form_valid(self,form):
        try:
            amount=form.cleaned_data.get('amount')
            account=self.request.user.account
            account.balance += amount
            account.save(
                update_fields=['balance']
            )
            messages.success(self.request,f"{amount}$ was deposited to your account successfully")
            return super().form_valid(form)
        except Exception as e:
            print(f"An error occurred in form_valid: {e}")    


class AdoptPetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        pet = get_object_or_404(Pet, id=id)
        adopting_cost=pet.price

        if pet.adopter is not None and pet.adopter==request.user:
            messages.warning(request, "You have already adopted this pet.")
            return HttpResponseRedirect(reverse_lazy('pets'))
        if request.user.account.balance < adopting_cost:
            messages.error(self.request, "Insufficient balance to adopt the pet.")
            return HttpResponseRedirect(reverse_lazy('deposit'))

        if pet.adopter is not None:
            messages.warning(request, "Someone has already adopted this pet.")
            return HttpResponseRedirect(reverse('pets'))

        with transaction.atomic():
            pet.adopter = request.user
            pet.save()

            request.user.account.balance -= adopting_cost
            request.user.account.save(update_fields=['balance'])

            Transaction.objects.create(
                account=request.user.account,
                amount=adopting_cost,
                balance_after_transaction=request.user.account.balance,
                transaction_type='Pay',
            )

        messages.success(request, f"You have successfully adopted the pet: {pet.name}")
        return HttpResponseRedirect(reverse('account'))

class TransactionReportView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction/transaction_report.html'
    context_object_name = 'data'

    def get_queryset(self):
        return Transaction.objects.filter(account=self.request.user.account)

