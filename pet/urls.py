from django.urls import path

from transaction.views import AdoptPetView
from .views import PetCreateView, PetDetailsView, PetListView

urlpatterns = [
    path('',PetListView.as_view(),name='pets'),
    path('add/',PetCreateView.as_view(),name='add_pet'),
    path('<slug:category_slug>/', PetListView.as_view(), name='pet_list_by_category'),
    path('details/<int:id>/', PetDetailsView.as_view(), name='pet_details'),
    path('adopt/<int:id>',AdoptPetView.as_view(),name='adopt_pet'),
]
