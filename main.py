from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup
import time, os, sys

class Karaotool(FloatLayout):
    
    def __init__(self, **kwargs):
        super(Karaotool, self).__init__(**kwargs)
        
        self.source = kwargs.get('source', None)
        
        
        if self.source == None:
            self.selecttextfile = Popup(title='Select the lirycs')
            self.selecttextfile.content = BoxLayout(orientation='vertical')
            self.selecttextfile.content.add_widget(Button(text='Seleccionar archivo') )
            self.selecttextfile.content.add_widget(Button(text='Insertar texto') )
            self.selecttextfile.open()
            
        else:
        
            self.base_filename = os.path.splitext(self.source)[0]
           
            with open(self.base_filename + '.kot') as f:    #open karaotool text file
                self.content = f.readlines()
           
        
        self.btn_stepline = Button(text='Iniciar !', 
                                    #size_hint=(1,None)
                                    on_press=self.nextline
                                    )
        self.add_widget(self.btn_stepline)
        
        
        self.video = Video(source=self.source, state='play')
        
        self.add_widget(self.video)
        
        self.kar_english = Label(text='englishh :)', 
                                    size_hint_y=None,
                                    font_size=32 )
                                    
        
        self.line = 0;
        
        self.add_widget(self.kar_english)
        
        self.start = time.time()
        
        #si existe el archivo con los tiempos
        if os.path.exists(self.base_filename + '.kos'):
            self.fsteps = open(self.base_filename + '.kos')
            self.steps = self.fsteps.readlines()
            Clock.schedule_interval(self.stepchecker, .1)
            
            self.cursteptime = self.steps[self.line]
            
        else:
            #open for steps creation
            self.fsteps = open(self.base_filename + '.kos', 'w+')  #karaotool steps
        
    def stepchecker(self, dt):
        
        elapsed = time.time() - self.start
        
        if elapsed > float(self.cursteptime):

            self.kar_english.text = self.content[self.line]
            self.line += 1
            
            print "Step: ", elapsed
            
            self.cursteptime = self.steps[self.line]
        
    def nextline(self, w):
        #advance one line
        self.kar_english.text = self.content[self.line]
        self.line += 1
        
        elapsed = time.time() - self.start
        
        self.fsteps.write(str(elapsed) + '\n')
        

if __name__ == '__main__':
    from kivy.base import runTouchApp
    
    runTouchApp(Karaotool(source = sys.argv[1]) )
