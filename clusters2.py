# Joseph Velez 2019
# Based on the Java Applet by 
#   Chris Mihos (mihos@case.edu)
#   Department of Astronomy
#   Case Western Reserve University

from Tkinter import *
from PIL import Image, ImageTk, ImageDraw
import ttk

#======================================
class DataPoint: # Rewriteable (x, y) tuple
    x = 0.0
    y = 0.0
    
    def __init__(self, nx, ny):
        try:
            self.x = float(nx)
            self.y = float(ny)
        except:
            pass

#======================================
class ClusterClass(): # Stores cluster data and provides the very important translate method
    def __init__(self, _name, _bvStart, _vstart, _ebv, _image, _comment):
        self.xStart, self.yStart = 62, 563
        self.DX, self.DBV, self.DY, self.DV = 37.0, 0.2, 401.0, 10.0
        self.name, self.bvStart, self.vStart, self.ebv, self.image, self.comment = _name, _bvStart, _vstart, _ebv, _image, _comment
        self.xMapSlope = self.DBV / self.DX;
        self.xMapInter = self.bvStart - self.DBV * self.xStart / self.DX
        self.yMapSlope = self.DV / self.DY
        self.yMapInter = self.vStart - self.DV * self.yStart / self.DY
        
    def translate(self, x, y):
        newX = self.xMapSlope * x + self.xMapInter
        newY = self.yMapSlope * y + self.yMapInter
        return DataPoint(newX, newY)

#======================================
def initClusters(): # Create a dictionary of cluster data, accessable via the same string used in cluster selection
    clusters = {}
    clusters["M 67"]     = ClusterClass("M 67",     -0.3, 21.0, 0.04, "m67.gif","")
    clusters["M 45"]     = ClusterClass("M 45",     -0.7, 14.5, 0.03, "m45.gif","Pleiades")
    clusters["M 44"]     = ClusterClass("M 44",     -0.3, 15.5, 0,    "m44.gif","Praesepe")
    clusters["M 25"]     = ClusterClass("M 25",     -0.3, 17.5, 0.5,  "m25.gif","")
    clusters["NGC 752"]  = ClusterClass("NGC 752",  -0.5, 17.5, 0.03, "ngc752.gif","")
    clusters["NGC 6791"] = ClusterClass("NGC 6791", -0.3, 23.5, 0.20, "ngc6791.gif","")
    clusters["NGC 7044"] = ClusterClass("NGC 7044",  0.3, 23,   0.7,  "ngc7044.gif","")
    clusters["Mel 20"]   = ClusterClass("Mel 20",   -0.7, 13.5, 0.09, "mel20.gif","alpha Persei")
    clusters["zams"]     = ClusterClass("zams",     -0.5,  7.5, 0.0,  "zams2.gif", "")
    return clusters

#======================================
def display(*args): # This function will redraw the cluster, add ZAMS and crosshairs as needed, and calculate and show the data values
    debug = 0
    global clusterDict, bvo, zOffset
    XgraphicCorrection, YgraphicCorrection = -3, 0
    background = Image.open(clusterDict[cluster_text.get()].image).convert("RGBA")
    # If selected cluster image is not available, the program will throw an error but should not crash
    bvo.set("")
    bv.set("")
    v.set("")
    mv.set("")
    # If ZAMS is not turned on, do not display ZAMS grid, crosshairs, or output data
    if zams_text.get() == "on":
        foreground = Image.open("zams2.gif").convert("RGBA")
        # If anything goes wrong with the images or the calculation, throw an error to the console
        try:
            background.paste(foreground, (int(zOffset.x), int(zOffset.y) * -1), foreground) # Watermark zams2.gif over cluster
            if clk.x > 0.0 and clk.x < 575.0 and clk.y > 0.0 and clk.y < 575.0:
                crosshair = Image.open("crosshair.gif").convert("RGBA")
                crossX = int(clk.x) + XgraphicCorrection # Compensates for differences between the crosshair image center and the mouse pointer
                crossY = int(clk.y) + YgraphicCorrection
                background.paste(crosshair, (crossX - 575, crossY - 575), crosshair)
                # Calculate the output data
                clusterDatum = clusterDict[cluster_text.get()].translate(crossX, crossY + 50)
                zamsDatum = clusterDict["zams"].translate(crossX - int(zOffset.x), crossY - int(zOffset.y) + 50)
                ebv = clusterDict[cluster_text.get()].ebv
                bvo.set("B-Vo = " + dataString(clusterDatum.x - ebv))
                bv.set("B - V = " + dataString(clusterDatum.x))
                v.set("V = " + dataString(clusterDatum.y))
                mv.set("Mv = " + dataString(zamsDatum.y))
        except Exception as e:
            print(e)
    # Display the composite image and the cluster comment
    img = ImageTk.PhotoImage(image=background)
    imgArea.configure(image=img)
    imgArea.image = img
    comment_text.set(clusterDict[cluster_text.get()].comment)
    
