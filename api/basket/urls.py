from .views import BasketViewSet,  LineViewSet


basket_list = BasketViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
basket_detail = BasketViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

line_list = LineViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
line_detail = LineViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
