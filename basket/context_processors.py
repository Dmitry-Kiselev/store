def basket_lines_count(request):
    return {
        'basket_lines_count': request.user.basket.all_lines().count() or 'empty'}
