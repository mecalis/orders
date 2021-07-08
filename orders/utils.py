import uuid
from profiles.models import Profile

def generate_code():
    code = str(uuid.uuid4()).replace('-','').upper()[:16]
    return code

def get_customer_from_id(val):
    customer = Profile.objects.get(id=val)
    return customer


def render_pdf_view(pdf_context):
    template_path = 'orders\pdf.html'
    context = pdf_context
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # letölthető:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # display
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

def convert_to_dataframes(qs):
    order_df = pd.DataFrame(qs.values())
    order_df['customer_id'] = order_df['customer_id'].apply(get_customer_from_id)
    order_df['created'] = order_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
    order_df['updated'] = order_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    order_df.rename({'customer_id': 'ordered by', 'id': 'orders_id'}, axis=1, inplace=True)
    order_df['ordered by'] = order_df['ordered by'].apply(lambda x: str(x))

    positions_data = []
    for order in qs:
        for pos in order.get_positions():
            obj = {
                'position_id': pos.id,
                'meal': pos.meal.name,
                'meal_commented': pos.full_name(),
                'quantity:': pos.quantity,
                'price': pos.price,
                'orders_id': pos.get_orders_id(),
            }
            positions_data.append(obj)

    positions_df = pd.DataFrame(positions_data)
    positions_df['meal'] = positions_df['meal_commented'].apply(lambda x: str(x))
    merged_df = pd.merge(order_df, positions_df, on='orders_id')
    df_meals = positions_df.groupby('meal', as_index=False)['quantity:'].agg('sum')

    return order_df, positions_df, merged_df, df_meals