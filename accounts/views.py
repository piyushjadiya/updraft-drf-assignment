import datetime

from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


# Create your views here.
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def home(request):
    return HttpResponse("Hello World!!")


class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an account to view it.
    """

    def has_permission(self, request, view):
        # Permissions are only allowed to the owner of the account.
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user.id == request.user.id

class AccountRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAdminOrOwner]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class AccountsListView(generics.ListAPIView):
    queryset = Account.objects.all()
    permission_classes = [IsAdminOrOwner]
    pagination_class = CursorPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Account.objects.all()
        elif user.is_authenticated:
            return Account.objects.filter(user=user)
        else:
            return Account.objects.none()

    def list(self, request, format=None):
        serializer_class = AccountSerializer(self.get_queryset(), many=True)
        return Response({"results": serializer_class.data})


class TransactionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminOrOwner]

class CursorSetPagination(CursorPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    ordering = 'id' # '-created' is default

class TransactionListView(generics.ListAPIView):
    pagination_class = CursorSetPagination
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        start_timestamp = self.request.query_params.get('start_timestamp')
        end_timestamp = self.request.query_params.get('end_timestamp')
        account_id = self.request.query_params.get('account_id')
        transaction_category = self.request.query_params.get('transaction_category')

        queryset = Transaction.objects.all()

        if start_timestamp is not None:
            start_dt = datetime.datetime.fromtimestamp(int(start_timestamp))
            queryset = queryset.filter(timestamp__gte=start_dt)
        
        if end_timestamp is not None:
            end_dt = datetime.datetime.fromtimestamp(int(end_timestamp))
            queryset = queryset.filter(timestamp__lte=end_dt)
        
        if account_id is not None:
            queryset = queryset.filter(account_id=account_id)
        
        if transaction_category is not None:
            queryset = queryset.filter(transaction_category=transaction_category)

        user = self.request.user
        if not user.is_staff:
            if not user.is_authenticated:
                return queryset.none()
            else:
                queryset = queryset.filter(account__user=self.request.user)
        
        return queryset

    def list(self, request):
        serializer = self.get_serializer()
        return Response(serializer.data)
    
    def get_serializer(self):
        serializer = TransactionSerializer(self.get_queryset(), many=True)
        return serializer

    # def list_id(self, request, id):
    #     try:
    #         query = Transaction.objects.get(id=id)
    #     except Transaction.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     if request.method == 'GET':
    #         serializer_class3 = TransactionSerializer(query)
    #         return Response(serializer_class3.data)
