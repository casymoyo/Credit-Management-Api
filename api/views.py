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

class DebtorViewset(viewsets.ModelViewSet):
    serializer_class = debtorSerializer

    #get query for debtors list
    def get_queryset(self):
        queryset = Debtor.objects.filter(user = self.request.user.id)
        return queryset
    
    #overiding the create method for validation and other additions
    def create(self, request, *args, **kwargs):
        debtor_data = request.data

        #validation
        if request.data['gender'].lower() == 'male' or request.data['gender'].lower() == 'female':
            gender = request.data['gender'].lower()
        else: return Response('Invalid Gender')

        if len(request.data['phonenumber']) != 10:
            return Response('Invalid phonenumber')

        if len(request.data['id_number']) != 10:
            return Response('Invalid ID Number')

        #creating new debtor object
        new_debtor = Debtor.objects.create(
            user = request.user,
            name = debtor_data['name'],
            maiden = debtor_data['maiden'],
            surname = debtor_data['surname'],
            gender = gender,
            address = debtor_data['address'],
            phonenumber = debtor_data['phonenumber'],
            id_number = debtor_data['id_number']
        )
        new_debtor.save()
        serializer = debtorSerializer(new_debtor)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        debtor = Debtor.objects.filter(
            Q(name__icontains = params['pk'])|
            Q(created__icontains =  params['pk'])|
            Q(payment__deposit__icontains =  params['pk'])|
            Q(payment__first_payment__icontains = params['pk'])|
            Q(payment__second_payment__icontains = params['pk'])|
            Q(payment__final_payment__icontains = params ['pk'])|
            Q(work__employer__contains = params['pk'])
        ) & Debtor.objects.filter(user = request.user)
        serializer = debtorSerializer(debtor, many =True)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        data = request.data
        debtor = Debtor.objects.filter(user = request.user.id)

        debtor.name = data['name']
        debtor.maiden = data['maiden']
        debtor.surname = data['surname']
        debtor.gender = data['gender']
        debtor.address = data['address']
        debtor.phonenumber = data['phonenumber']

        debtor.save()
        serializer = debtorSerializer(debtor)
        return Response(serializer)

    def delete(self, request, *args, **kwargs):
        if request.user.position == 'admin':
            debtor = self.get_object()
            debtor.delete()
            return Response(f'{debtor} deleted')

class workViewset(viewsets.ModelViewSet):
    serializer_class = workSerializer
    
    #get query for debtors list
    def get_queryset(self):
        work = Work.objects.filter(debtor__user = self.request.user.id) 
        return work

    def createWork(self, request, *args, **kwargs):
        data = request.data
        params = kwargs
        print(params)
        work = Work.objects.create(
            debtor = data['debtor'],
            employer = data['employer'],
            address = data['address'],
            phonenumber = data['phonenumber']
        )
        work.save()
        serializer = workSerializer(work)
        return Response(serializer.data)

    
    def delete(self, request, *args, **kwargs):
        if request.user.position == 'admin':
            work = self.get_object()
            work.delete()
            return Response(f'{work} deleted')

class ProductViewset(viewsets.ModelViewSet):
    serializer_class =  productSerializer
    queryset = Product.objects.all()
    
class PaymentViewset(viewsets.ModelViewSet):
    serializer_class = paymentSerializer
    queryset = Payment.objects.all()
    

@api_view()
@permission_classes([AllowAny])
def overdues(request):
    debtors = Debtor.objects.filter(user = request.user.id)

    # dues
    debtor_due_in_30 = debtors.filter(payment__first_payment_due_date__lte = date.today()) & Debtor.objects.filter(payment__first_payment__lte = 0)
    debtor_due_in_60 = debtors.filter(payment__second_payment_due_date__lte = date.today()) & Debtor.objects.filter(payment__second_payment__lte = 0)
    debtor_due_in_90 = debtors.filter(payment__final_payment_due_date__lte = date.today())& Debtor.objects.filter(payment__final_payment__lte = 0)

    context = {
        'overdue_30': debtor_due_in_30,
        'overdue_60': debtor_due_in_60,
        'overdue_90': debtor_due_in_90,
    }
    return Response(context)

@api_view()
@permission_classes([AllowAny])
def overdues30(request):
    debtors = Debtor.objects.filter(user = request.user.id)

    # dues
    debtor_due_in_30 = debtors.filter(payment__first_payment_due_date__lte = date.today()) & Debtor.objects.filter(payment__first_payment__lte = 0)

    context = {
        'overdue_30': debtor_due_in_30,
    }
    return Response(context)

@api_view()
@permission_classes([AllowAny])
def overdues60(request):
    debtors = Debtor.objects.filter(user = request.user.id)

    # dues
    debtor_due_in_60 = debtors.filter(payment__second_payment_due_date__lte = date.today()) & Debtor.objects.filter(payment__second_payment__lte = 0)
    context = {
        'overdue_60': debtor_due_in_60,
    }
    return Response(context)

@api_view()
@permission_classes([AllowAny])
def overdues90(request):
    debtors = Debtor.objects.filter(user = request.user.id)

    # dues
    debtor_due_in_90 = debtors.filter(payment__final_payment_due_date__lte = date.today())& Debtor.objects.filter(payment__final_payment__lte = 0)

    context = {
        'overdue_90': debtor_due_in_90,
    }
    return Response(context)