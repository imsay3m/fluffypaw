from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Pet,Category
from django.views.generic import DetailView,ListView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import ReviewForm,PetCreateForm
from django.contrib import messages
# Create your views here.
class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetCreateForm
    template_name = 'pet/add_pets.html' 
    success_url = reverse_lazy('pets') 

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class PetListView(ListView):
    model = Pet
    template_name = 'pet/pets.html'
    context_object_name = 'pets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        return queryset


class PetDetailsView(DetailView):
    model = Pet
    template_name = 'pet/pet_details.html'
    context_object_name = 'pet'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = self.object
        reviews = pet.reviews.all()
        review_form = ReviewForm()
        context["form"] = review_form
        context["reviews"] = reviews
        return context

    def post(self, request, *args, **kwargs):
        pet = self.get_object()
        form = ReviewForm(request.POST)

        if form.is_valid():
            user = request.user
            if user.is_authenticated:
                form.instance.user = user
                form.instance.pet = pet
                form.save()
                messages.success(request, "You have successfully submitted the review.")
                return HttpResponseRedirect(reverse_lazy('pet_details', kwargs={'id': pet.id}))
            else:
                messages.error(request, "You need to be logged in to submit a review.")
        return self.get(*args, **kwargs)
