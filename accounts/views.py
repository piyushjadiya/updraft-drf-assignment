from django.http import HttpResponse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
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
        # return request.user.is_staff or obj.user == request.user

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class AccountsViewSet(viewsets.ViewSet):
    queryset = Account.objects.all()
    permission_classes = [IsAdminOrOwner]

    def list(self, request, format=None):
        serializer_class = AccountSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, id):
        try:
            query = Account.objects.get(id=id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer_class2 = AccountSerializer(query)
            return Response(serializer_class2.data)

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAdminOrOwner]
    #     return [permission() for permission in permission_classes]


class TransactionViewSet(viewsets.ViewSet):
    queryset = Transaction.objects.all()

    def list(self, request):
        serializer = TransactionSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        pass

    def list_id(self, request, id):
        try:
            query = Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer_class3 = TransactionSerializer(query)
            return Response(serializer_class3.data)
