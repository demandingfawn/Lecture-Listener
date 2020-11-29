from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.scrollview import ScrollView

import ll_keyword as KS













class AccordionApp(App):
    KeywordSearch = KS.keyword()
    KeywordSearch.openTranscript("sampleText.txt")
    #change this openTranscript() to inputTrscString(),
    #   and give a string input of transcript.
    Keywords = KeywordSearch.getTopKeywords()
    def build(self):
        root = Accordion(orientation ='vertical')
        
        for i in range(0, len(self.Keywords)):
            word = self.Keywords[i]
            item = AccordionItem(title= word)
            temp = Label(text=self.KeywordSearch.searchWiki(word))
            temp.text_size = [600,100]
            temp.valign = 'center'
            #temp.size_hint_y = None
            temp.height = temp.texture_size[1]
            item.add_widget(temp)
            root.add_widget(item)
            
        return root


if __name__ == '__main__':
    AccordionApp().run()
