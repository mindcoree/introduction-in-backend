from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import Reservation
from .forms import ReservationForm
from customers.models import Customer


class ReservationCreateView(View):
    def get(self, request):
        form = ReservationForm()
        return render(request, 'reservations/reservation_form.html', {'form': form})

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data['customer']
            table = form.cleaned_data['table']
            date = form.cleaned_data['date']

            # Проверка на наличие существующей брони для другого пользователя
            if Reservation.objects.filter(table=table, date=date).exists():
                form.add_error('table', 'Table is already reserved for this date')
                return render(request, 'reservations/reservation_form.html', {'form': form})

            # Проверка на наличие существующей брони для текущего пользователя на эту дату
            if Reservation.objects.filter(customer=customer, date=date).exists():
                form.add_error('customer', 'User already has a reservation for this date')
                return render(request, 'reservations/reservation_form.html', {'form': form})

            form.save()
            return redirect('reservation-list-create')
        return render(request, 'reservations/reservation_form.html', {'form': form})


class ReservationDetailView(View):
    def get(self, request, id):
        reservation = get_object_or_404(Reservation, id=id)
        return render(request, 'reservations/reservation_detail.html', {'reservation': reservation})


class UserReservationsView(View):
    def get(self, request, user_id):
        reservations = Reservation.objects.filter(customer_id=user_id)
        return render(request, 'reservations/reservation_list.html', {'reservations': reservations})


class ReservationUpdateView(View):
    def get(self, request, id):
        reservation = get_object_or_404(Reservation, id=id)
        form = ReservationForm(instance=reservation)
        return render(request, 'reservations/reservation_form.html', {'form': form})

    def post(self, request, id):
        reservation = get_object_or_404(Reservation, id=id)
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation-list-create')
        return render(request, 'reservations/reservation_form.html', {'form': form})


class ReservationDeleteView(View):
    def get(self, request, id):
        reservation = get_object_or_404(Reservation, id=id)
        return render(request, 'reservations/reservation_confirm_delete.html', {'reservation': reservation})

    def post(self, request, id):
        reservation = get_object_or_404(Reservation, id=id)
        reservation.delete()
        return redirect('reservation-list-create')