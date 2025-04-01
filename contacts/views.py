from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from .forms import ContactForm
from django.db.models import Q
from django.core.paginator import Paginator

# Home - List Contacts
def contact_list(request):
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
def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/contact_form.html', {'form': form})

# Update Contact
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/contact_form.html', {'form': form})

# Delete Contact
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.delete()
        return redirect('contact_list')
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact})
