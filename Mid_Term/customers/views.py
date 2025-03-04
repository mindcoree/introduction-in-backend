from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import Customer
from .forms import CustomerForm

class CustomerListCreateView(View):
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'customers/customer_list.html', {'customers': customers})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer-list-create')
        return render(request, 'customers/customer_form.html', {'form': form})

class CustomerDetailView(View):
    def get(self, request, id):
        customer = get_object_or_404(Customer, id=id)
        return render(request, 'customers/customer_detail.html', {'customer': customer})

class CustomerCreateView(View):
    def get(self, request):
        form = CustomerForm()
        return render(request, 'customers/customer_form.html', {'form': form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer-list-create')
        return render(request, 'customers/customer_form.html', {'form': form})

class CustomerEditView(View):
    def get(self, request, id):
        customer = get_object_or_404(Customer, id=id)
        form = CustomerForm(instance=customer)
        return render(request, 'customers/customer_form.html', {'form': form})

    def post(self, request, id):
        customer = get_object_or_404(Customer, id=id)
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer-list-create')
        return render(request, 'customers/customer_form.html', {'form': form})

class CustomerDeleteView(View):
    def get(self, request, id):
        customer = get_object_or_404(Customer, id=id)
        return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})

    def post(self, request, id):
        customer = get_object_or_404(Customer, id=id)
        customer.delete()
        return redirect('customer-list-create')