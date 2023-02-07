from api.models import *
from api.serializers import *
from datetime import date
from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Q
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes, APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


#users dashboard
@api_view()
@permission_classes([AllowAny])
def Dashboard(request):
    total_debtors_amount = 0

    debtors = Debtor.objects.filter(user = request.user.id)
    # dues
    debtor_due_in_30 = debtors.filter(payment__first_payment_due_date__lte = date.today()) & Debtor.objects.filter(payment__first_payment__lte = 0)
    debtor_due_in_60 = debtors.filter(payment__second_payment_due_date__lte = date.today()) & Debtor.objects.filter(payment__second_payment__lte = 0)
    debtor_due_in_90 = debtors.filter(payment__final_payment_due_date__lte = date.today())& Debtor.objects.filter(payment__final_payment__lte = 0)

    # selling price total
    total_selling_amount = debtors.aggregate(Sum('product__product_selling_price'))

    #total amount of debtors calculation
    total_deposit_amount = debtors.aggregate(Sum('payment__deposit'))
    first_payment_total_amount = debtors.aggregate(Sum('payment__first_payment'))
    second_payment_total_amount = debtors.aggregate(Sum('payment__second_payment')) 
    final_payment_total_amount = debtors.aggregate(Sum('payment__final_payment'))

    #to catch the null(s) from aggregates
    try:
        total_debtors_amount = total_deposit_amount['payment__deposit__sum'] + first_payment_total_amount['payment__first_payment__sum'] + second_payment_total_amount['payment__second_payment__sum'] + final_payment_total_amount['payment__final_payment__sum']
    except:
        return Response('failed to calculate total amounts')

    context = {
        'debtors_count':debtors.count(),
        'due_30': debtor_due_in_30.count(),
        'due_60': debtor_due_in_60.count(),
        'due_90': debtor_due_in_90.count(),
        'total_debtors_amount': total_debtors_amount,
        'total_selling_amount': total_selling_amount['product__product_selling_price__sum']
    }
    return Response(context)

#debtor viewset
class DebtorViewset(viewsets.ModelViewSet):
    serializer_class = debtorSerializer

    #get query for debtors list
    def get_queryset(self):
        queryset = Debtor.objects.all()
        return queryset
    
    #overiding the create method for validation and other additions
    def create(self, request, *args, **kwargs):
        debtor_data = request.data

        #creating new debtor object
        new_debtor = Debtor.objects.create(
            user = request.user,
            name = debtor_data['name'],
            maiden = debtor_data['maiden'],
            surname = debtor_data['surname'],
            gender = debtor_data['gender'],
            address = debtor_data['address'],
            phonenumber = debtor_data['phonenumber'],
            id_number = debtor_data['id_number']
        )
        new_debtor.save()
        serializer = debtorSerializer(new_debtor)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        debtor = Debtor.objects.filter(
            Q(name__icontains =  'chiedza')|
            Q(created__icontains =  '')|
            Q(payment__deposit__icontains =  '')|
            Q(payment__first_payment__icontains = '')|
            Q(payment__second_payment__icontains = '')|
            Q(payment__final_payment__icontains = '')|
            Q(work__employer__contains = '')
        )
        serializer = debtorSerializer(debtor, many =True)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        if request.user.position == 'admin':
            debtor = self.get_object()
            debtor.delete()
            return Response(f'{debtor} deleted')

class workViewset(viewsets.ModelViewSet):
    serializer_class = workSerializer
    
    #get query for debtors list
    def get_queryset(self):
        debtor = Debtor.objects.all() #use post view
        return debtor

    def createWork(self, request, *args, **kwargs):
        data = request.data

        work = Work.objects.create(
            debtor = data['debtor'],
            employer = data['employer'],
            address = data['address'],
            phonenumber = data['phonenumber']
        )
        work.save()
        serializer = workSerializer(work)
        return Response(serializer.data)

class workAPIView(APIView):
    serializers = workSerializer
    def get_queryset(self):
        debtors = Work.objects.all() #use post view
        return debtors

    def get(self, request, *args, **kwargs):
        work = self.get_queryset()
        serializer = workSerializer(work, many=True)

        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        work = Work.objects.create(
            debtor = data['debtor'],
            employer = data['employer'],
            address = data['address'],
            phonenumber = data['phonenumber']
        )
        work.save()
        serializer = workSerializer(work)
        return Response(serializer.data)