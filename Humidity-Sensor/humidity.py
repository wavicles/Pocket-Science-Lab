'''
Relative Humidity using HS-1101 Sensor

ExpEYES program developed as a part of GSoC-2015 project
Project Tilte: Sensor Plug-ins, Add-on devices and GUI Improvements for ExpEYES
Mentor Organization:FOSSASIA
Mentors: Hong Phuc, Mario Behling, Rebentisch
Author: Praveen Patil
License : GNU GPL version 3
'''
import gettext
gettext.bindtextdomain("expeyes")
gettext.textdomain('expeyes')
_ = gettext.gettext

from Tkinter import *
import time, math, sys
if sys.version_info.major==3:
        from tkinter import *
else:
        from Tkinter import *

sys.path=[".."] + sys.path


import expeyes.eyesj as eyes
import expeyes.eyeplot as eyeplot
import expeyes.eyemath as eyemath

WIDTH  = 600   # width of drawing canvas
HEIGHT = 400   # height    

class humidity:
	tv = [ [], [], [] ]			# Lists for Readings
	TIMER = 500				# Time interval between reads
	MINY = 0				# Humidity Range
	MAXY = 250
	running = False
				
	def start(self):
		self.running = True
		self.index = 0
		self.tv = [ [], [], [] ]
		
		try:
			self.MAXTIME = int(DURATION.get())
			#self.MINY = int(TMIN.get())
			#self.MAXY = int(TMAX.get())
			
			g.setWorld(0, self.MINY, self.MAXTIME, self.MAXY,_('Time in second'),_('C & RH '))
			self.TIMER = int(TGAP.get())
			Total.config(state=DISABLED)
			Dur.config(state=DISABLED)
			self.msg(_('Starting the Measurements'))
			root.after(self.TIMER, self.update)
		except:
			self.msg(_('Failed to Start'))

	def stop(self):
		self.running = False
		Total.config(state=NORMAL)
		Dur.config(state=NORMAL)
		self.msg(_('User Stopped the measurements'))

	def update(self):
		if self.running == False:
			return
		t,v = p.get_voltage_time(3)  # Read IN1 for time
		if len(self.tv[0]) == 0:
			self.start_time = t
			elapsed = 0
		else:
			elapsed = t - self.start_time
		self.tv[0].append(elapsed)
		
		cap = p.measure_cap()
		self.tv[1].append(cap)
		

		if cap< 180: 
         		RH= (cap -163)/0.3
		elif 180<cap<186: 
        		RH= (cap -160.25)/0.375
		elif 186<cap<195: 
        		RH= (cap -156.75)/0.425
		else:
			RH= (cap -136.5)/0.65


		self.tv[2].append(RH)
		if len(self.tv[0]) >= 2:
			g.delete_lines()
			
			g.line(self.tv[0], self.tv[1],1)    # red line - Capacity in pF
			g.line(self.tv[0], self.tv[2],2)	# blue line - Relative Humidity in %
		if elapsed > self.MAXTIME:
			self.running = False
			Total.config(state=NORMAL)
			Dur.config(state=NORMAL)
			self.msg(_('Completed the Measurements'))
			return 
		root.after(self.TIMER, self.update)

	
	def save(self):
		try:
			fn = filename.get()
		except:
			fn = 'Humidiy.dat'
		p.save([self.tv],fn)
		self.msg(_('Data saved to %s')%fn)

	def clear(self):
		if self.running == True:
			return
		self.nt = [ [], [] ]
		g.delete_lines()
		self.msg(_('Cleared Data and Trace'))

	def msg(self,s, col = 'blue'):
		msgwin.config(text=s, fg=col)

	def quit(self):
		#p.set_state(10,0)
		sys.exit()

p = eyes.open()
p.disable_actions()

root = Tk()
Canvas(root, width = WIDTH, height = 5).pack(side=TOP)  

g = eyeplot.graph(root, width=WIDTH, height=HEIGHT, bip=False)
pt = humidity()

cf = Frame(root, width = WIDTH, height = 10)
cf.pack(side=TOP,  fill = BOTH, expand = 1)

b3 = Label(cf, text = _('Read Every'))
b3.pack(side = LEFT, anchor = SW)
TGAP = StringVar()
Dur =Entry(cf, width=5, bg = 'white', textvariable = TGAP)
TGAP.set('500')
Dur.pack(side = LEFT, anchor = SW)
b3 = Label(cf, text = _('mS,'))
b3.pack(side = LEFT, anchor = SW)
b3 = Label(cf, text = _('for total'))
b3.pack(side = LEFT, anchor = SW)
DURATION = StringVar()
Total =Entry(cf, width=5, bg = 'white', textvariable = DURATION)
DURATION.set('100')
Total.pack(side = LEFT, anchor = SW)
b3 = Label(cf, text = _('Seconds.'))
b3.pack(side = LEFT, anchor = SW)

b3 = Label(cf, text = _('Range'))
b3.pack(side = LEFT, anchor = SW)

'''
