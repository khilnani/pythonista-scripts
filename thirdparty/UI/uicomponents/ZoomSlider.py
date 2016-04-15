# coding: utf-8
import ui
class ZoomSlider(ui.View):
   '''a slider like view, which is both zoomable and panable.   '''
   def __init__(self,vert=1,barwidth=0.25,barvalue=0.5,*args,**kwargs):
      self.bg_color=(0.9,.9,.9)
      ui.View.__init__(self,*args,**kwargs)
      self.vert=vert
      self.barwidth=barwidth
      self.barvalue=barvalue
      self.multitouch_enabled=True
      self.dragging=False
      self.touches={}
   def draw(self):
      ui.set_color((.7,.5,.5))
      if not self.vert:
         path=ui.Path.rounded_rect((self.barvalue-self.barwidth/2.)*self.width,0,self.barwidth*self.width,self.height,self.height*0.1)
      else:
         path=ui.Path.rounded_rect(0,(self.barvalue-self.barwidth/2.)*self.height,self.width, self.barwidth*self.height,self.width*0.1)
      path.fill()
      ui.set_color((0.5,.5,.5))
      path.stroke()
      ui.set_color((0.5,0,0))
      if len(self.touches)==1:
         ui.set_color((0.7,0.7,0))
         path.fill()
      elif len(self.touches)==2:
         ui.set_color((0.7,0.0,0.7))
         path.fill()
   def touch_began(self,touch) :
      self.touches[touch.touch_id]=touch.location
      self.dragging=True
      self.set_needs_display()
   def touch_moved(self,touch):
      self.touches[touch.touch_id]=touch.location
      self.dragging=True
      vert=self.vert
      size=self.frame[2:]
      if len(self.touches)==1:  #single touch pan.  ios type "fine scrubbing" by dragging finger away from slider
         fine_scale=size[1-vert]/(size[1-vert]+abs(touch.location[1-vert]))
         self.barvalue+=fine_scale*(touch.location[vert]-touch.prev_location[vert])/size[vert]
         if self.barvalue-self.barwidth/2.<=0:
            self.barvalue=self.barwidth/2.
         elif (self.barvalue+self.barwidth/2.)>=1:
            self.barvalue=1-self.barwidth/2.
      elif len(self.touches)==2:
         fine_scale=size[1-vert]/(size[1-vert]+abs(touch.location[1-vert]))
         other=self.touches[[k for k in self.touches.keys() if not k==touch.touch_id][0]]
         curr_width=max(abs(other[vert]-touch.location[vert]),1.)
         old_width=max(abs(other[vert]-touch.prev_location[vert]),1.)
         scale=fine_scale*(1.-old_width/curr_width)+1.0
         self.barwidth*=scale
         #pan by 1/2 of motion

         self.barvalue+=fine_scale*(touch.location[vert]-touch.prev_location[vert])/size[vert]/2.
         if self.barvalue-self.barwidth/2.<=0:
            self.barvalue=self.barwidth/2.
         elif (self.barvalue+self.barwidth/2.)>=1:
            self.barvalue=1-self.barwidth/2.
      self.set_needs_display()
      if hasattr(self,'action') and callable(self.action):
         self.action(self)
   def touch_ended(self,touch):
       del self.touches[touch.touch_id]
       if len(self.touches)==0:
          self.dragging=False
          if hasattr(self,'action') and callable(self.action):
             self.action(self)
       self.set_needs_display()
      
#v=ZoomSlider(frame=(0,0,100.,1000.))
#v.present('sheet')