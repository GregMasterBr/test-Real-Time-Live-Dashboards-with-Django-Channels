from django.shortcuts import render, redirect, get_object_or_404
from .models import Statistic, DataItem  
from faker import Faker
from django.http import JsonResponse
from django.db.models import Sum
fake = Faker()

def main(request):    
    
    qs = Statistic.objects.all()
    if request.method == "POST":
        new_stat = request.POST.get('new-statistic')
        obj, created = Statistic.objects.get_or_create(name=new_stat)        
        return redirect('dashboard', obj.slug)

    return render(request,'main.html', {'qs':qs})


def dashboard(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    return render(request,'dashboard.html', {
        'name':obj.name,
        'slug':obj.slug,
        'data':obj.data,
        'user': request.user.username if request.user.username else fake.name()
    })


def chart_data(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    qs = obj.data.values('owner').annotate(Sum('value'))
    chartdata = [x ["value__sum"] for x in qs ]
    chartlables = [x ["owner"] for x in qs ]
    print(chartdata)
    return JsonResponse({
        "chartData":chartdata,
        "chartLabels":chartlables
    })