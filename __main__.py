# main.py
from kivy.app import App
from kivy.clock import mainthread
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
import time
import os
import cloud
import ll_keyword as KS
import SpeechTrans as ST
import Audio_Recording as AR


class user:
    username = None

    def init(username):
        user.username = username


class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if 4 < len(self.username.text) <= 16:
            if len(self.email.text) <= 320 and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
                if 4 < len(self.password.text) <= 16:
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
        if cloud.validate(self.username.text, self.password.text):
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
    email = ObjectProperty(None)
    current = ""

    class LectureLength:
        start = None
        formatted = None

        @staticmethod
        def Set():
            now = datetime.now()
            HomeWindow.LectureLength.start = now.time()
            if now.hour > 12:
                hour = now.hour - 12
                if now.minute < 10:
                    HomeWindow.LectureLength.formatted = str(hour) + ":0" + str(now.minute) + " PM"
                else:
                    HomeWindow.LectureLength.formatted = str(hour) + ":" + str(now.minute) + " PM"
            else:
                hour = now.hour
                if now.minute < 10:
                    HomeWindow.LectureLength.formatted = str(hour) + ":0" + str(now.minute) + " AM"
                else:
                    HomeWindow.LectureLength.formatted = str(hour) + ":" + str(now.minute) + " PM"

        @staticmethod
        def CalcLength():
            now = datetime.now()
            hour = now.hour - HomeWindow.LectureLength.start.hour
            minute = now.minute - HomeWindow.LectureLength.start.minute
            second = now.second - HomeWindow.LectureLength.start.second
            length = str(hour) + ":" + str(minute) + ":" + str(second)
            return length

    def RecordLectureBtn(self):
        # declare temporary screen for saving widgets
        tempScreen = Screen()

        # ScrollView to display lectures in scrollable form
        scr = ScrollView(size_hint=(1, 0.9), size=(Window.width, Window.height))
        scr.do_scroll_x = False
        scr.do_scroll_y = True

        # GridLayout for organizing widgets
        layout = GridLayout(cols=1, spacing=20, size_hint_y=None)

        # add information to GridLayout
        height_calc = 100

        # add GridLayout to the ScrollView
        layout.height = height_calc
        scr.add_widget(layout)

        # add go-back button to the screen
        class ExitButton(Button):
            def on_release(self):
                lecture_id = cloud.get_lecture_id(user.username)
                if not os.path.exists("output.wav"):
                    time.sleep(2)
                ar.run = False
                rr.run = False
                cloud.upload_file("output.wav", lecture_id + ".wav")
                # os.remove("output.wav")
                cloud.upload_file("transcript.md", lecture_id + ".md")
                # os.remove("transcript.md")
                cloud.upload_file("transcript.txt", lecture_id + ".txt")

                date = datetime.today().strftime('%m/%d/%Y')
                length = HomeWindow.LectureLength.CalcLength()
                name = "Unnamed - " + HomeWindow.LectureLength.formatted
                cloud.add_lecture(user.username, lecture_id, date, length, name)
                sm.current = "home"
                sm.transition.direction = "right"
                sm.remove_widget(sm.get_screen("ll"))

        temp = ExitButton(text="Exit", size_hint_y=None, height=40)
        temp.pos_hint = {"left": 0.2, "top": 1}
        temp.size_hint = (0.2, 0.1)
        tempScreen.add_widget(temp)

        # add the screen to the manager
        tempScreen.add_widget(scr)
        tempScreen.name = "ll"
        sm.add_widget(tempScreen)

        # change current screen
        sm.current = "ll"

        rr = ST.Recording()
        ar = AR.Audio()

    def PrevLectureBtn(self):
        # declare temporary screen for saving widgets
        tempScreen = Screen()

        # ScrollView to display lectures in scrollable form
        scr = ScrollView(size_hint=(1, 0.9), size=(Window.width, Window.height))
        scr.do_scroll_x = False
        scr.do_scroll_y = True

        # get list of lecture recordings (title, record date, running time)
        lectureList = cloud.get_lectures(user.username)

        # GridLayout for organizing widgets
        layout = GridLayout(cols=1, spacing=20, size_hint_y=None)

        # button to go to transcript
        # change it when you get a way to access each transcript in database
        class tsButton(Button):
            def on_release(self):
                tsScreen = Screen()

                # add go-back button
                class backButton(Button):
                    def on_release(self):
                        sm.current = "pl"
                        sm.transition.direction = "right"
                        sm.remove_widget(sm.get_screen("ts"))

                tempBackBtn = backButton(text="Back", size_hint_y=None, height=40)
                tempBackBtn.pos_hint = {"left": 0.2, "top": 1}
                tempBackBtn.size_hint = (0.2, 0.1)
                tsScreen.add_widget(tempBackBtn)

                # add keyword button
                tempKeywordBtn = keywordBtn(text="Keyword", size_hint_y=None, height=40)
                tempKeywordBtn.pos_hint = {"right": 1, "top": 1}
                tempKeywordBtn.size_hint = (0.2, 0.1)
                tsScreen.add_widget(tempKeywordBtn)

                print(self.id)
                cloud.download_file(self.id + ".md", "download.md")
                md = open('download.md', 'r')

                # add transcript string
                trscScr = ScrollView()
                trscScr.size =(self.width, (self.height)-0.1)
                trscScr.size_hint_y = 0.9
                # trscScr.do_scroll_x = True
                trscScr.do_scroll_y = True
                # trscLabel = Label(text=md.read())
                trscLabel = Label(text = "Test Text I hope this helps!" * 100)
                trscLabel.size_hint = (1, None)
                trscLabel.text_size = self.size
                trscLabel.halign= 'left'
                trscLabel.valign= 'middle'
                trscScr.add_widget(trscLabel)
                tsScreen.add_widget(trscScr)

                # add screen to the manager
                tsScreen.name = "ts"
                sm.add_widget(tsScreen)
                sm.transition.direction = "left"
                sm.current = "ts"

        # add information to GridLayout
        height_calc = 100
        for i in range(0, len(lectureList)):
            Date = tsButton()
            Name = Label()
            Length = Label()
            Date.text = lectureList[i][0]
            Date.font_size: (root.width ** 2 + root.height ** 2)
            Date.id = lectureList[i][3]

            Name.text = lectureList[i][1]
            Name.font_size: (root.width ** 2 + root.height ** 2)

            Length.text = lectureList[i][2]
            Length.font_size: (root.width ** 2 + root.height ** 2)

            temp = BoxLayout(size_hint=(1, None), orientation="horizontal")
            temp.size_x = Window.width
            temp.size_y = 50
            temp.add_widget(Date)
            temp.add_widget(Name)
            temp.add_widget(Length)

            layout.add_widget(temp)
            height_calc += temp.height

        # add GridLayout to the ScrollView
        layout.height = height_calc
        scr.add_widget(layout)

        # add go-back button to the screen
        class backButton(Button):
            def on_release(self):
                sm.current = "home"
                sm.transition.direction = "right"
                sm.remove_widget(sm.get_screen("pl"))

        temp = backButton(text="Back", size_hint_y=None, height=40)
        temp.pos_hint = {"left": 0.2, "top": 1}
        temp.size_hint = (0.2, 0.1)
        tempScreen.add_widget(temp)

        # add the screen to the manager
        tempScreen.add_widget(scr)
        tempScreen.name = "pl"
        sm.add_widget(tempScreen)

        # change current screen
        sm.current = "pl"

    def logOut(self):
        sm.current = "login"


