from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Reservation, Table


def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/list.html', {'reservations': reservations})


def reservation_detail(request, id):
    reservation = get_object_or_404(Reservation, id=id)

    if request.method == 'GET':
        return render(request, 'reservations/detail.html', {'reservation': reservation})

    elif request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status not in dict(Reservation.STATUS_CHOICES).keys():
            return HttpResponse('Неверный статус', status=400)
        reservation.status = new_status
        reservation.save()
        return redirect('reservations:reservation_detail', id=reservation.id)

    return HttpResponseNotAllowed(['GET', 'POST'])


def reservation_create(request):
    if request.method == 'POST':
        user_id = request.POST.get('customer_id')
        table_id = request.POST.get('table_id')
        date = request.POST.get('date')
        time = request.POST.get('time')

        user = get_object_or_404(User, id=user_id)
        table = get_object_or_404(Table, id=table_id)

        # Проверка на существующие брони
        if Reservation.objects.filter(customer=user, date=date).exists():
            return HttpResponse('У вас уже есть бронь на этот день!', status=400)
        if Reservation.objects.filter(table=table, date=date, time=time).exists():
            return HttpResponse('Этот стол уже забронирован на указанное время!', status=400)

        reservation = Reservation(customer=user, table=table, date=date, time=time)
        reservation.save()
        return redirect('reservations:reservation_list')

    return render(request, 'reservations/create.html')


def reservation_delete(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservations:reservation_list')

    return HttpResponseNotAllowed(['POST'])


def reservations_by_user(request, user_id):
    reservations = Reservation.objects.filter(customer_id=user_id)
    return render(request, 'reservations/user_list.html', {'reservations': reservations})
