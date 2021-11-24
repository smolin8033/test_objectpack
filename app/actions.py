from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from objectpack.actions import ObjectPack
from objectpack.ui import BaseEditWindow, ModelEditWindow, make_combo_box
from m3_ext.ui import all_components as ext


"""
Я устанавливал все по зависимостям, которые были в requirements.txt.
Инструкции по импорту здесь:
https://objectpack.readthedocs.io/ru/latest/tutorial.html значительно
отличались от импорта в моей версии модуля objectpack.
"""


class ContentTypePack(ObjectPack):

	model = ContentType

	add_window = edit_window = ModelEditWindow.fabricate(model)

	add_to_menu = True

	add_to_desktop = True


class GroupPack(ObjectPack):

	model = Group

	add_window = edit_window = ModelEditWindow.fabricate(model)

	add_to_menu = True

	add_to_desktop = True


'''
CRUD пермишионов не работает из-за поля 'content_type'. Я
пробовал делать по-разному. Видимо, как-то надо обрабатывать
Foreign Key филды, почему возникает ошибка:
"Permission.content_type" must be a "ContentType" instance
не понимаю совсем. В документации тоже не нашел ни одного
примера обработки поля с внешним ключом. Если будет какой-то
фидбек, буду рад разобраться в этом.
'''


class PermissionWindow(BaseEditWindow):
	
	def _init_components(self):
		super(PermissionWindow, self)._init_components()

		self.field__name = ext.ExtStringField(
            label='Name',
            name='name',
            allow_blank=False,
            anchor='100%')

		self.field__content_type = ext.ExtComboBox(
            label='Content type',
            name='content_type',
            allow_blank=False,
            anchor='100%')

		self.field__codename = ext.ExtStringField(
            label='Codename',
            name='codename',
            allow_blank=False,
            anchor='100%')


	def _do_layout(self):
		super(PermissionWindow, self)._do_layout()
		self.form.items.extend((
				self.field__name,
				self.field__content_type,
				self.field__codename,
			))

	def set_params(self, params):
		super(PermissionWindow, self).set_params(params)
		self.height = 'auto'


class PermissionPack(ObjectPack):

	model = Permission

	#add_window = edit_window = ModelEditWindow.fabricate(model)
	add_window = edit_window = PermissionWindow

	add_to_menu = True

	add_to_desktop = True

	columns = [
        {
            'data_index': 'name',
            'header': 'Permission',
            'width': 2,
        },
        {
            'data_index': 'content_type',
            'header': 'Content type',
            'width': 2,
        },
    ]


'''
# Не смог включить поля last_login и date_joined в окно User ниже. С ними
# проблемы с форматированием даты, какие бы филды из модуля
# all_components не ставил. В документации не нашел, как это решить.
# Без них CRUD работает. Документация по m3_ext отсутствует, как я понял.
'''


class UserWindow(BaseEditWindow):
	
	def _init_components(self):
		super(UserWindow, self)._init_components()

		self.field__password = ext.ExtStringField(
            label='Password',
            name='password',
            allow_blank=False,
            anchor='100%')

		self.field__is_superuser = ext.ExtCheckBox(
            label='Superuser status',
            name='is_superuser',
            allow_blank=True,
            anchor='100%')

		self.field__username = ext.ExtStringField(
            label='Username',
            name='username',
            allow_blank=False,
            anchor='100%')

		self.field__first_name = ext.ExtStringField(
            label='First name',
            name='first_name',
            allow_blank=True,
            anchor='100%')

		self.field__last_name = ext.ExtStringField(
            label='Last name',
            name='last_name',
            allow_blank=True,
            anchor='100%')

		self.field__email = ext.ExtStringField(
            label='Email address',
            name='email',
            allow_blank=True,
            anchor='100%')

		self.field__is_staff = ext.ExtCheckBox(
            label='Staff status',
            name='is_staff',
            allow_blank=True,
            anchor='100%')

		self.field__is_active = ext.ExtCheckBox(
            label='Active',
            name='is_active',
            allow_blank=True,
            anchor='100%')


	def _do_layout(self):
		super(UserWindow, self)._do_layout()
		self.form.items.extend((
				self.field__password,
				self.field__is_superuser,
				self.field__username,
				self.field__first_name,
				self.field__last_name,
				self.field__email,
				self.field__is_staff,
				self.field__is_active,
			))

	def set_params(self, params):
		super(UserWindow, self).set_params(params)
		self.height = 'auto'


class UserPack(ObjectPack):

	model = User

	add_window = edit_window = UserWindow
	#add_window = edit_window = ModelEditWindow.fabricate(model)

	add_to_menu = True

	add_to_desktop = True