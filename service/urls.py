"""service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

import accounts.views as views

viewaccount = views.AccountsListView.as_view()
viewaccountid = views.AccountRetrieveAPIView.as_view()
viewtransaction = views.TransactionListView.as_view(pagination_class=views.CursorSetPagination)
viewtransactionid = views.TransactionRetrieveAPIView.as_view()

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", viewaccount, name="account"),
    path('accounts/<int:id>/', viewaccountid, name="account_id"),
    path("transactions/", viewtransaction, name="transaction"),
    path("transactions/<int:id>/", viewtransactionid, name="transaction_id"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
]
