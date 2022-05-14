from functools import wraps
from marshmallow.exceptions import ValidationError
from model.exceptions import DBException
import PySimpleGUI as sg
from .entity import TxtField


def exception_handler(func):
    @wraps(func)
    def translate_exception(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValidationError, DBException) as err:
            warning = TxtField(f'There was some issue in your input data, pleas try again\nOrigin error:{str(err)}')
            window = sg.Window("Error!", [
                [warning.layout],
            ])

            event, _ = window.read()
            if event == sg.WIN_CLOSED:
                window.close()

    return translate_exception

