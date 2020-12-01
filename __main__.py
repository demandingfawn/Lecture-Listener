# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
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

import cloud
import ll_keyword as KS
import time
import os.path
from os import path

from mutagen.mp3 import MP3

class user:
    username = None
    def init(username):
        user.username = username

class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if len(self.username.text)>4 and len(self.username.text)<=16:
            if len(self.email.text)<=320 and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
                if len(self.password.text)>4 and len(self.password.text)<=16:
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

class AddLecWindow(Screen):
    username = ObjectProperty(None)
    course = ObjectProperty(None)
    audio = ObjectProperty(None)
    transcript = ObjectProperty(None)

    def addLecture(self):
        #if course name is empty
        if self.course.text == "":
            pop = Popup(
                  content=Label(text='Please enter a course name.'),
                  size_hint=(None, None), size=(400, 400))
            pop.open()
        
        #if audio file doesn't exists
        elif self.audio.text == "" or path.exists("lectures/" + str(self.audio.text) + ".mp3") == False:
            pop = Popup(content=Label(text='Please check if audio file exists in lecture folder'),
                  size_hint=(None, None), size=(400, 400))
            pop.open()
        
        #if transcript file doesn't exists
        elif self.transcript.text == "" or path.exists("lectures/" + str(self.transcript.text) + ".txt") == False:
            pop = Popup(title='Username Not Available',
                  content=Label(text='Please check if transcript file exists in lecture folder'),
                  size_hint=(None, None), size=(400, 400))
            pop.open()
        
        #when everything is valid
        else:
            print(str(self.audio.text))
            print(str(self.transcript.text))
            currentDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            mp3File = MP3("lectures/" + str(self.audio.text) + ".mp3")
            length = mp3File.info.length
            h = int(length/3600)
            m = int((length - (3600 * h))/60)
            s = int((length - (3600 * h))%60)
            lengthStr = str(h) + ":" + str(m) + ":" + str(s)
            print("added/",cloud.add_lecture(user.username, cloud.get_lecture_id(user.username), currentDate, lengthStr, self.course.text, self.audio.text, self.transcript.text)
)
        self.course.text = ""
        self.audio.text = ""
        self.transcript.text = ""
        sm.transition.direction = "up"
        sm.current = "pl"

class PrevLecWindow(Screen):
    username = ObjectProperty(None)
    current = ""
    #GridLayout for organizing widgets
    layout = ObjectProperty()
    #ScrollView to display lectures in scrollable form
    scr = ObjectProperty()
    
    """
    #declear temporary screen for saving widgets
    tempScreen = Screen()
    """
    def makeList(self):
        self.layout.clear_widgets()
        #button to go to transcript
        #change it when you get a way to access each transcript in database
        class tsButton(Button):
            txtName = ""
            def setName(self, name):
                self.txtName = name
            def on_release(self):
                #first, check if transcript exists
                print("file name: ",str(self.txtName))
                if path.exists("lectures/" + str(self.txtName) + ".txt") == False:
                    pop = Popup(title='Transcript Not Available', #text_size = [600,100],
                  size_hint=(None, None), size=(400, 400))
                    cont = Label(text='Please check if transcript file exists\nin lecture folder, or delete this lecture')
                    cont.valign = 'center'
                    cont.halign = 'center'
                    pop.content = cont
                    pop.open()
                    return
                
                tsScreen = Screen()

                #add go-back button
                class backButton(Button):
                    def on_release(self):
                        sm.current = "pl"
                        sm.transition.direction = "right"
                        sm.remove_widget(sm.get_screen("ts"))
                
                tempBackBtn = backButton(text= "Back", size_hint_y=None, height=40)
                tempBackBtn.pos_hint = {"left": 0.2, "top":1}
                tempBackBtn.size_hint = (0.2,0.1)
                tsScreen.add_widget(tempBackBtn)
                
                #add transcript string
                trscScr = ScrollView(size_hint=(1, 0.9), size=(Screen.width, Screen.height))
                trscScr.do_scroll_x = False
                trscScr.do_scroll_y = True
                f = open("lectures/" + str(self.txtName) + ".txt", 'r',encoding='utf-8')
                trsc = f.read()
                trscLabel = Label(text = trsc)
                print(len(trsc))

                trscLabel.text_size = (600, None)
                trscLabel.size_hint = (1,None)
                trscLabel.height = int((len(trsc)/4.5)) #height of widget in the ScrollView need to be longer than the height of ScrollView
                trscLabel.valign = 'top'
                trscLabel.halign = 'left'
                
                trscScr.add_widget(trscLabel)
                tsScreen.add_widget(trscScr)
                
                #add keyword button
                tempKeywordBtn = keywordBtn(text= "Keyword", size_hint_y=None, height=40)
                tempKeywordBtn.pos_hint = {"right": 1, "top":1}
                tempKeywordBtn.size_hint = (0.2,0.1)
                tempKeywordBtn.setTrsc(trsc)
                tsScreen.add_widget(tempKeywordBtn)
                
                
                
                #trscLabel.text_size.width=tsScreen.width
                print("height ", trscLabel.text_size.height)
                print("width ", trscLabel.text_size.width)
                print("t size ", trscLabel.text_size)
                trscLabel.size_hint = (1,None)
                temp.valign = 'center'
                temp.halign = 'center'
                trscScr.add_widget(trscLabel)
                tsScreen.add_widget(trscScr)

        
                
                #add screen to the manager
                tsScreen.name = "ts"
                sm.add_widget(tsScreen)
                sm.transition.direction = "left"
                sm.current = "ts"

        #delete button for each lectures
        class delBtn(Button):
            lectureID = 0
            screenAttached = Screen()
            
            def setLectureID(self,ID):
                self.lectureID = ID
                
            def on_release(self):
                pop = Popup(title='Checking delete',
                  size_hint=(None, None), size=(400, 400))
                
                class cancleBtn(Button):
                    def on_release(self):
                        pop.dismiss()
                        
                Btn1 = cancleBtn(text= "Cancle", size_hint_y=None, height=40)
                
                class confirmBtn(Button):
                    lecture = 0
                    def setLecture(self, l):
                        self.lecture = l
                    def on_release(self):
                        cloud.delete_lecture(user.username,self.lecture)
                        sm.get_screen("pl").makeList()
                        pop.dismiss()
                        
                Btn2 = confirmBtn(text= "Delete", size_hint_y=None, height=40)
                Btn2.setLecture(self.lectureID)

                grid = GridLayout(cols = 2, padding = 10)
                grid.add_widget(Btn1)
                grid.add_widget(Btn2)

                grid2 = GridLayout(cols = 1, padding = 10)
                L = Label(text='Are you sure you want to delete it?.')
                grid2.add_widget(L)
                grid2.add_widget(grid)

                pop.add_widget(grid2)
                pop.open()
                
        #get list of lecture recordings (title, record date, running time)
        
        lectureList = cloud.get_lectures(user.username)
        
        #add information to GridLayout
        height_calc = 100
        temp = BoxLayout()
        for i in range(0,len(lectureList)):
            temp = BoxLayout(size_hint = (1, None), orientation = "horizontal")
            temp.size_x = Window.width
            temp.size_y = 50
            
            Title = tsButton()
            Date = Label()
            Length = Label()
            Dbtn = delBtn(text= "X")

            Dbtn.setLectureID(lectureList[i][3])
            
            Dbtn.font_size: (root.width**2 + root.height**2)

            Title.text = str(lectureList[i][1])
            Title.font_size: (root.width**2 + root.height**2)
            Title.setName(str(lectureList[i][5]))

            Date.text = lectureList[i][0]
            Date.font_size: (root.width**2 + root.height**2)

            Length.text = lectureList[i][2]
            Length.font_size: (root.width**2 + root.height**2)
            
            temp.add_widget(Title)
            temp.add_widget(Date)
            temp.add_widget(Length)
            temp.add_widget(Dbtn)

            self.layout.add_widget(temp)
            height_calc += temp.height
            self.layout.height = height_calc
        return
    
    def on_pre_enter(self):
        #add GridLayout to the ScrollView
        self.makeList()
        """
        #add go-back button to the screen
        class backButton(Button):
            def on_release(self):
                sm.current = "home"
                sm.transition.direction = "right"
                sm.remove_widget(sm.get_screen("pl"))
        temp = backButton(text= "back", size_hint_y=None, height=40)
        temp.pos_hint = {"left": 0.2, "top":1}
        temp.size_hint = (0.2,0.1)
        self.add_widget(temp)

        #add button for adding new lecture file
        class addBtn(Button):
            def on_release(self):
                sm.current = "al"
                sm.transition.direction = "down"

        temp = addBtn(text= "Add new Lecture", size_hint_y=None, height=40)
        temp.pos_hint = {"right": 1, "top":1}
        temp.size_hint = (0.2,0.1)
        self.add_widget(temp)
        """
        
    

    #update lecture list whenever screen is about to be used
    def on_enter(self):
        self.layout.clear_widgets()
        self.makeList()


class HomeWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    username = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"


class LecList(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""



#keyword button for transcript page    
class keywordBtn(Button):
    trsc = ""

    def setTrsc(self, tr):
        self.trsc = tr
        len(self.trsc)
    def on_release(self):
        #declear temporary screen for saving widgets
        tempScreen = Screen()

        #initiate keyword search engine
        KeywordSearch = KS.keyword()
        #KeywordSearch.openTranscript("sampleText.txt")
        KeywordSearch.inputTrscString(self.trsc)
        
        Keywords = KeywordSearch.getTopKeywords()
        

        #button for going back
        class backButton(Button):
            def on_release(self):
                sm.current = "ts"
                sm.transition.direction = "right"
                sm.remove_widget(sm.get_screen("keyword"))

        #add button to the screen
        temp = backButton(text= "back", size_hint_y=None, height=40)
        temp.pos_hint = {"right": 0.2, "top":1}
        temp.size_hint = (0.2,0.1)
        tempScreen.add_widget(temp)

        #ScrollView to store keyword list in a scrollable form.
        scr = ScrollView(size_hint=(1, 0.9), size=(Screen.width, Screen.height))
        scr.do_scroll_x = False
        scr.do_scroll_y = True

        #Accordion to store keyword and definitions
        acc = Accordion(orientation ='vertical')
        acc.size_hint = (1, None)
        heightCal = 200

        #add keywords to accordion
        for i in range(0, len(Keywords)):
            word = Keywords[i]
            item = AccordionItem(title= word)

            temporaryDef = KeywordSearch.searchWiki(word)
            temp = Label(text=KeywordSearch.searchWiki(word))
            temp.text_size = [600,100]
            temp.valign = 'center'
                #temp.size_hint_y = None
            temp.height = temp.texture_size[1]
            item.add_widget(temp)
            acc.add_widget(item)
            heightCal += item.min_space

        #add Accordion to the ScrollView    
        acc.height = heightCal
        scr.add_widget(acc)
        tempScreen.add_widget(scr)
        
        #add screen to the manager
        tempScreen.name = "keyword"
        sm.add_widget(tempScreen)

        #change current screen
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

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),HomeWindow(name="home")
    ,LecList(name="ll"),SettingsWindow(name="settings"), AddLecWindow(name = "al"), PrevLecWindow(name = "pl")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
