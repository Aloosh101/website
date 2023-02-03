from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Product
from store.models.orders import Orders
from store.middlewares.auth import auth_middleware


class Order(View):

    def get(self, request):
        customer = request.session.get('customer')
        orders = Orders.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'orders.html', {'orders': orders})
