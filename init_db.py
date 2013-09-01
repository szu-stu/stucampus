#-*- coding: utf-8
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from stucampus.account.models import Student
from stucampus.organization.models import Organization


DEFAULT_ADMIN_EMAIL = 'stucampus@live.cn'
DEFAULT_ADMIN_PASSWORD = '123456'
DEFAULT_ADMIN_NAME = 'stucampus'


create_perm = Permission.objects.create
create_group = Group.objects.create
get_content_type = ContentType.objects.get


def run():
    # Content_type for permissions
    student_model_content_type = get_content_type(app_label='account')
    organization_content_type = get_content_type(app_label='organization')
    infor_content_type = get_content_type(app_label='infor')

    # Permissions for student
    students_list = create_perm(codename='students_list',
                               name='List all students',
                               content_type=student_model_content_type)
    student_show = create_perm(codename='student_show',
                               name='Show the information of student.',
                               content_type=student_model_content_type)
    student_create = create_perm(codename='student_create',
                                 name='Create new student.',
                                 content_type=student_model_content_type)
    student_edit = create_perm(codename='student_edit',
                               name='Edit the information of students.',
                               content_type=student_model_content_type)
    student_del = create_perm(codename='student_del',
                              name='Delete student.',
                              content_type=student_model_content_type)

    # Permissions for organizations
    organizations_list = create_perm(codename='organizations_list',
                                    name='List all organizations.',
                                    content_type=organization_content_type)
    organization_show = create_perm(codename='organization_show',
                                    name='Show information of organization.',
                                    content_type=organization_content_type)
    organization_create = create_perm(codename='organization_create',
                                      name='Create organization.',
                                      content_type=organization_content_type)
    organization_edit = create_perm(codename='organization_edit',
                                    name='Edit information of organization.',
                                    content_type=organization_content_type)
    organization_del = create_perm(codename='organization_del',
                                   name='Delete the organization.',
                                   content_type=organization_content_type)

    # Permissions for organization managers.
    managers_list = create_perm(codename='org_managers_list',
                               name='List all managers of a organization.',
                               content_type=student_model_content_type)
    manager_create = create_perm(codename='org_manager_create',
                                  name='Create new manager.',
                                  content_type=student_model_content_type)
    managers_del = create_perm(codename='org_manager_del',
                               name='Delete manager of a organization',
                               content_type=student_model_content_type)

    # Permissions for organization members
    members_list = create_perm(codename='members_list',
                              name='List the members in a organization.',
                              content_type=student_model_content_type)
    member_show = create_perm(codename='member_show',
                              name='Show the information of member.',
                              content_type=student_model_content_type)
    member_create = create_perm(codename='member_create',
                                name='Create member in a organization.',
                                content_type=student_model_content_type)
    member_del = create_perm(codename='member_del',
                             name='Delete member from a organization',
                             content_type=student_model_content_type)

    # Permission for infor
    infors_list = create_perm(codename='infors_list',
                             name='List all informations',
                             content_type=infor_content_type)
    infor_show = create_perm(codename='infor_show',
                             name='Show an information.',
                             content_type=infor_content_type)
    infor_create = create_perm(codename='infor_create',
                               name='Create an information.',
                               content_type=infor_content_type)
    infor_edit = create_perm(codename='infor_edit',
                             name='Edit an information',
                             content_type=infor_content_type)
    infor_del = create_perm(codename='infor_del',
                            name='Delete information',
                            content_type=infor_content_type)

    admin_email = (raw_input('Please input the email of admin, '
                             'or leave blank for %s.\n' % DEFAULT_ADMIN_EMAIL)
                   or DEFAULT_ADMIN_EMAIL)
    admin_password = (raw_input('Please input the password of admin, '
                                'or leave blank for %s\n'
                                % DEFAULT_ADMIN_PASSWORD)
                      or DEFAULT_ADMIN_PASSWORD)
    admin_name = (raw_input('Please input the name of admin, '
                            'or leave blank for %s\n'
                            % DEFAULT_ADMIN_NAME)
                  or DEFAULT_ADMIN_NAME)
    admin_user = User.objects.create_user(username=admin_email,
                                          email=admin_email,
                                          password=admin_password)
    student = Student.objects.create(user=admin_user, screen_name=admin_name)

    admin_group = create_group(name='StuCampus')
    organization_manager_group = create_group(name='organization_manager')
    organization_member_group = create_group(name='organization_member')

    org = Organization.objects.create(name='深圳大学学子天地')
    org.url = 'http://stu.szu.edu.cn'
    org.logo = '/static/images/layout/logo3.png'
    org.save()

    admin_user.groups.add(admin_group, organization_manager_group)
    org.managers.add(admin_user.student)
    perms = Permission.objects.all()
    for perm in perms:
        admin_group.permissions.add(perm)

    organization_manager_group.permissions.add(organizations_list,
                                               organization_show,
                                               organization_edit,
                                               organization_del)
