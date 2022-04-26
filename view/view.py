import PySimpleGUI as sg
from controller.controllers import UserController


class UserView:
    def __init__(self):
        self.controller = UserController()

        self.event = 'L-Home'

        self._create_layout_base()

        self.event_function_map = {
            'Create': self._create,
            'Delete': self._delete,
            'Retrieve': self._retrieve,
            'List': self._list,
            'Update': self._update,
        }
        self.event_layout_map = {
            'L-Create': self.create_layout,
            'L-Delete': self.delete_layout,
            'L-Retrieve': self.retrieve_layout,
            'L-Home': self.home_layout,
            'L-Update': self.update_layout
        }

    def run(self):
        while True:
            # Create the window
            self.window = sg.Window("DB Project", self.event_layout_map[self.event])

            # Create an event loop
            while True:
                self.event, values = self.window.read()

                if self.event in self.event_layout_map.keys():
                    self.window.close()
                    break

                elif self.event == sg.WIN_CLOSED:
                    self.window.close()
                    exit()
                elif self.event in self.event_function_map.keys():
                    print(self.event)
                    print(values)
                    self.event_function_map[self.event](**values)

    def _create_layout_base(self):
        self.id_field = [sg.Text("user id"), sg.In(enable_events=True, key="id")]
        self.first_name_field = [sg.Text("first name"), sg.In(enable_events=True, key="f_name")]
        self.last_name_field = [sg.Text("last name"), sg.In(enable_events=True, key="l_name")]
        self.email_field = [sg.Text("email"), sg.In(enable_events=True, key="email")]

        self.create_button = sg.Button("Create")
        self.retrieve_button = sg.Button("Retrieve")
        self.delete_button = sg.Button("Delete")
        self.update_button = sg.Button("Update")
        self.list_button = sg.Button("List")

        self.create_layout_button = sg.Button("Create", key="L-Create")
        self.retrieve_layout_button = sg.Button("Retrieve", key="L-Retrieve")
        self.delete_layout_button = sg.Button("Delete", key="L-Delete")
        self.update_layout_button = sg.Button("Update", key="L-Update")
        self.home_layout_button = sg.Button("Home", key="L-Home")

    @property
    def response_layout(self):
        self.response_container_name = f"{self.event}-Response"
        return sg.Text("", key=f"{self.event}-Response")

    def response_layout_loader(self, response: str):
        self.window.extend_layout(
            self.window[self.response_container_name],
            [[sg.Text(f"-------------------\n{response}\n-------------------")]]
        )

    @property
    def home_layout(self):
        return [
            [sg.Text("Choose an action")],
            [
                self.create_layout_button,
                self.delete_layout_button,
                self.retrieve_layout_button,
                self.update_layout_button,
            ],
            [self.list_button],
            [self.response_layout],
        ]

    @property
    def delete_layout(self):
        return [
            [self.id_field, ],
            [self.delete_button, ],
            [self.response_layout],
        ]

    @property
    def create_layout(self):
        return [
            [self.first_name_field],
            [self.last_name_field],
            [self.email_field],
            [self.create_button],
            [self.response_layout],
        ]

    @property
    def update_layout(self):
        return [
            [sg.Text("Note: you cant update user id. use this field to determine target user")],
            [self.id_field],
            [self.first_name_field],
            [self.last_name_field],
            [self.email_field],
            [self.update_button],
            [self.response_layout],
        ]

    @property
    def retrieve_layout(self):
        return [
            [self.id_field, ],
            [self.retrieve_button, ],
            [self.response_layout],
        ]

    def _retrieve(self, **kwargs):
        user = self.controller.retrieve(**kwargs)
        self.response_layout_loader(str(user))

    def _list(self, **kwargs):
        users = self.controller.list()
        resp = ""
        for user in users:
            resp += f"{str(user)}\n"
        self.response_layout_loader(resp)

    def _update(self, **kwargs):
        self.controller.update(**kwargs)
        self.response_layout_loader(f"User with was updated with new data ")

    def _delete(self, **kwargs):
        self.controller.delete(**kwargs)
        self.response_layout_loader(f"User with {kwargs} deleted")

    def _create(self, **kwargs):
        self.controller.insert(**kwargs)
        self.response_layout_loader(f"User with {kwargs} created")
