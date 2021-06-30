from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Order, Position
from .forms import OrdersSearchForm
import pandas as pd
from .utils import get_customer_from_id
from meals.models import Meal
from profiles.models import Profile
import json
from datetime import datetime

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin

from math import pi
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.models.widgets.markups import Div
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.transform import cumsum
from bokeh.layouts import column, row,Spacer, WidgetBox
from bokeh.palettes import Category20c

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

    napi_qs = Meal.objects.filter(type='2', day = datetime.now())
    allando_qs = Meal.objects.filter(type='1')
    egyeb_qs = Meal.objects.filter(type='4')
    napi_tablas_qs = Meal.objects.filter(type='3', day = datetime.now())

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
    qs = Order.objects.all().order_by('-created')
    return render(request, 'orders/main.html', {'object_list': qs})

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/detail.html'

@login_required
def order_detail_view(request, pk):
    obj = Order.objects.get(pk=pk)
    list = obj.positions.all()
    # print(list)
    return render(request, 'orders/detail.html', {'object': obj, 'list': list})

@login_required
def order_new(request):
    data = None
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.POST.get('data', ''))
        boxdb = request.POST.get('boxdb', '')
        profile = Profile.objects.get(user=request.user)

        print("Boxdb:", boxdb)
        print("DATA:")
        print("post data", data)
        print("Kulcsok:")
        order = Order(customer=profile)
        order.save()
        for key in list(data.keys()):
            obj = get_object_or_404(Meal, pk=int(key))
            db = int(data[key])
            print("MEAL:", obj)
            print("darabszám", data[key])
            pos = Position.objects.create(meal=obj, quantity=db)
            pos.save()

            order.positions.add(pos)
        # order.save()
        print(order)

        return JsonResponse({'msg': 'beírva'})


@login_required
def queries_view(request):
    form = OrdersSearchForm(request.POST or None)
    order_df = None
    positions_df = None
    merged_df = None
    df_meals = None
    script_table_meal = None
    div_table_meal = None
    script_table_orders = None
    div_table_orders = None

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
            order_df['ordered by'] = order_df['ordered by'].apply(lambda x: str(x))

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
            df_meals = positions_df.groupby('meal', as_index=False)['quantity:'].agg('sum')



            ######################### BOKEH #################

            source_orders = ColumnDataSource(order_df)
            columns = [
                TableColumn(field="orders_id", title="orders_id"),
                TableColumn(field="transacton_id", title="transacton_id"),
                TableColumn(field="total_price", title="total_price"),
                TableColumn(field="ordered by", title="ordered by"),
                TableColumn(field="paid", title="paid"),
                TableColumn(field="created", title="created"),
                TableColumn(field="updated", title="updated"),
            ]
            data_table_orders = DataTable(source=source_orders, columns=columns, width=800, height=400)

            source_positions = ColumnDataSource(positions_df)
            columns = [
                TableColumn(field="position_id", title="pozíció ID"),
                TableColumn(field="meal", title="étel"),
                TableColumn(field="quantity:", title="mennyiség"),
                TableColumn(field="price", title="ár"),
                TableColumn(field="orders_id", title="rendelés ID"),
            ]
            data_table_positions = DataTable(source=source_positions, columns=columns, width=800, )

            source_merged = ColumnDataSource(merged_df)
            columns = [
                TableColumn(field="orders_id", title="rendelés ID"),
                TableColumn(field="transacton_id", title="tranzakció száma"),
                TableColumn(field="total_price", title="teljes összeg"),
                TableColumn(field="ordered by", title="megrendelő"),
                TableColumn(field="paid", title="kifizetve"),
                TableColumn(field="created", title="készítve"),
                TableColumn(field="updated", title="módosítva"),
                TableColumn(field="position_id", title="pozíció ID"),
                TableColumn(field="meal", title="étel"),
                TableColumn(field="quantity:", title="mennyiség"),
                TableColumn(field="price", title="ár"),
            ]
            data_table_merged = DataTable(source=source_merged, columns=columns, width=800)

            source_meal = ColumnDataSource(df_meals)
            columns = [
                TableColumn(field="meal", title="Étel"),
                TableColumn(field="quantity:", title="Darabszám"),
            ]
            data_table_meal = DataTable(source=source_meal, columns=columns, height_policy='auto',
                                        height=250
                                        )

            df_pie = df_meals.copy()
            df_pie['angle'] = df_pie['quantity:'] / df_pie['quantity:'].sum() * 2 * pi
            df_pie['meal'] = df_pie['meal'].apply(lambda x: str(x))
            df_pie['color'] = Category20c[df_pie.shape[0]]
            df_pie.rename({'quantity:': 'db'}, axis=1, inplace=True)
            print(df_pie)
            p = figure(plot_height=350, title="Megoszlás", toolbar_location=None,tools="hover", tooltips="@meal: @db", x_range=(-0.5, 1.0))

            p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend_field='meal', source=df_pie)

            p.axis.axis_label = None
            p.axis.visible = False
            p.grid.grid_line_color = None

            layout = column(
                Div(text="Rendelések:", height=80, sizing_mode="stretch_width"),
                data_table_orders,
                # data_table_positions,
                Div(text='Részletek:', height=80, sizing_mode="stretch_width"),
                data_table_merged,
                Div(text='Rendelt ételek:', height=80, sizing_mode="stretch_width"),
                data_table_meal,

                #  Spacer(width=100),
                # WidgetBox(data_table),
            )

            # output_file("DATATABLE TEST.html")
            # show(p)
            # script_table_orders, div_table_orders = components(data_table_orders)
            # script_table_meal, div_table_meal = components(layout)
            script_table_meal, div_table_meal = components({'orders': data_table_orders,
                                                            'merged': data_table_merged,
                                                            'meals': data_table_meal,
                                                            'p': p,
                                                            })



            ######################### BOKEH VÉGE #################


            order_df = order_df.to_html()
            merged_df = merged_df.to_html()
            positions_df = positions_df.to_html()
            df_meals = df_meals.to_html()

    context = {
        'form': form,
        'order_df': order_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df_meals': df_meals,
        'script_table_meal': script_table_meal,
        'div_table_meal': div_table_meal,
        'script_table_orders': script_table_orders,
        'div_table_orders': div_table_orders,
        # 'df_user': df_user,
        # 'df_pos': df_pos_html,
    }
    return render(request, 'orders/queries.html', context)

@staff_member_required
def order_toggle_view(request):
    data = None
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.POST.get('data', ''))
        id = int(data['id'])
        obj = get_object_or_404(Order, pk=id)
        if obj.paid == True:
            obj.paid = False
            obj.save()
            print(obj, ' átváltva FALSE-ra')
            return JsonResponse({'msg': 'FALSE', 'id': id})
        else:
            obj.paid = True
            obj.save()
            print(obj, ' átváltva TRUE-ra')
            return JsonResponse({'msg': 'TRUE', 'id': id})

@login_required
def order_delete_view(request, pk):

    obj = get_object_or_404(Order, pk=pk)
    template_name = 'orders/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/orders")
    context = {"object": obj}
    return render(request, template_name, context)