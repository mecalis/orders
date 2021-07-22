from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Order, Position
from .forms import OrdersSearchForm
import pandas as pd
from .utils import get_customer_from_id, render_pdf_view
from meals.models import Meal
from profiles.models import Profile
import json
from datetime import datetime, timedelta
from datetime import date

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

# PDF készítése
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#Lapozás
from django.core.paginator import Paginator


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
    paginate_by = 2
    template_name = 'orders/main.html'

@login_required
def order_list_view(request):
    qs = Order.objects.all().order_by('-created')
    today = date.today()
    qs_today = qs.filter(created__year=today.year, created__month=today.month, created__day=today.day)
    paginator = Paginator(qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/main.html', {'object_list': qs, 'qs_today': qs_today, 'page_obj': page_obj})

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
        comments = json.loads(request.POST.get('comment', ''))
        boxes = json.loads(request.POST.get('boxes', ''))
        print("Dobozok: ",boxes)
        profile = Profile.objects.get(user=request.user)


        print("post data", data)
        order = Order(customer=profile)
        order.save()

        comments_cleard = {}
        for key in comments.keys():
            key_cleard = key.split('_')[0]
            comments_cleard[key_cleard] = comments[key]
        print("Comments: ", comments_cleard)

        for key in list(data.keys()):
            box = 0
            obj = get_object_or_404(Meal, pk=int(key))
            db = int(data[key])
            print("Darab ", db)
            box_per_meal = int(boxes[key])
            print("box_per_meal ", box_per_meal)

            box = db * box_per_meal
            print("Összes doboz:", box)
            comment_string = comments_cleard[key]
            pos = Position.objects.create(meal=obj, quantity=db, comment=comment_string, boxes_used=box)
            pos.save()
            order.positions.add(pos)

        # for key, comment in zip(sorted(list(data.keys())), sorted(list(comments_cleard.keys()))):
        #     # print("kulcs: ", key, " érték: ", comment)
        #     obj = get_object_or_404(Meal, pk=int(key))
        #     db = int(data[key])
        #     comment_string = comments_cleard[comment]
        #     pos = Position.objects.create(meal=obj, quantity=db, comment=comment_string, boxes_used = 0)
        #     pos.save()
        #     order.positions.add(pos)
        return JsonResponse({'msg': 'beírva'})

@login_required
def statistics(request):

    # Összes tartozás
    # Összes költés a megadott időtartamban
    profile = Profile.objects.get(user=request.user)
    qs = Order.objects.filter(customer = profile)
    last_month_qs = qs

    context = {
        "profile": profile

    }
    return render(request, 'orders/statistics.html', context)


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
    meals = None
    context = {}

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        only_self = request.POST.get('only_self')
        # print('Only:', only_self)
        qs = Order.objects.filter(created__date__lte=date_to, created__date__gte = date_from)
        if only_self:
            profile = Profile.objects.get(user=request.user)
            qs = qs.filter(customer = profile)
        # print(qs.query)
        if len(qs) > 0:
            order_df = pd.DataFrame(qs.values())
            order_df['customer_id'] = order_df['customer_id'].apply(get_customer_from_id)
            order_df['created'] = order_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            order_df['updated'] = order_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

            order_df.rename({'customer_id': 'ordered by', 'id': 'orders_id'}, axis=1, inplace=True)
            order_df['ordered by'] = order_df['ordered by'].apply(lambda x: str(x))
            order_df['created'] = order_df['created'].apply(lambda x: str(x))

            positions_data = []
            for order in qs:
                for pos in order.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'meal': pos.meal.name,
                        'meal_full': pos.meal.full_name(),
                        'meal_commented': pos.full_name(),
                        'quantity:': pos.quantity,
                        'price': pos.price,
                        'orders_id': pos.get_orders_id(),
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)
            positions_df['meal'] = positions_df['meal_commented'].apply(lambda x: str(x))
            positions_df['meal_full'] = positions_df['meal_full'].apply(lambda x: str(x))
            merged_df = pd.merge(order_df, positions_df, on='orders_id')
            df_meals = positions_df.groupby('meal', as_index=False)['quantity:'].agg('sum')



            ######################### BOKEH #################

            source_orders = ColumnDataSource(order_df)
            columns = [
                TableColumn(field="orders_id", title="ID",  width=15),
                # TableColumn(field="transacton_id", title="tranzakció száma",  width=250),
                TableColumn(field="total_price", title="teljes összeg", width=150),
                TableColumn(field="ordered by", title="megrendelő", width=150),
                TableColumn(field="paid", title="kifizetve", width=80),
                TableColumn(field="created", title="készítve", width=170),
                TableColumn(field="updated", title="módosítva"),
            ]
            data_table_orders = DataTable(source=source_orders, columns=columns, width=800, height=400)

            source_positions = ColumnDataSource(positions_df)
            columns = [
                TableColumn(field="position_id", title="pozíció ID", width=15),
                TableColumn(field="meal_full", title="étel"),
                TableColumn(field="quantity:", title="mennyiség", width=120),
                TableColumn(field="price", title="ár", width=120),
                TableColumn(field="orders_id", title="rendelés ID"),
            ]
            data_table_positions = DataTable(source=source_positions, columns=columns, width=800, )

            source_merged = ColumnDataSource(merged_df)
            columns = [
                TableColumn(field="orders_id", title="ID", width=15),
                # TableColumn(field="transacton_id", title="tranzakció száma", width=280),
                TableColumn(field="total_price", title="teljes összeg", width=150),
                TableColumn(field="ordered by", title="megrendelő"),
                TableColumn(field="paid", title="kifizetve", width=80),
                TableColumn(field="created", title="készítve", width=170),
                TableColumn(field="updated", title="módosítva"),
                TableColumn(field="position_id", title="pozíció ID", width=150),
                TableColumn(field="meal_full", title="étel"),
                TableColumn(field="quantity:", title="mennyiség", width=120),
                TableColumn(field="price", title="ár", width=120),
            ]
            data_table_merged = DataTable(source=source_merged, columns=columns, width=1200)

            source_meal = ColumnDataSource(df_meals)
            columns = [
                TableColumn(field="meal", title="Étel"),
                TableColumn(field="quantity:", title="Darabszám"),
            ]
            data_table_meal = DataTable(source=source_meal, columns=columns, height_policy='auto',
                                        height=500
                                        )

            df_pie = df_meals.copy()

            to_convert = {
                'orders': data_table_orders,
                'merged': data_table_merged,
                'meals': data_table_meal,

            }

            if df_pie.shape[0] >2:
                df_pie['angle'] = df_pie['quantity:'] / df_pie['quantity:'].sum() * 2 * pi
                df_pie['meal'] = df_pie['meal'].apply(lambda x: str(x))
                # print(df_pie)
                # print(df_pie.shape[0])

                df_pie['color'] = Category20c[df_pie.shape[0]]
                df_pie.rename({'quantity:': 'db'}, axis=1, inplace=True)
                # print(df_pie)
                p = figure(plot_height=450, title="Megoszlás", toolbar_location=None,tools="hover", tooltips="@meal: @db", x_range=(-0.5, 1.0))

                p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend_field='meal', source=df_pie)

                p.axis.axis_label = None
                p.axis.visible = False
                p.grid.grid_line_color = None
                to_convert['p'] = p

            #
            # script_table_meal, div_table_meal = components({
            #                                                 'orders': data_table_orders,
            #                                                 'merged': data_table_merged,
            #                                                 'meals': data_table_meal,
            #                                                 'p': p,
            #                                                 })

            ## BAR PLOT ###
            if only_self:
                # print(order_df)
                # print('###')
                # print(pd.unique(order_df['created']))
                source = ColumnDataSource(order_df[['total_price', 'created']])
                bar = figure(x_range=pd.unique(order_df['created']), plot_height=250, title="Költéseim:", tools = '',
                             tooltips="@total_price Ft")
                bar.vbar(x='created', top='total_price', width=0.9, source=source)
                # show(bar)
                # to_convert['bar'] = bar

            script_table_meal, div_table_meal = components(to_convert)
            ######################### BOKEH VÉGE #################


            meals = []
            for i in range(df_meals.shape[0]):
                row = f"{str(df_meals.iloc[i, 1])}x - {str(df_meals.iloc[i, 0])}"
                meals.append(row)
                # print(row)

            order_df = order_df.to_html()
            merged_df = merged_df.to_html()
            positions_df = positions_df.to_html()
            df_meals = df_meals.to_html()

            # pdf_context = {'myvar': 'hello',
            #                'order_df': order_df,
            #                'merged_df': merged_df,
            #                'df_meals': df_meals,
            #                }
            #
            # template_path = 'orders\pdf.html'
            # context = pdf_context
            # # Create a Django response object, and specify content_type as pdf
            # response = HttpResponse(content_type='application/pdf')
            # # letölthető:
            # # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # # display
            # response['Content-Disposition'] = 'filename="report.pdf"'
            # # find the template and render it.
            # template = get_template(template_path)
            # html = template.render(context)
            #
            # # create a pdf
            # pisa_status = pisa.CreatePDF(
            #     html, dest=response)
            # # if error then show some funy view
            # if pisa_status.err:
            #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
            # return response
            # # render_pdf_view(pdf_context)

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
        'meals': meals,
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
            # print(obj, ' átváltva FALSE-ra')
            return JsonResponse({'msg': 'FALSE', 'id': id})
        else:
            obj.paid = True
            obj.save()
            # print(obj, ' átváltva TRUE-ra')
            return JsonResponse({'msg': 'TRUE', 'id': id})

@login_required
def order_delete_view(request, pk):
    context = {}
    obj = get_object_or_404(Order, pk=pk)
    template_name = 'orders/delete.html'
    context = {"object": obj}
    if request.method == "POST":
        if str(request.user) == str(obj.customer) or request.user.is_staff:
            print('Törlő: ',request.user,' Tulaj: ',obj.customer)
            obj.delete()
            return redirect("/orders")
        context['message'] = "Ehhez nincs jogosultságod. Megpróbálod mégegyszer, hátha sikerül?"
    return render(request, template_name, context)

@login_required
def render_pdf_view(request):
    template_path = 'orders\pdf.html'
    context = {'myvar': 'hello world'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #letölthető:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #display
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response