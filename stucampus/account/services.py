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


def is_exist(email):
    exist_in_user = True
    exist_in_student = True
    try:
        query_user = User.objects.get(username=email)
    except User.DoesNotExist:
        exist_in_user = False
    try:
        query_user.student
    except:
        exist_in_student = False
    return (exist_in_student or exist_in_user)