#======================================
def dataString(n):
    return str(round(n, 2))
    
#======================================
def clicked(event): # Capture mouse click within the program
    global clk
    clk = DataPoint(event.x, event.y)
    display()
    
#======================================
def zamsAdjust(x, y):
    global zOffset
    if x > 0 and zOffset.x + x > 400:
        x = 400 - zOffset.x
    if x < 0 and zOffset.x - x < -350:
        x = -350 - zOffset.x
    if y > 0 and zOffset.y + y > 350:
        y = 350 - zOffset.y
    if y < 0 and zOffset.y - y < -350:
        y = -350 - zOffset.y
    zOffset = DataPoint(zOffset.x + x, zOffset.y + y)
    display()
    
#======================================
def zamsAdjust_ypA():
    zamsAdjust(0, 10)
    
#======================================
def zamsAdjust_yp1():
    zamsAdjust(0, 1)
    
#======================================
def zamsAdjust_ym1():
    zamsAdjust(0, -1)
    
#======================================
def zamsAdjust_ymA():
    zamsAdjust(0, -10)
    
#======================================
def zamsAdjust_xmA():
    zamsAdjust(-10, 0)
    
#======================================
def zamsAdjust_xm1():
    zamsAdjust(-1, 0)
    
#======================================
def zamsAdjust_xp1():
    zamsAdjust(1, 0)
    
#======================================
def zamsAdjust_xpA():
    zamsAdjust(10, 0)
    
#==============================================================================
# Initialize the form
window = Tk()
window.option_add("*font", "helvetica 11" )
window.title("Cluster Lab")
window.geometry("775x575")
window.resizable(0, 0)
clk = DataPoint(-1, -1)
zOffset = DataPoint(-10, 20)

# Initialize the Label that displays the cluster graph (it must have a graphic to start)
img = PhotoImage(file="zams2.gif")
imgArea = Label(window, width=575, height=575)
imgArea.bind("<Button-1>", clicked)
imgArea.image = img
imgArea.pack(side="left")

# Create and set defaults for the controls and labels.
# The textvariable flag assigns tkinter constructs to the obect, allowing us set values without an explicit global context. 
# The .trace method allows us to listen for changes to the textvariable, such as user input.

# Cluster controls
Label(window, text="Choose a cluster:").pack()
cluster_text = StringVar()
cluster_text.set("M 67")
clusterSelect = ttk.Combobox(window, textvariable=cluster_text, state="readonly", values=["M 67", "M 45", "M 44", "M 25", "NGC 752", "NGC 6791", "NGC 7044", "Mel 20"])
# Explicitly sets the cluster name values. A more clever version could use a loop to set the values implicitly.
clusterSelect.pack()
cluster_text.trace("w", display)
comment_text = StringVar()
clusterComment = Label(window, textvariable=comment_text)
clusterComment.pack()

# ZAMS controls: on/off and adjustment
Label(window, text="\nZAMS is: ").pack()
zams_text = StringVar()
zams_text.set("off")
zamsSelect = ttk.Combobox(window, textvariable=zams_text, state="readonly", values=["off", "on"])
zamsSelect.pack()
zams_text.trace("w", display)
adjustFrame = Frame(window)
adjustFrame.pack()
ypA = Button(adjustFrame, text="+10", command=zamsAdjust_ypA)
yp1 = Button(adjustFrame, text="+1 ", command=zamsAdjust_yp1)
xmA = Button(adjustFrame, text="-10", command=zamsAdjust_xmA)
xm1 = Button(adjustFrame, text="-1", command=zamsAdjust_xm1)
xp1 = Button(adjustFrame, text="+1", command=zamsAdjust_xp1)
xpA = Button(adjustFrame, text="+10", command=zamsAdjust_xpA)
ym1 = Button(adjustFrame, text="-1", command=zamsAdjust_ym1)
ymA = Button(adjustFrame, text="-10", command=zamsAdjust_ymA)
ypA.grid(row=0, column=2)
yp1.grid(row=1, column=2)
xmA.grid(row=2, column=0)
xm1.grid(row=2, column=1)
xp1.grid(row=2, column=3)
xpA.grid(row=2, column=4)
ym1.grid(row=3, column=2)
ymA.grid(row=4, column=2)

# Output controls
Label(window, text="\n\nOUTPUT:\n").pack()
bvo = StringVar()
bvoLabel = Label(window, textvariable=bvo)
bvoLabel.pack()
bv = StringVar()
bvLabel = Label(window, textvariable=bv)
bvLabel.pack()
v = StringVar()
vLabel = Label(window, textvariable=v)
vLabel.pack()
mv = StringVar()
mvLabel = Label(window, textvariable=mv)
mvLabel.pack()

# Vanity
Label(window, text="\n\n\n\nJoseph Velez 2019", fg="lightgray").pack()

# Initialize the cluster dictionary and image display
clusterDict = initClusters()
display()

window.mainloop() # tkinter command to begin the GUI