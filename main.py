import os
from view.view import UserView
from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':
    view = UserView()
    view.run()