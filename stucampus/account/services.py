from django.contrib.auth.models import User
from stucampus.account.models import Student


def find(id):
    try:
        query_user = User.objects.get(id__exact=id).student
    except Student.DoesNotExist:
        return None
    except User.DoesNotExist:
        return None
    return query_user.student


def find_by_email(email):
    try:
        query_user = User.objects.get(email__exact=email).student
    except Student.DoesNotExist:
        return None
    except User.DoesNotExist:
        return None
    return query_user.student