from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import ValidationError
from .models import Reservation


def reservation_detail(request, id):
    """
    GET /reservations/{id}/ – показать детали брони;
    POST /reservations/{id}/ – обновить статус брони.
    """
    reservation = get_object_or_404(Reservation, id=id)

    if request.method == 'GET':
        return render(request, 'reservations/detail.html', {'reservation': reservation})

    elif request.method == 'POST':
        # Обновление только поля status
        new_status = request.POST.get('status')
        if new_status not in dict(Reservation.STATUS_CHOICES).keys():
            return HttpResponse('Неверный статус', status=400)
        reservation.status = new_status
        try:
            reservation.save()
        except ValidationError as e:
            # Если валидация не пройдена, отображаем ошибку в том же шаблоне
            return render(request, 'reservations/detail.html', {'reservation': reservation, 'error': e.message})
        return redirect('reservation_detail', id=reservation.id)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def reservation_delete(request, id):
    """
    DELETE /reservations/{id}/ – удалить бронь.
    Так как HTML-формы не поддерживают метод DELETE, можно использовать POST-запрос.
    """
    reservation = get_object_or_404(Reservation, id=id)
    if request.method == 'POST':
        reservation.delete()
        # Перенаправляем на список броней конкретного пользователя
        return redirect('reservations_by_user', user_id=reservation.customer.id)
    else:
        return HttpResponseNotAllowed(['POST'])


def reservations_by_user(request, user_id):
    """
    GET /reservations/user/{user_id}/ – получить список всех броней конкретного пользователя.
    """
    reservations = Reservation.objects.filter(customer_id=user_id)
    return render(request, 'reservations/user_list.html', {'reservations': reservations})
