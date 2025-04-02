from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from .forms import ContactForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Homepage
def index(request):
    return render(request, 'contacts/index.html')


# Profile page
@login_required
def profile(request):
    contacts = Contact.objects.filter(user=request.user)
    return render(request, 'contacts/profile.html', {'contacts': contacts})

#List Contacts
@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user)
    query = request.GET.get('q')
    category = request.GET.get('category', 'all')
    contacts = Contact.objects.all()

    if query:
        contacts = contacts.filter(
            Q(name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(phone__icontains=query)
        )

    if category and category != "all":
        contacts = contacts.filter(category=category)

    # Pagination: Show 5 contacts per page
    paginator = Paginator(contacts, 5)  
    page_number = request.GET.get('page')
    contacts_page = paginator.get_page(page_number)

    return render(request, 'contacts/contact_list.html', {
        'contacts': contacts_page,
        'query': query,
        'category': category
    })


# Create Contact
@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/contact_form.html', {'form': form})


# Update Contact
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/contact_form.html', {'form': form, 'contact': contact})


# Delete Contact
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.delete()
        return redirect('contact_list')
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact})


