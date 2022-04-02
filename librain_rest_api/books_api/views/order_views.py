from django.shortcuts import render
from rest_framework.response import Response
from books_api.models import Book, Order, OrderItem, ShippingAddress
from books_api.serializers import BookSerializer, OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems'] #this is the list sent from the frontend
    if orderItems and len(orderItems) == 0: #but we have to check if there any products in the order
        return Response({'detail':'No Order Items'}, status = status.HTTP_400_BAD_REQUEST)
    else:
        #1 create order
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            tax = data['taxPrice'],
            shipping = data['shippingPrice'],
            total = data['totalPrice'],
        )
        #2 create shipping address
        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            zip = data['shippingAddress']['zip'],
            state = data['shippingAddress']['state'],
            shipping = data['shippingPrice']
        )
        #3 create order items and set order to orderItem ralationship
        for i in orderItems:
            book = Book.objects.get(id=i['bookId'])

            item = OrderItem.objects.create(
                book = book,
                order = order,
                name = book.name,
                qty = i['qty'],
                price = i['price'],

            )
            #4 Update the countInStock
            book.countInStock -= item.qty
            book.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
