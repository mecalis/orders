import uuid
from profiles.models import Profile

def generate_code():
    code = str(uuid.uuid4()).replace('-','').upper()[:16]
    return code

def get_customer_from_id(val):
    customer = Profile.objects.get(id=val)
    return customer