import string, random
import PySimpleGUI as sg


def entity_key_generator():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))


class Entity:
    def __init__(self, txt):
        self.key = entity_key_generator()
        self.txt = txt


class Button(Entity):
    def __init__(self, txt):
        super(Button, self).__init__(txt)
        self.layout = sg.Button(self.txt, key=self.key)


class TxtField(Entity):
    def __init__(self, txt):
        super(TxtField, self).__init__(txt)
        self.layout = sg.Text(self.txt, key=self.key)

    def extend(self, additional_txt, window):
        window.extend_layout(
            window[self.key],
            [[sg.Text(f"-------------------\n{additional_txt}\n-------------------")]]
        )


class InputField(Entity):
    def __init__(self, txt):
        super(InputField, self).__init__(txt)
        self.layout = sg.In(self.txt, key=self.key, enable_events=True)
