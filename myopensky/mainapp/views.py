from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Airplane
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.models import User

# Часть представлений обёрнуты в декораторы @login_required для редиректа на страницу авторизации, если пользователь
# не авторизирован

# Кастомный декоратор для представлений, добавляет им условия для POST, которые повторяются для разных страниц
# Если метод GET - исполняется обёрнутое представление

# Если пользователь отправляет данные через навигационную панель,
# создается таблица с подходящими воздушными судами
def wrapper(func):
    def html_post(request, *args, **kwargs):
        if request.method == "GET":
            return func(request, *args, **kwargs)
        elif request.method == "POST":
            # Получаем значения
            icao24 = request.POST.get("1_icao24")
            origin_country = request.POST.get("1_Origin")
            long = request.POST.get("1_Longitude")
            long_inaccur = request.POST.get("long_Inaccuracy")
            lati = request.POST.get("1_Latitude")
            lati_inaccur = request.POST.get("lati_Inaccuracy")
            
            # Нелепый и смешной кусок для реализации поиска по координатам с учётом погрешности
            if long_inaccur == '':
                long_inaccur = 0
            if lati_inaccur == '':
                lati_inaccur = 0
            if long == '':
                long = 0
                long_inaccur = 90
            if lati == '':
                lati = 0
                lati_inaccur = 180
            # Фильтруем по полученным значениям БД
            airplanes = Airplane.objects.filter(origin_country__icontains = origin_country,
                                                icao24__icontains=icao24,
                                                longitude__range=[int(long) - int(long_inaccur), int(long) + int(long_inaccur)],
                                                latitude__range=[int(lati) - int(lati_inaccur), int(lati) + int(lati_inaccur)]
                                                )
            result = [row for row in airplanes]
            # Создаем контекст с результатом, для отображение в html
            context = {
                'airplanes': airplanes,
            }
        return render(request=request, template_name='app/table.html', context=context)
    return html_post


# Базовое представление домашней страницы - отображение 'любимых' ВС
@login_required
@wrapper
def show_fav(request):
    user = request.user             # Создаем объёкт пользователя, к которому применяем необходимый фильтр
    favorite = user.favorite.all    # для поиска в БД.
    context = {
        'favorite': favorite
    }
    return render(request=request, template_name='app/opensky.html', context=context)


@login_required
@wrapper
def show_airplane(request, icao24):
    airplane = Airplane.objects.get(icao24=icao24)
    context={
        'airplane': airplane,
    }
    return render(request=request, template_name='app/airplane.html', context=context)


# Два представления, для добавления и удаления любимых ВС к аккаунту. Вместо render возвращается особый redirect,
# в результате которого происходит взаимодействие с БД и обновляется текущая страница.
# В сущности - это костыль, который должен быть переделан под работу с сессиями django + AJAX

def add_favorite(request, icao24):
    airplane = Airplane.objects.get(icao24=icao24)
    add = airplane.users.add(request.user.id)
    context = {
        'add': add
    }
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))

def del_favorite(request, icao24):
    airplane = Airplane.objects.get(icao24=icao24)
    delete = airplane.users.remove(request.user.id)
    context = {
        'del': delete
    }
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
