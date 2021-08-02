from django.shortcuts import render, get_object_or_404, redirect
from .utils import get_images_from_facebook, extract_data_from_image
from django.http import JsonResponse
import json
from django.contrib.admin.views.decorators import staff_member_required

from profiles.models import Profile
from meals.models import Meal


# Create your views here.
@staff_member_required
def classifier_home_view(request):
    # image = get_images_from_facebook()
    # day_data = extract_data_from_image(image)
    template = 'classifier/home.html'
    context = {'msg': 'msg'}
    # return JsonResponse({'msg': 'beírva'})
    return render(request, template, context=context)

@staff_member_required
def classifier_get_data_view(request):
    if request.method == "GET" and request.is_ajax():
        image = get_images_from_facebook()[0]
        day_data = extract_data_from_image(image)
        context = {'day_data': day_data, 'msg': True}
        return JsonResponse(context)

@staff_member_required
def classifier_new_data_view(request):
    if request.method == "POST" and request.is_ajax():
        day_datas = json.loads(request.POST.get('data', ''))
        def get_int_or_0(day_data, key):
            # if len(day_data[key]) > 0:
            #     return day_data[key]
            # else:
            #     return 0
            return int(day_data[key]) if len(day_data[key]) else 0

        def save_meal_if_exist(meal_nev, meal_ar, date, type, boxes, description=''):
            if len(meal_nev)>0 and meal_ar>0:
                meal = Meal.objects.create(name=meal_nev, price=meal_ar, day=date, type=type, description=description, boxes=boxes)
                meal.save()

        # print(day_data)
        for day in day_datas.keys():
            day_data = day_datas[day]
            print(day)
            print(day_data)
            date = day_data['date']
            fozi_ar = get_int_or_0(day_data, 'fozi_ar')
            fozi_nev = day_data.get('fozi_nev', '')
            save_meal_if_exist(meal_nev=fozi_nev, meal_ar=fozi_ar, date=date, type='3', boxes=1, description='')

            feltet_ar = get_int_or_0(day_data, 'feltet_ar')
            feltet_nev = day_data.get('feltet_nev', '')
            save_meal_if_exist(meal_nev=feltet_nev, meal_ar=feltet_ar, date=date, type='3', boxes=0, description='')

            M1_leves_nev = day_data.get('M1_leves_nev', '')
            M1_leves_ar = get_int_or_0(day_data, 'M1_leves_ar')
            save_meal_if_exist(meal_nev='Egyes menü levese magában', meal_ar=M1_leves_ar, date=date, type='2', boxes=1, description=M1_leves_nev)

            M1_fo_nev = day_data.get('M1_fo_nev', '')
            M1_fo_ar = get_int_or_0(day_data, 'M1_fo_ar')
            save_meal_if_exist(meal_nev='Egyes menü főétele magában', meal_ar=M1_fo_ar, date=date, type='2', boxes=1, description=M1_fo_nev)

            M2_leves_nev = day_data.get('M2_leves_nev', '')
            M2_leves_ar = get_int_or_0(day_data, 'M2_leves_ar')
            save_meal_if_exist(meal_nev='Kettes menü levese magában', meal_ar=M2_leves_ar, date=date, type='2', boxes=1,
                               description=M2_leves_nev)

            M2_fo_nev = day_data.get('M2_fo_nev', '')
            M2_fo_ar = int(day_data.get('M2_fo_ar', '0'))
            save_meal_if_exist(meal_nev='Kettes menü főétele magában', meal_ar=M2_fo_ar, date=date, type='2', boxes=1,
                               description=M2_fo_nev)

            M1 = f"{M1_leves_nev} és {M1_fo_nev}"
            save_meal_if_exist(meal_nev='Egyes menü', meal_ar=1050, date=date, type='2', boxes=2,
                               description=M1)

            M2 = f"{M2_leves_nev} és {M2_fo_nev}"
            save_meal_if_exist(meal_nev='Kettes menü', meal_ar=950, date=date, type='2', boxes=2,
                               description=M2)
        return JsonResponse({'msg': 'Sikeresen bekerült az adatbázisba'})


