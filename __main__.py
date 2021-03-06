from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.core.audio import Sound
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
from datetime import datetime
from kivy.app import App
from os import path
import Audio_Recording as AR
import SpeechTrans as ST
import ll_keyword as KS
import mdReader as md
import threading
import cloud
import time


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
                        unavailable_username()
                    else:
                        self.reset()
                        sm.current = "login"
                else:
                    invalid_password()
            else:
                invalid_email()
        else:
            invalid_username()

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
    username = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

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
        t = Label(font_size=25, size_hint_y=None, height=500)
        t.halign = "center"

        # add information to GridLayout
        height_calc = 0

        # add GridLayout to the ScrollView
        scr.add_widget(t)

        exitBool = True

        # add go-back button to the screen
        class ExitButton(Button):
            def on_release(self):
                ar.run = False
                rr.run = False
                pd.exitBool = False
                lecture_id = cloud.get_lecture_id(user.username)
                date = datetime.today().strftime('%m/%d/%Y')
                length = HomeWindow.LectureLength.CalcLength()
                name = "Unnamed - " + HomeWindow.LectureLength.formatted
                cloud.add_lecture(user.username, lecture_id, date, length, name)
                sm.current = "home"
                sm.transition.direction = "left"
                sm.remove_widget(sm.get_screen("ll"))
                while path.exists("audio_upload.wav") is False \
                        and path.exists("transcript_upload.md.md") is False:
                    time.sleep(0.5)
                cloud.upload_file("audio_upload.wav", user.username + "/" + lecture_id + ".wav")
                cloud.upload_file("transcript_upload.md", user.username + "/" + lecture_id + ".md")

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

        def producer():
            while exitBool:
                rr.record()
                temp = rr.tempStr
                if temp != "":
                    t.text += temp + "\n"

        pd = threading.Thread(name='producer', target=producer)
        pd.start()


