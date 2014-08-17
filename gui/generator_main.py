from tkinter import *
from tkinter import ttk
import tkinter
import gurpsspace.dice as GD
import gurpsspace.starsystem as starsys


class StarSystemOverview(tkinter.Frame):
	

	def __init__(self, parent, mysys = None):

		width = parent.winfo_screenwidth() / 4 
		height = parent.winfo_screenheight() / 4
		offset_x = (parent.winfo_screenwidth() / 2) - (width / 2)
		offset_y = (parent.winfo_screenheight() / 2) - (height / 4)
		# Geometry is a string of the format 'WxH+offset_x+offset_y' where the offsets are calculated on Linux from the top right corner
		#parent.geometry(str(width) + 'x' + str(height) + '-' + str(offset_x) + '+' + str(offset_y))
		#parent.geometry('-' + str(offset_x) + '+' + str(offset_y))

		mainframe = ttk.Frame(parent)

		ttk.Label(parent, text="Star System Overview", anchor=CENTER).pack(side=TOP, fill="x", expand=False, padx=50, pady=20)

		if mysys == None:
			args = {
			    'opencluster': None, # True or False
			    'numstars': None, # 1, 2 or 3
			    'age': None # Number > 0
			}
			mysys = starsys.StarSystem(**args)

		if mysys._StarSystem__opencluster:
			openCluster = "Yes"
		else: 
			openCluster = "No"

		details = ttk.Frame(mainframe)
		details.pack(pady=10)
		ttk.Button(details, text="Stars Details", command= lambda: self.openStarsWindow(self, mysys)).pack(fill="x", expand=True, pady=5, side=LEFT)
		ttk.Button(details, text="Planets Details", command= lambda: self.openPlanetsWindow(self, mysys)).pack(fill="x", expand=True, pady=5, side=RIGHT)

		labels = ttk.Frame(mainframe)
		labels.pack(side=LEFT, pady=10)
		ttk.Label(labels, text="Age:", anchor=W).pack()
		ttk.Label(labels, text="# of Stars:", anchor=W).pack()
		ttk.Label(labels, text="Open Cluster:", anchor=W).pack()
		if mysys._StarSystem__numstars > 1:
			for i in range(len(mysys._StarSystem__orbits)):
				ttk.Label(labels, text="Companion Star " + str(i+1), anchor=W).pack(padx=10, pady=10)
				ttk.Label(labels, text="Stellar Orbit:", anchor=W).pack()
				ttk.Label(labels, text="Eccentricity:", anchor=W).pack()
				ttk.Label(labels, text="Minimum Stellar Orbit:", anchor=W).pack()
				ttk.Label(labels, text="Maximum Stellar Orbit:", anchor=W).pack()
				ttk.Label(labels, text="Orbital Period:", anchor=W).pack()

		values = ttk.Frame(mainframe)
		values.pack(side=RIGHT, pady=10)
		ttk.Label(values, text=str(round(mysys._StarSystem__age, 2)) + " billion years").pack(padx=10)
		ttk.Label(values, text=mysys._StarSystem__numstars).pack()
		ttk.Label(values, text=openCluster).pack()
		if mysys._StarSystem__numstars > 1:
			for i in range(len(mysys._StarSystem__orbits)):
				ttk.Label(values, text="--------------------").pack(padx=10, pady=10)
				ttk.Label(values, text=str(mysys._StarSystem__orbits[i][0]) + " AU", anchor=E).pack()
				ttk.Label(values, text=mysys._StarSystem__orbits[i][1], anchor=E).pack()
				ttk.Label(values, text=str(mysys._StarSystem__minmaxorbits[i][0]) + " AU", anchor=E).pack()
				ttk.Label(values, text=str(mysys._StarSystem__minmaxorbits[i][1]) + " AU", anchor=E).pack()
				ttk.Label(values, text=str(round(mysys._StarSystem__periods[i], 1)) + "d", anchor=E).pack()

		mainframe.pack()
		parent.update()

	def openStarsWindow(self, parent, mysys):
		tkMessageBox.showinfo("Placeholder", "Not implemented yet")

	def openPlanetsWindow(self, parent, mysys):
		tkMessageBox.showinfo("Placeholder", "Not implemented yet")