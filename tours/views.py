import random

from django.shortcuts import render
from django.views import View

from tours.data import tours, departures


class MainView(View):
    def get(self, request):
        context = {
            'tours': random.sample(list(tours.values()), 6)
        }
        return render(request, 'tours/index.html', context)


class DepartureView(View):
    def get(self, request, departure):
        tours_with_departure = {tour_id: tour_item for tour_id, tour_item in tours.items() if
                                tour_item['departure'] == departure}
        context = {
            'tours': tours_with_departure,
            'fly_from': departures[departure],
            'total_count_tours': len(tours_with_departure),
            'min_price': to_pretty_price(get_min_value(tours_with_departure, 'price')),
            'max_price': to_pretty_price(get_max_value(tours_with_departure, 'price')),
            'min_nights': get_min_value(tours_with_departure, 'nights'),
            'max_nights': get_max_value(tours_with_departure, 'nights'),
        }
        return render(request, 'tours/departure.html', context)


class TourView(View):
    def get(self, request, id):
        tour = tours[id]
        context = {
            'stars_string': '★' * int(tour['stars']),
            'tour': tour,
            'departure': departures[tour['departure']],
        }
        return render(request, 'tours/tour.html', context)


def custom_handler_404(request, exception):
    return render(request, 'tours/error_404.html')


def custom_handler_500(request):
    return render(request, 'tours/error_500.html')


def get_max_value(dict_, param):
    return max([dict_[key][param] for key in dict_])


def get_min_value(dict_, param):
    return min([dict_[key][param] for key in dict_])


def to_pretty_price(price):
    price = str(price)[::-1]
    return ' '.join(price[i:i + 3] for i in range(0, len(price), 3))[::-1]