class PrevLecWindow(Screen):
    username = ObjectProperty(None)
    current = ""
    # GridLayout for organizing widgets
    layout = ObjectProperty()
    # ScrollView to display lectures in scrollable form
    scr = ObjectProperty()

    def makeList(self):
        self.layout.clear_widgets()

        # button to go to transcript
        # change it when you get a way to access each transcript in database
        class tsButton(Button):
            txtName = ""
            audioName = ""
            lectureID = ""

            def setName(self, name):
                self.txtName = name

            def setAudio(self, name):
                self.audioName = name

            def set_lecture_id(self, ID):
                self.lectureID = ID

            def on_release(self):
                # first, check if transcript exists
                if cloud.check_storage(user.username + "/" + self.lectureID + ".md") is False:
                    pop = Popup(title='Can\'t Find Transcript',  # text_size = [600,100],
                                size_hint=(None, None), size=(400, 400))
                    # cont = Label(
                    #     text='Please check if transcript file exists\nin lecture folder,
                    #       or delete this lecture')
                    # cont.valign = 'center'
                    # cont.halign = 'center'
                    # pop.content = cont
                    pop.open()
                    return
                cloud.download_file(user.username + "/" + self.lectureID + ".md", "transcript_download.md")
                cloud.download_file(user.username + "/" + self.lectureID + ".wav", "audio_download.wav")
                tsScreen = Screen()

                # add audio file and button
                class audioButton(Button):
                    playtime = 0.0
                    sound = Sound()

                    def load(self, audio):
                        self.sound = SoundLoader.load("audio_download.wav")
                        print("length: ", self.sound.length)

                    def stopAudio(self):
                        self.sound.stop()

                    def on_release(self):
                        if self.sound.state == 'stop':
                            self.sound.play()
                            print(self.playtime)
                            self.sound.seek(self.playtime)
                            self.text = text = "[b]Play[/b]/Pause audio file"
                        else:
                            if path.exists("audio_download.wav") is False:
                                pop = Popup(title='Can\'t Find Audio',  # text_size = [600,100],
                                            size_hint=(None, None), size=(400, 400))
                                # cont = Label(
                                #     text='Please check if audio file exists\nin lecture folder, or delete '
                                #          'this lecture')
                                # cont.valign = 'center'
                                # cont.halign = 'center'
                                # pop.content = cont
                                pop.open()
                                return
                            print(self.sound.get_pos())
                            self.playtime = self.sound.get_pos()
                            print(self.playtime)
                            self.sound.stop()
                            self.text = "Play/[b]Pause[/b] audio file"

                audioBtn = audioButton(text="Play/[b]Pause[/b] audio file",
                                       size_hint_y=None, height=40, markup=True)
                audioBtn.pos_hint = {"center_x": 0.5, "top": 1}
                audioBtn.size_hint = (0.2, 0.05)
                audioBtn.load(self.audioName)
                tsScreen.add_widget(audioBtn)

                # add go-back button
                class backButton(Button):
                    def on_release(self):
                        sm.current = "pl"
                        sm.transition.direction = "right"
                        sm.remove_widget(sm.get_screen("ts"))
                        audioBtn.stopAudio()  # stop audio when user go out from transcript

                tempBackBtn = backButton(text="Back", size_hint_y=None, height=40)
                tempBackBtn.pos_hint = {"left": 0.2, "top": 1}
                tempBackBtn.size_hint = (0.2, 0.1)
                tsScreen.add_widget(tempBackBtn)

                # ScrollView to display transcript
                trscScr = ScrollView(size_hint=(1, 0.9), size=(Screen.width, Screen.height))
                trscScr.do_scroll_x = False
                trscScr.do_scroll_y = True

                # open transcript and check places for timestamp
                # [ref=<str>] ~some string here ~ [/ref]
                # this is text markup that enable text crickable and linked to some function
                # string in the beginning of the reference will be the parameter that passed to the function
                # when this text is clicked, it call its event, 'on_ref_press()'

                file = open("transcript_download.md", 'r', encoding='utf-8')
                trsc = file.read()
                stamps = md.mdReader()
                stamps.readMD(self.lectureID)
                stampList = stamps.getStamps()
                print(stampList)

                tsString = "[ref=0]"
                tempWord = ''
                placeCount = 1  # link this value later with list of timestamps
                isStamp = False
                stampNum = ""
                if len(stampList) != 0:
                    # we might need to change it as we decide a syntax (or where) to place timestamp.
                    for i in range(0, len(trsc)):
                        if trsc[i] == '}':
                            print("adding: ", stampList[int(stampNum)])

                            tsString += "[/ref][ref=" + str(stampList[int(stampNum)]) + "]"
                            isStamp = False
                            stampNum = ""
                            print(tsString)

                        elif isStamp:
                            stampNum += trsc[i]
                            continue

                        elif trsc[i] == '{':
                            isStamp = True

                        else:
                            tsString += trsc[i]
                else:
                    # we might need to change it as we decide a syntax (or where) to place timestamp.
                    for i in range(0, len(trsc)):
                        if trsc[i] == '}':
                            isStamp = False


                        elif isStamp:
                            continue

                        elif trsc[i] == '{':
                            isStamp = True

                        else:
                            tsString += trsc[i]
                tsString += "[/ref]"

                def go_to(time):
                    audioBtn.sound.play()
                    audioBtn.sound.seek(time)
                    return

                    # @@@@@@@@@@@@@@@@@@@@@@@@@
                    # change this function to go-to-timestamp function

                def timestamp(instance, value):
                    go_to(float(value))
                    """
                    pop = Popup(content=Label(text="sentence number is: " + value), 
                        size_hint=(None, None), size=(400, 400))
                    pop.open()
                    """
                    # @@@@@@@@@@@@@@@@@@@@@@@

                trscLabel = Label(text=tsString, markup=True)
                trscLabel.bind(on_ref_press=timestamp)

                # trscLabel.size = sm.size
                trscLabel.text_size = (600, None)
                trscLabel.size_hint = (1, None)
                # height of widget in the ScrollView need to be longer than the height of ScrollView
                trscLabel.height = int((len(trsc) / 4.5))
                trscLabel.valign = 'top'
                trscLabel.halign = 'left'

                trscScr.add_widget(trscLabel)
                tsScreen.add_widget(trscScr)

                # add keyword button
                tempKeywordBtn = keywordBtn(text="Keyword", size_hint_y=None, height=40)
                tempKeywordBtn.pos_hint = {"right": 1, "top": 1}
                tempKeywordBtn.size_hint = (0.2, 0.1)
                tempKeywordBtn.setTrsc(trsc)
                tsScreen.add_widget(tempKeywordBtn)

                # add screen to the manager
                tsScreen.name = "ts"
                sm.add_widget(tsScreen)
                sm.transition.direction = "left"
                sm.current = "ts"

        # delete button for each lectures
        class delBtn(Button):
            lectureID = 0
            screenAttached = Screen()

            def set_lecture_id(self, lecture_id):
                self.lecture_id = lecture_id

            def on_release(self):
                pop = Popup(title='Checking delete',
                            size_hint=(None, None), size=(400, 400))

                class cancleBtn(Button):
                    def on_release(self):
                        pop.dismiss()

                Btn1 = cancleBtn(text="Cancel", size_hint_y=None, height=40)

                class confirmBtn(Button):
                    # lecture_id = None
                    #
                    def set_lecture_id(self, lecture_id):
                        self.lecture_id = lecture_id

                    def on_release(self):
                        cloud.delete_lecture(self.lecture_id)
                        cloud.delete_file(user.username + "/" + self.lecture_id + ".wav")
                        cloud.delete_file(user.username + "/" + self.lecture_id + ".md")
                        sm.get_screen("pl").makeList()
                        pop.dismiss()

                Btn2 = confirmBtn(text="Delete", size_hint_y=None, height=40)
                Btn2.set_lecture_id(self.lecture_id)

                grid = GridLayout(cols=2, padding=10)
                grid.add_widget(Btn1)
                grid.add_widget(Btn2)

                grid2 = GridLayout(cols=1, padding=10)
                # L = Label(text='Are you sure you want to delete it?.')
                grid2.add_widget(Label(text='Are you sure you want to delete it?'))
                grid2.add_widget(grid)

                pop.add_widget(grid2)
                pop.open()

        # get list of lecture recordings (title, record date, running time)
        lectureList = cloud.get_lectures(user.username)

        # add information to GridLayout
        height_calc = 100
        temp = BoxLayout()
        for i in range(0, len(lectureList)):
            temp = BoxLayout(size_hint=(1, None), orientation="horizontal")
            temp.size_x = Window.width
            temp.size_y = 50

            Title = tsButton()
            Date = Label()
            Length = Label()

            Dbtn = delBtn(text="X")
            Dbtn.set_lecture_id(lectureList[i][3])
            Dbtn.font_size: (root.width ** 2 + root.height ** 2)

            Title.text = str(lectureList[i][1])
            Title.font_size: (root.width ** 2 + root.height ** 2)
            Title.setName(str(lectureList[i][5]))
            Title.setAudio(str(lectureList[i][4]))
            Title.set_lecture_id(lectureList[i][3])

            Date.text = lectureList[i][0]
            Date.font_size: (root.width ** 2 + root.height ** 2)

            Length.text = lectureList[i][2]
            Length.font_size: (root.width ** 2 + root.height ** 2)

            temp.add_widget(Title)
            temp.add_widget(Date)
            temp.add_widget(Length)
            temp.add_widget(Dbtn)

            self.layout.add_widget(temp)
            height_calc += temp.height
            self.layout.height = height_calc
        return

    def on_pre_enter(self):
        # add GridLayout to the ScrollView
        self.makeList()

    # update lecture list whenever screen is about to be used
    def on_enter(self):
        self.layout.clear_widgets()
        self.makeList()


