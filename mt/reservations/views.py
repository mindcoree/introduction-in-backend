from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation
from .forms import ReservationForm

def reservation_create(request):
    error = None
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Проверка: если на выбранный стол уже есть бронь на эту дату
            if Reservation.objects.filter(table=reservation.table, date=reservation.date).exists():
                error = 'На выбранный столик уже есть бронь на эту дату.'
            # Проверка: если у клиента уже есть бронь в этот день
            elif Reservation.objects.filter(customer=reservation.customer, date=reservation.date).exists():
                error = 'У этого клиента уже есть бронь на эту дату.'
            else:
                reservation.save()
                return redirect('reservation_detail', id=reservation.id)
    else:
        form = ReservationForm()
    return render(request, 'reservations/create.html', {'form': form, 'error': error})

def reservation_detail(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    return render(request, 'reservations/detail.html', {'reservation': reservation})

def reservations_by_user(request, user_id):
    reservations = Reservation.objects.filter(customer__id=user_id)
    return render(request, 'reservations/user_list.html', {'reservations': reservations})

def reservation_update(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    error = None
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated_reservation = form.save(commit=False)
            # Если изменился стол или дата – проверяем на наличие конфликта
            if Reservation.objects.filter(table=updated_reservation.table, date=updated_reservation.date).exclude(id=reservation.id).exists():
                error = 'На выбранный столик уже есть бронь на эту дату.'
            elif Reservation.objects.filter(customer=updated_reservation.customer, date=updated_reservation.date).exclude(id=reservation.id).exists():
                error = 'У этого клиента уже есть бронь на эту дату.'
            else:
                updated_reservation.save()
                return redirect('reservation_detail', id=reservation.id)
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservations/update.html', {'form': form, 'reservation': reservation, 'error': error})

def reservation_delete(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    if request.method == 'POST':
        customer_id = reservation.customer.id
        reservation.delete()
        return redirect('reservations_by_user', user_id=customer_id)
    return render(request, 'reservations/confirm_delete.html', {'reservation': reservation})
