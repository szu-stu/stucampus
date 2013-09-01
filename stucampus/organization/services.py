from django.contrib.auth.models import Group


def organization_update(student, organization):
    if not organization in student.orgs_as_member.all():
        organization.members.add(student)
    organization.managers.add(student)
    try:
        org_mng_group = Group.objects.get(name='organization_manager')
        student.user.groups.add(org_mng_group)
    except Group.DoesNotExist:
        pass
