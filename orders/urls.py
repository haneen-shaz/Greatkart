from django.urls import path
from . import views

urlpatterns = [
    path('place_order/<int:id>', views.place_order, name='place_order'),
    path('place_order/', views.place_orderone, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('orders/place_order/cod',views.cash_on_delivery,name='cod'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('invoice/<int:id>',views.Invoice),
      

]





