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