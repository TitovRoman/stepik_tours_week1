from random import sample

from django.http import Http404
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

import tours.data as mock_data


def get_min_max_value(sequence_of_dict, key):
    def get_key(item):
        return item[key]

    return min(sequence_of_dict, key=get_key)[key], max(sequence_of_dict, key=get_key)[key]


def main_view(request):
    context = {
        'subtitle': mock_data.subtitle,
        'description': mock_data.description,
        'tours': dict(sample(mock_data.tours.items(), min(6, len(mock_data.tours)))),
    }

    return render(request, 'tours/index.html', context=context)


def departure_view(request, departure):
    context = {}
    try:
        context['current_departure_humanize'] = mock_data.departures[departure]
    except KeyError:
        raise Http404
    context['tours'] = {pk: tour for pk, tour in mock_data.tours.items() if tour['departure'] == departure}

    context['tours_length'] = len(context['tours'])
    context['min_price'], context['max_price'] = get_min_max_value(context['tours'].values(), 'price')
    context['min_night'], context['max_night'] = get_min_max_value(context['tours'].values(), 'nights')

    return render(request, 'tours/departure.html', context=context)


def tour_view(request, pk):
    context = {}
    try:
        context['tour'] = mock_data.tours[pk]
    except KeyError:
        raise Http404

    if 'departure_humanize' not in context['tour']:
        context['tour']['departure_humanize'] = mock_data.departures[context['tour']['departure']]

    return render(request, 'tours/tour.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound("404 Страница не найдена")


def custom_handler500(request):
    return HttpResponseServerError("500 Server Error")
