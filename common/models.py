from django.contrib.auth.models import AbstractUser
from django.db.models import Model, IntegerField, DateTimeField, CharField, ForeignKey, DO_NOTHING, DateField


class AbstractLibraryBaseModel(Model):
    creator = IntegerField('creator', null=True)
    created_at = DateTimeField(verbose_name='Created at', auto_now_add=True)

    modifier = IntegerField('modifier', null=True)
    modified_at = DateTimeField(verbose_name='Modified at', auto_now=True)

    class Meta:
        abstract = True


class College(Model):
    name = CharField('name', null=False, blank=False, max_length=200)

    class Meta:
        db_table = 'library_college'


class User(AbstractUser, AbstractLibraryBaseModel):
    avatar = CharField('Avatar', max_length=1000)
    nickname = CharField('Nickname', null=True, blank=True, max_length=200)
    gender = CharField('Gender', null=False, blank=False, max_length=200)
    student_id = CharField('Student ID', null=False, blank=False, max_length=30)
    college = ForeignKey(College, verbose_name='College', on_delete=DO_NOTHING, related_name='user_college',
                         null=True)
    major = CharField('Major', null=False, blank=False, max_length=200)
    admission_at = DateField('Admission at', default=None)
    role = CharField('Role', null=True, blank=True, max_length=200)

    @property
    def new_password(self):
        return self.password

    class Meta:
        db_table = 'library_user'
