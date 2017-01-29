# coding: utf-8
import ui,colorsys

class ColorPicker(ui.View):
	def __init__(self, *args,**kwargs):
		ui.View.__init__(self,*args,**kwargs)
		self.history=[]  #future...keep track of recent colors
		self.current=(.3,0.2,0.5) 
		self.N=16
		self.Nb=32
	def draw(self):
			square_size=min(self.width,self.height)
			N=self.N
			Nb=self.Nb
			dx=square_size*1.0/(N+2)
			dxb=N*dx/Nb
			h,s,v=self.current
			i0,j0,k0=(round(c*N) for c in self.current)
	
			k0=round(self.current[2]*Nb)
			#draw H/S grid
			for i in xrange(0,N):
				for j in xrange(0,N):			
					ui.set_color(colorsys.hsv_to_rgb(i*1.0/N,j*1.0/N,v))
					ui.set_blend_mode(ui.BLEND_NORMAL)
					ui.fill_rect(round(i*dx),round(j*dx),round(dx),round(dx))
	
			#draw V slider
			for k in xrange(0,Nb):
				ui.set_color(colorsys.hsv_to_rgb(h,s,k*1./Nb))
				ui.set_blend_mode(ui.BLEND_NORMAL)
				ui.fill_rect(round((N+1)*dx),round(k*dxb),round(dx),round(dxb+0.5))
				
			#highlight selection
			if all([c>=0 for c in self.current]):
				ui.set_color(colorsys.hsv_to_rgb(h,s,1-0.5*(1-v)))
				p=ui.Path.rect(i0*dx,j0*dx,dx,dx)
				p.line_width=4
				p.stroke()
				
				ui.set_color(colorsys.hsv_to_rgb(h,s,1-0.5*(1-v)))
				p=ui.Path.rect((N+1)*dx,k0*dxb,dx,dxb)
				p.line_width=4
				p.stroke()
				#preview
				ui.set_color(colorsys.hsv_to_rgb(h,s,v))
				ui.fill_rect(0,(N+1)*dx,6*dx,dx)
				r,g,b=colorsys.hsv_to_rgb(h,s,v)
				
				clip=lambda x:min(max(x,0),1)
				rp,gp,bp=colorsys.hsv_to_rgb(1-h,1,clip((0.5-v)*100))
				ui.draw_string(			('{:02x}'*3).format(int(r*255),int(g*255),int(b*255)), (0,(N+1)*dx,6*dx,dx),alignment=ui.ALIGN_CENTER,color=(rp,gp,bp))
	def touch_began(self,touch):
		self.touch_moved(touch)
	def touch_moved(self,touch):
			#set color
			#  self dx=size/(N+2)
			square_size=min(self.width,self.height)
			N=self.N
			Nb=self.Nb
			dx=square_size*1.0/(N+2)
			dxb=N*dx*1.0/Nb
			h,s,v=self.current
			if touch.location[0]>=dx*(N+1) and touch.location[1]<=dxb*Nb:
				v=round(touch.location[1]/dxb-0.5)/Nb
			elif touch.location[1]<=dx*N and touch.location[0]<=dx*N:
				h=round(touch.location[0]/dx-0.5)/N
				s=round(touch.location[1]/dx-0.5)/N
			clip=lambda x:min(max(x,0),1)
			self.current=(clip(h),clip(s),clip(v))
			self.set_needs_display()
v=ColorPicker(frame=(0,0,360,576))
v.present('sheet')