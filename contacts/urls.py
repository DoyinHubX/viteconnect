from django.urls import path
from .views import index, contact_list, add_contact, edit_contact, delete_contact, profile

urlpatterns = [
    path('', index, name='index'),
    path('contact_list/', contact_list, name='contact_list'),
    path('accounts/profile/', profile, name='profile'),
    path('add/', add_contact, name='add_contact'),
    path('edit/<int:pk>/', edit_contact, name='edit_contact'),
    path('delete/<int:pk>/', delete_contact, name='delete_contact'),
]


