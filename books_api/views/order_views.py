from django.shortcuts import render
from rest_framework.response import Response
from books_api.models import Book, Order, OrderItem, ShippingAddress
from books_api.serializers import BookSerializer, OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from datetime import datetime



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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user #this is from the token
    try:
        order = Order.objects.get(id=pk)
        if user.is_staff or order.user == user :
            serializer = OrderSerializer(order, many = False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this order'}, status = status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order is not existed'},status = status.HTTP_400_BAD_REQUEST )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many = True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(id=pk)
    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()
    return Response('Order was paid')
