def handle_invalid_discounts(request):
    discount = {
        'lte__90': request.POST.get('un90_disc', 0),
        'gt__90': request.POST.get('up90_disc', 0),
    }
    discount['lte__90'] = int(discount['lte__90']) if discount['lte__90'] is not "" else 0
    discount['gt__90'] = int(discount['gt__90']) if discount['gt__90'] is not "" else 0
    return discount


def remove_comma_from_number(number):
    if type(number) in [int, float]:
        return number
    if type(number) == str:
        return float(number.replace(',', ''))
    return number
