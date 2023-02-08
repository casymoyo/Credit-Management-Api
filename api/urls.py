from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('debtor', views.DebtorViewset, basename='debtor')
router.register('createWork', views.workViewset, basename='work')
router.register('product', views.ProductViewset, basename='product')
router.register('payment', views.PaymentViewset, basename='payment')

urlpatterns = [
    path('dashboard/', views.Dashboard, name='Dashboard'),
    # path('debtors/', DebtorViewset.as_view({'get':'list'})),
    # path('debtorDetails/', DebtorViewset.as_view({'get': 'retrieve'})),
    # path('createDebtor/', DebtorViewset.as_view({'post': 'create'})),
    # path('deleteDebtor/', DebtorViewset.as_view({'get': 'delete'})),

    # path('createWork/', workViewset.as_view({'post', 'create'})),
    path('', include(router.urls)),
    path('overdues', views.overdues, name='overdues'),
    path('overdues30', views.overdues30, name='overdues30'),
    path('overdues60', views.overdues60, name='overdues60'),
    path('overdues90', views.overdues90, name='overdues90'),
]