# Keyword button for transcript page
class keywordBtn(Button):
    trsc = ""

    def setTrsc(self, tr):
        self.trsc = tr
        len(self.trsc)

    def on_release(self):
        # declare temporary screen for saving widgets
        tempScreen = Screen()
        # initiate keyword search engine
        KeywordSearch = KS.keyword()
        # KeywordSearch.openTranscript("sampleText.txt")
        KeywordSearch.inputTrscString(self.trsc)
        Keywords = KeywordSearch.getTopKeywords()

        # button for going back
        class backButton(Button):
            def on_release(self):
                sm.current = "ts"
                sm.transition.direction = "right"
                sm.remove_widget(sm.get_screen("keyword"))

        # add button to the screen
        temp = backButton(text="Back", size_hint_y=None, height=40)
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


def invalid_username():
    pop = Popup(title='Invalid Username',
                content=Label(text='A Username must be 5-16 characters.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalid_email():
    pop = Popup(title='Invalid Email',
                content=Label(text='Please enter a valid email.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalid_password():
    pop = Popup(title='Invalid Password',
                content=Label(text='A Password must be 5-16 characters.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def unavailable_username():
    pop = Popup(title='Username Not Available',
                content=Label(text='Please enter a different username.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


kv = Builder.load_file("my.kv")
sm = WindowManager()

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), HomeWindow(name="home"),
           SettingsWindow(name="settings"), PrevLecWindow(name="pl")]

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
