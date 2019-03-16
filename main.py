from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup
import time, os, sys

class LabelShadow(Label):
    pass

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
        
        self.line = 0;
        
        
        self.video = Video(source=self.source, state='play', allow_stretch=True, keep_ratio=False)
        
        self.video.bind(on_loaded=self.on_loaded)
        
        self.kar_english = LabelShadow(text='KARAOKELAND', 
                                    size_hint_y=None,
                                    color=(0,0,0,1),
                                    font_size=32 )
                                
                                
        self.add_widget(self.video)
        self.add_widget(self.kar_english)    
        
        #si existe el archivo con los tiempos
        if os.path.exists(self.base_filename + '.kos'):            
                
            self.kar_spanish = LabelShadow(text='KARAOKELAND ESP', 
                                        size_hint_y=1,
                                        color=(0,0,0,1),
                                        font_size=32 ) 
                                        
            self.add_widget(self.kar_spanish)
            
            self.fsteps = open(self.base_filename + '.kos') #steps
            self.steps = self.fsteps.readlines()
            
            try:
                self.efsteps = open(self.base_filename + '.koe') #subtitulos en lenguaje traducido
                self.esteps = self.efsteps.readlines()
            except:
                pass
            
            #Clock.schedule_interval(self.stepchecker, .1)
            
            
            self.video.bind(position=self.on_position)
            
            self.cursteptime = self.steps[self.line]
            
        else:
            
            self.btn_stepline = Button(text='Iniciar !', 
                                        #size_hint=(1,None),
                                        on_press=self.nextline
                                        )
            self.add_widget(self.btn_stepline, index=len(self.children) )
            
            
            #open for steps creation
            self.fsteps = open(self.base_filename + '.kos', 'w+')  #karaotool steps
            
            
    def on_loaded(self, w):
        print("Iniciando video")
        
    def on_position(self, w, val):
        
        if val > float(self.cursteptime):

            try:
                self.kar_english.text = self.content[self.line]
                try:
                    self.kar_spanish.text = self.esteps[self.line]
                except:
                    pass
                
                self.line += 1
                
                #print "Step: ", self.video.position
                
                self.cursteptime = self.steps[self.line]
            except:
                self.kar_english.text = "END"
                self.kar_spanish.text = "FIN"
                
        
    def nextline(self, w):
        try:
            #advance one line
            self.kar_english.text = self.content[self.line]
            self.line += 1
            
            self.fsteps.write(str(self.video.position) + '\n')
        except:
            self.kar_english.text = "FIN"

class Karaolang(FloatLayout):
    pass

if __name__ == '__main__':
    
    from kivy.app import App
    
    class KaraolangApp(App):
        def build(self):
            return Karaotool(source=sys.argv[1])

    KaraolangApp().run()
