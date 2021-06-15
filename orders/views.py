from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Order
from .forms import OrdersSearchForm
import pandas as pd
from .utils import get_customer_from_id
from meals.models import Meal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@login_required
def home_view(request):
    form = OrdersSearchForm(request.POST or None)
    order_df = None
    positions_df = None
    merged_df = None
    df_meals = None

    napi_qs = []
    allando_qs = []

    napi_qs = Meal.objects.filter(type='2')
    allando_qs = Meal.objects.filter(type='1')
    egyeb_qs = Meal.objects.filter(type='4')
    napi_tablas_qs = Meal.objects.filter(type='3')

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        qs = Order.objects.filter(created__date__lte=date_to, created__date__gte = date_from)
        # print(qs.query)
        if len(qs) > 0:
            order_df = pd.DataFrame(qs.values())
            order_df['customer_id'] = order_df['customer_id'].apply(get_customer_from_id)
            order_df['created'] = order_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            order_df.rename({'customer_id': 'ordered by', 'id': 'orders_id'}, axis=1, inplace=True)


            positions_data = []
            for order in qs:
                for pos in order.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'meal': pos.meal.name,
                        'quantity:': pos.quantity,
                        'price': pos.price,
                        'orders_id': pos.get_orders_id(),
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)

            merged_df = pd.merge(order_df, positions_df, on='orders_id')
            # print(' +++++++ Merged DF ++++++++')
            # print(merged_df.columns)
            # print(merged_df)

            df_meals = positions_df.groupby('meal', as_index=False)['quantity:'].agg('sum')
            # print(df_meals)
            # merged_df_sliced = merged_df[['position_id','meal','quantity:', 'price']]
            # print(merged_df_sliced)
            # df = merged_df_sliced.groupby('position_id', as_index=False)['quantity:'].agg('sum')
            #
            # print('Összes position summa:')
            # print(df)
            #
            order_df = order_df.to_html()
            merged_df = merged_df.to_html()
            positions_df = positions_df.to_html()
            df_meals = df_meals.to_html()

            # df_pos = merged_df.groupby('ordered by', as_index=False)['price'].agg('sum')
            # df_pos_html = df.to_html()
            # print('GROUP')
            # print(df_pos)

            # df_user = merged_df.groupby('ordered by', as_index=False)['price'].agg('sum')
            # print(df_user)


        else:
            print('No data')

    context = {
        'form' : form,
        'order_df': order_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df_meals': df_meals,
        'allando_qs': allando_qs,
        'napi_qs': napi_qs,
        'egyeb_qs': egyeb_qs,
        'napi_tablas_qs': napi_tablas_qs,
        # 'df_user': df_user,
        # 'df_pos': df_pos_html,
    }
    return render(request, 'orders/home.html', context)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/main.html'

@login_required
def order_list_view(request):
    qs = Order.objects.all()
    return render(request, 'orders/main.html', {'object_list': qs})

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/detail.html'

@login_required
def order_detail_view(request, pk):
    obj = Order.objects.get(pk=pk)
    list = obj.positions.all()
    print(list)
    return render(request, 'orders/detail.html', {'object': obj, 'list': list})

# def order_edit_view(request, pk):
#     obj = Order.objects.get(pk=pk)
#     form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
#
#     confirm = False
#     if form.is_valid():
#         form.save()
#         confirm = True
#
#     context = {
#         'profile': profile,
#         'form': form,
#         'confirm': confirm,
#     }
#     return render(request, 'profiles/main.html', context)


