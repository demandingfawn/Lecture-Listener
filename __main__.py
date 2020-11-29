# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
import cloud


class user:
    username = None

    def init(username):
        user.username = username


class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if len(self.username.text) > 4 and len(self.username.text) <= 16:
            if len(self.email.text) <= 320 and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
                if len(self.password.text) > 4 and len(self.password.text) <= 16:
                    if not cloud.add_user(self.username.text, self.email.text, self.password.text):
                        takenUsername()
                    self.reset()
                    sm.current = "login"
                else:
                    invalidPassword()
            else:
                invalidEmail()
        else:
            invalidUsername()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.username.text = ""


class LoginWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        user.init(self.username.text)
        if cloud.validate(user.username, self.password.text):
            self.reset()
            sm.current = "home"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.username.text = ""
        self.password.text = ""


class HomeWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    username = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def lecturelist(self):
        lectures = cloud.get_lectures(user.username)
        screen = Screen()
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)
        for x in lectures:
            items = OneLineListItem(text=x[0] + x[1] + x[2])
            list_view.add_widget(items)
        screen.add_widget(scroll)
        return screen

    # def lecturelist(self):
    #     tempScreen = Screen()
    #     lectures = cloud.get_lectures(user.username)
    #
    #     class backButton(Button):
    #         def on_release(self):
    #             sm.current = "ts"
    #             sm.transition.direction = "right"
    #
    #     temp = backButton(text="back", size_hint_y=None, height=40)
    #     temp.pos_hint = {"right": 0.2, "top": 1}
    #     temp.size_hint = (0.2, 0.1)
    #     tempScreen.add_widget(temp)
    #
    #     scr = ScrollView()
    #     scr.do_scroll_x = False
    #     acc = Accordion(orientation='vertical')
    #     acc.min_space = 44
    #     for i in range(0, len(lectures)):
    #         word = lectures[i][0]
    #         item = AccordionItem(title=word)
    #         # temp = Label(text=lectures[i][0] + lectures[i][1] + lectures[i][2])
    #         # temp.text_size = [600, 100]
    #         # temp.valign = 'center'
    #         # # temp.size_hint_y = None
    #         # temp.height = temp.texture_size[1]
    #         # item.add_widget(temp)
    #         acc.add_widget(item)
    #     scr.add_widget(acc)
    #     tempScreen.add_widget(scr)
    #
    #     tempScreen.name = "keyword"
    #     sm.add_widget(tempScreen)


class LecList(Screen):
    n = ObjectProperty(None)
    username = ObjectProperty(None)
    current = ""


class Transcript(Screen):
    n = ObjectProperty(None)
    current = ""


class SettingsWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidUsername():
    pop = Popup(title='Invalid Username',
                content=Label(text='A Username must be 5-16 characters.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidEmail():
    pop = Popup(title='Invalid Username',
                content=Label(text='Please enter a valid email.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidPassword():
    pop = Popup(title='Invalid Password',
                content=Label(text='A Username must be 5-16 characters.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def takenUsername():
    pop = Popup(title='Username Not Available',
                content=Label(text='Please enter a different username.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), HomeWindow(name="home")
    , LecList(name="ll"), Transcript(name="ts"), SettingsWindow(name="settings")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
