from stucampus.account.models import User


def find(id):
    query_user = User.objects.get(id__exact=id)
    return query_user


def get_by_email(email):
    query_user = User.objects.get(email__exact=email)
    return query_user


def validate_user(email, passwd):
    try:
        query_user = User.objects.get(email__exact=emaili + password__exact=passwd)
    except User.DoesNotExsit:
        return None
    return query_user
