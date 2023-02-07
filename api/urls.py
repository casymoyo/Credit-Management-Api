from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('debtor', views.DebtorViewset, basename='debtor')
router.register('createWork', views.workViewset, basename='work')

urlpatterns = [
    path('dashboard/', views.Dashboard, name='Dashboard'),
    # path('debtors/', DebtorViewset.as_view({'get':'list'})),
    # path('debtorDetails/', DebtorViewset.as_view({'get': 'retrieve'})),
    # path('createDebtor/', DebtorViewset.as_view({'post': 'create'})),
    # path('deleteDebtor/', DebtorViewset.as_view({'get': 'delete'})),

    # path('createWork/', workViewset.as_view({'post', 'create'})),
    path('', include(router.urls))
]