# keyword button for transcript page
class keywordBtn(Button):
    def on_release(self):
        # declare temporary screen for saving widgets
        tempScreen = Screen()

        # initiate keyword search engine
        KeywordSearch = KS.keyword()
        KeywordSearch.openTranscript("sampleText.txt")
        Keywords = KeywordSearch.getTopKeywords()

        # button for going back
        class backButton(Button):
            def on_release(self):
                sm.current = "ts"
                sm.transition.direction = "right"
                sm.remove_widget(sm.get_screen("keyword"))

        # add button to the screen
        temp = backButton(text="back", size_hint_y=None, height=40)
        temp.pos_hint = {"right": 0.2, "top": 1}
        temp.size_hint = (0.2, 0.1)
        tempScreen.add_widget(temp)

        # ScrollView to store keyword list in a scrollable form.
        scr = ScrollView(size_hint=(1, 0.9), size=(Screen.width, Screen.height))
        scr.do_scroll_x = False
        scr.do_scroll_y = True

        # Accordion to store keyword and definitions
        acc = Accordion(orientation='vertical')
        acc.size_hint = (1, None)
        heightCal = 200

        # add keywords to accordion
        for i in range(0, len(Keywords)):
            word = Keywords[i]
            item = AccordionItem(title=word)

            temporaryDef = KeywordSearch.searchWiki(word)
            temp = Label(text=KeywordSearch.searchWiki(word))
            temp.text_size = [600, 100]
            temp.valign = 'center'
            # temp.size_hint_y = None
            temp.height = temp.texture_size[1]
            item.add_widget(temp)
            acc.add_widget(item)
            heightCal += item.min_space

        # add Accordion to the ScrollView
        acc.height = heightCal
        scr.add_widget(acc)
        tempScreen.add_widget(scr)

        # add screen to the manager
        tempScreen.name = "keyword"
        sm.add_widget(tempScreen)

        # change current screen
        sm.current = "keyword"


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

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),
           HomeWindow(name="home"), SettingsWindow(name="settings")]

for screen in screens:
    sm.add_widget(screen)

# sm.current = "login"
sm.current = "home"
user.username = "caseyroot"


class MyMainApp(App):
    def build(self):
        Window.size = (700, 500)
        Window.top = 200
        Window.left = 200
        return sm


if __name__ == "__main__":
    MyMainApp().run()
