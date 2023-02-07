from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import DebtorViewset, workViewset, workAPIView

# router = DefaultRouter
# router.register('debtor', DebtorViewset)

urlpatterns = [
    path('dashboard/', views.Dashboard, name='Dashboard'),
    path('debtors/', DebtorViewset.as_view({'get':'list'})),
    path('debtorDetails/', DebtorViewset.as_view({'get': 'retrieve'})),
    path('createDebtor/', DebtorViewset.as_view({'post': 'create'})),
    path('deleteDebtor/', DebtorViewset.as_view({'get': 'delete'})),

    path('createWork/', workAPIView.as_view()),
]
