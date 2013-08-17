from stucampus.account.models import User


def find(id):
    try:
        query_user = User.objects.get(id__exact=id)
    except User.DoesNotExist:
        return None
    return query_user


def get_by_email(email):
    try:
        query_user = User.objects.get(email__exact=email)
    except User.DoesNotExist:
        return None
    return query_user


def validate_user(email, passwd):
    try:
        query_user = User.objects.get(email__exact=email, password__exact=passwd)
    except User.DoesNotExist:
        return None
    return query_user
