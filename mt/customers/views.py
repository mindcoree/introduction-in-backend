# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/list.html', {'customers': customers})

def customer_detail(request, id):
    customer = get_object_or_404(Customer, id=id)
    return render(request, 'customers/detail.html', {'customer': customer})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/create.html', {'form': form})


def edit_customer(request, id):
    customer = get_object_or_404(Customer, id)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/edit.html', {'form': form})


def delete_customer(request, id):
    customer = get_object_or_404(Customer,id)
    if request.method == "POST":
        customer.delete()
        return redirect('customers_list')
    return render(request, 'customers/delete.html', {'customer': customer})
