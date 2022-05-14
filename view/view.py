import PySimpleGUI as sg
from .entity import Button, InputField, TxtField
from controller.controllers import UserController
from .decorator import exception_handler


class UserView:
    def __init__(self):
        self.controller = UserController()
        self.task_map = None
        self.field_map = None
        self.response_field = None

        # initiate state of window
        self.event = 'Home'
        self.layout_map = {
            'Home': self.home_layout,
        }

    def run(self):
        while True:
            # Create the window
            self.window = sg.Window("DB Project", self.layout_map[self.event]())

            # Create an event loop
            while True:
                self.event, values = self.window.read()

                if self.event in self.layout_map.keys():
                    self.window.close()
                    break

                elif self.event == sg.WIN_CLOSED:
                    self.window.close()
                    exit()

                elif self.event in self.task_map.keys():
                    data = {}
                    for key, value in values.items():
                        data[self.field_map[key]] = value
                    self.task_map[self.event](**data)

    def response_layout_loader(self, response: str):
        self.response_field.extend(response, self.window)

    def home_layout(self):
        note = TxtField('Choose an action')
        create_button = Button('Create')
        delete_button = Button('Delete')
        update_button = Button('Update')
        retrieve_button = Button('Retrieve')
        list_button = Button('List')
        response_layout = TxtField('')

        self.response_field = response_layout
        self.layout_map = {
            create_button.key: self.create_layout,
            delete_button.key: self.delete_layout,
            update_button.key: self.update_layout,
            retrieve_button.key: self.retrieve_layout,
        }
        self.task_map = {
            list_button.key: self._list,
        }

        return [
            [note.layout],
            [
                create_button.layout,
                delete_button.layout,
                retrieve_button.layout,
                update_button.layout,
            ],
            [list_button.layout],
            [response_layout.layout],
        ]

    def delete_layout(self):
        id_field = TxtField('id')
        id_input = InputField('')
        delete_button = Button('Delete')
        home_button = Button('Home')
        response_layout = TxtField('')

        self.response_field = response_layout
        self.layout_map = {
            home_button.key: self.home_layout,
        }
        self.task_map = {
            delete_button.key: self._delete,
        }
        self.field_map = {
            id_input.key: 'id'
        }

        return [
            [id_field.layout, id_input.layout],
            [delete_button.layout, home_button.layout],
            [response_layout.layout],
        ]

    def create_layout(self):
        first_name = TxtField('first name')
        first_name_input = InputField('')
        last_name = TxtField('last name')
        last_name_input = InputField('')
        email = TxtField('email')
        email_input = InputField('')
        create_button = Button('Create')
        home_button = Button('Home')
        response_layout = TxtField('')

        self.response_field = response_layout
        self.layout_map = {
            home_button.key: self.home_layout,
        }
        self.task_map = {
            create_button.key: self._create,
        }
        self.field_map = {
            first_name_input.key: 'f_name',
            last_name_input.key: 'l_name',
            email_input.key: 'email',
        }

        return [
            [first_name.layout, first_name_input.layout],
            [last_name.layout, last_name_input.layout],
            [email.layout, email_input.layout],
            [create_button.layout, home_button.layout],
            [response_layout.layout],
        ]

    def update_layout(self):
        note = TxtField("Note: you cant update user id. use this field to determine target user")
        id_field = TxtField('id')
        id_input = InputField('')
        first_name = TxtField('first name')
        first_name_input = InputField('')
        last_name = TxtField('last name')
        last_name_input = InputField('')
        email = TxtField('email')
        email_input = InputField('')
        update_button = Button('Update')
        home_button = Button('Home')
        response_layout = TxtField('')

        self.response_field = response_layout
        self.layout_map = {
            home_button.key: self.home_layout,
        }
        self.task_map = {
            update_button.key: self._update,
        }
        self.field_map = {
            id_input.key: 'id',
            first_name_input.key: 'f_name',
            last_name_input.key: 'l_name',
            email_input.key: 'email',
        }

        return [
            [note.layout],
            [id_field.layout, id_input.layout],
            [first_name.layout, first_name_input.layout],
            [last_name.layout, last_name_input.layout],
            [email.layout, email_input.layout],
            [update_button.layout, home_button.layout],
            [response_layout.layout],
        ]

    def retrieve_layout(self):
        id_input = InputField('')
        id_field = TxtField('id')
        retrieve_button = Button('Retrieve')
        home_button = Button('Home')
        response_layout = TxtField('')

        self.response_field = response_layout
        self.layout_map = {
            home_button.key: self.home_layout,
        }
        self.task_map = {
            retrieve_button.key: self._retrieve,
        }
        self.field_map = {
            id_input.key: 'id',
        }

        return [
            [id_field.layout, id_input.layout],
            [retrieve_button.layout, home_button.layout],
            [response_layout.layout],
        ]

    @exception_handler
    def _retrieve(self, **kwargs):
        user = self.controller.retrieve(**kwargs)
        self.response_layout_loader(str(user))

    @exception_handler
    def _list(self, **kwargs):
        users = self.controller.list()
        resp = ""
        for user in users:
            resp += f"{str(user)}\n"
        self.response_layout_loader(resp)

    @exception_handler
    def _update(self, **kwargs):
        self.controller.update(**kwargs)
        self.response_layout_loader(f"User with was updated with new data ")

    @exception_handler
    def _delete(self, **kwargs):
        self.controller.delete(**kwargs)
        self.response_layout_loader(f"User with {kwargs} deleted")

    @exception_handler
    def _create(self, **kwargs):
        self.controller.insert(**kwargs)
        self.response_layout_loader(f"User with {kwargs} created")
