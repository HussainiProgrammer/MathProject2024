from customtkinter import *


from PIL import ImageTk, Image
import os 
import threading


from tkinter import Text , Label, Frame


import tkinter.font as fonts
import matplotlib.pyplot as plt



from CTkMessagebox import *

print('\u03c0')
import json

from problems import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from geopy.distance import geodesic
import math
import mandlebrot_set
import unit_circle
import threading

class PointPickerApp:
    def __init__(self, root):
        self.root = root
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.points = []
        self.earth_radius = 20
        self.sun_point = [50, 50]
        self.animation_in_progress = False

        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)

        self.plot_points()  # Plot initial points and set limits

    def on_click(self, event):
        if self.animation_in_progress:
            return  # Disable adding points during animation
        if event.button == 1:  # Left mouse button
            x = event.xdata
            y = event.ydata
            self.star = (x,y)
            self.sun = (50,50)
            self.earth = (70,50)
            if x is not None and y is not None and 1 <= x <= 100 and 1 <= y <= 100:
                self.points.append((x, y))
                self.plot_points()  # Update plot when point is added

    def on_key_press(self, event):
        if event.key == 'k':
            if not self.animation_in_progress:
                print(self.sun,self.earth,self.star)
                self.animation_in_progress = True
                print('hi')
                self.ax.scatter(70, 50, color='blue', s=200, marker='o', label='New Earth')
                self.animate_earth_move()
                dist_A_B = geodesic(self.sun, self.earth).kilometers
                dist_B_C = geodesic(self.earth, self.star).kilometers
                dist_C_A = geodesic(self.star, self.sun).kilometers

                angle_A = np.arccos((dist_B_C**2 + dist_C_A**2 - dist_A_B**2) / (2 * dist_B_C * dist_C_A))
                angle_B = np.arccos((dist_C_A**2 + dist_A_B**2 - dist_B_C**2) / (2 * dist_C_A * dist_A_B))
                angle_C = np.arccos((dist_A_B**2 + dist_B_C**2 - dist_C_A**2) / (2 * dist_A_B * dist_B_C))

                angle_A_deg = np.degrees(angle_A)
                angle_B_deg = np.degrees(angle_B)
                angle_C_deg = np.degrees(angle_C)

                print("Angle A:", angle_A_deg)
                print("Angle B:", angle_B_deg)
                print("Angle C:", angle_C_deg)
                distance =1/math.tan(angle_A)
                self.ax.set_title(f'The Distance From The Earth To The Star Is :  {round(1/math.tan(angle_A),3)} AU')
                plt.rcParams['toolbar'] = 'None' 
                plt.rcParams["font.family"] = "serif"
                plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
                plt.rcParams["mathtext.default"] = "regular"

                plt.close("all")
                figure = plt.figure(figsize=(7,3)) 
                ay = figure.add_subplot(111)
                ay.get_xaxis().set_visible(False)
                ay.get_yaxis().set_visible(False)
                expression = r"$\tan(\theta) = \frac{1}{d} \rightarrow d = \frac{1}{\tan(\theta)} \rightarrow d = \frac{1}{{\text{{variable}}}} \rightarrow d = \text{{results}}$"

                ay.spines["right"].set_visible(False)
                ay.spines["left"].set_visible(False)
                ay.spines["top"].set_visible(False)
                ay.spines["bottom"].set_visible(False)
                x = angle_A
                plt.text(0,0, "$tan(\\theta) $ $=$ $ \\frac{1AU}{d} \\longrightarrow d $ $=$ $ \\frac{1AU}{tan(\\theta)}$\n$d$ $=$ $\\frac{1AU}{tan(" + str(round(x,3)) + ")}$ $=$ $\\frac{1AU}{" + str(round(math.tan(x),3)) + "}$ $=$ $" + str(round(1/math.tan(x),3))+ " AU$", fontsize=32)
                plt.figure(figure.number)
                plt.show()

    def animate_earth_move(self):
        step = np.pi / 180  # Smaller step for faster animation

        # Plot the Sun
        sun_artist = self.ax.scatter(self.sun_point[0], self.sun_point[1], color='yellow', s=400, marker='o')

        # Set initial limits
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        angle = 0

        # Plot the Earth at (70, 50)
        new_earth_artist = self.ax.scatter(70, 50, color='blue', s=200, marker='o', label='New Earth')

        while angle <  np.pi:  # Travel half circle
            # Calculate new Earth position based on circular motion
            earth_x = 50 + self.earth_radius * np.cos(angle)
            earth_y = 50 + self.earth_radius * np.sin(angle)

            # Ensure Earth coordinates are within the range 1 to 100
            earth_x = max(min(earth_x, 100), 1)
            earth_y = max(min(earth_y, 100), 1)

            # Clear the axis to remove all elements from the plot
            self.ax.clear()

            # Reapply the initial limits
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)

            # Plot the Sun
            self.ax.scatter(self.sun_point[0], self.sun_point[1], color='yellow', s=400, marker='o')

            # Plot the Earth at (70, 50)
            self.ax.scatter(70, 50, color='green', s=200, marker='o', label='New Earth')

            # Plot the Earth
            self.ax.scatter(earth_x, earth_y, color='green', s=200, marker='o', label='Earth')
            

            # Connect Earth with the Sun
            self.ax.plot([self.sun_point[0], earth_x], [self.sun_point[1], earth_y], color='white', linestyle='--')

            # Plot the stars
            for x, y in self.points:
                self.ax.plot([earth_x, x], [earth_y, y], color='white', linestyle='--')
                self.ax.plot([50, x], [50, y], color='white', linestyle='--')
                self.ax.plot([70, x], [50, y], color='white', linestyle='--')
                self.ax.plot([50, 70], [50, 50], color='white', linestyle='--')
                

            self.ax.set_title('Click to Add Stars')
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.grid(True)
            self.ax.legend()

            self.fig.canvas.draw_idle()
            self.root.update()  # Update the Tkinter GUI

            angle += step+.05

        sun_artist.remove()
        new_earth_artist.remove()

        # After completing the animation, plot the new version of Earth at (70, 50)
        self.ax.scatter(70, 50, color='green', s=200, marker='o', label='New Earth')
        

        self.fig.canvas.draw_idle()
        self.root.update()  # Update the Tkinter GUI

        self.animation_in_progress = False


    def plot_points(self):
        self.ax.clear()
        if self.points:
            xs, ys = zip(*self.points)
            self.ax.scatter(xs, ys, color='blue')

        # Plot the Sun
        sun_artist = self.ax.scatter(self.sun_point[0], self.sun_point[1], color='yellow', s=400, marker='o', label='Sun')

        # Remove the previous Earth point
        if hasattr(self, 'earth_artist'):
            self.earth_artist.remove()

        # Plot the new Earth point
        self.earth_artist = self.ax.scatter(70, 50, color='green', s=200, marker='o', label='Earth')

        # Plot the stars
        for x, y in self.points:
            self.ax.plot([70, x], [50, y], color='white', linestyle='--')
            self.ax.plot([50, 70], [50, 50], color='white', linestyle='--')
            self.ax.plot([50, x], [50, y], color='white', linestyle='--')

        # Set limits to ensure all elements are visible
        self.ax.set_xlim(1, 100)
        self.ax.set_ylim(1, 100)

        self.ax.set_title('Click to Add Stars')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()






abtUs = '''ثانوية الذرى للمتميزين 


      طلاب الرابع علمي



بأشراف : الاستاذ محمد سمير  
الاستاذ علي خالد   


Programming Team

رضا حسن هادي

حسين علاء مصطفى


Designers

حسين ماهر عبدالصاحب

سجاد علي عبد عبدالحسين

'''



correct_color = '#33FF57'


error_color = '#FF3333'


button_color = '#00845e'


hover_color = '#009c70'


text_color = '#cccccc'



def quit_root(): threading.Thread(target=root.quit()).start


def NewFrame():return CTkFrame(root, height=800, width=500)


def view3DModule(element: str): os.system(f'"{path}/DataBase/3D Elements/{element}.glb"')


def validate_input(text):


    if text.count('.') > 1 or any(c not in '0123456789.πpi*/' for c in text):


        return False


    return True


def on_entry_click(event):valuesEntery.configure(validate="key", validatecommand=validate_cmd)



quantities = ["Central Angle", "Angle", "Sine", "Cosine", "Tangent", "Arc Length", "Side Length", "Radius", "Area"]

quantities_units = {
    "Central Angle": ["Degrees", "Radians"],
    "Angle": ["Degrees", "Radians"],
    "Sine": ["None"],
    "Cosine": ["None"],
    "Tangent": ["None"],
    "Arc Length": ["m", "cm", "km", "unit"],
    "Side Length": ["m", "cm", "km", "unit"],
    "Radius": ["m", "cm", "km", "unit"],
    "Area": ["m²", "cm²", "unit²"],
}

def get_sol():
    with open(path+"\\values.json",'r+',encoding="utf8") as file:
        file.truncate(0)
        data = {
            "order":[],
            "count":0,
            "count_required":0
        }
        json.dump(data,file,indent=4)

    widgets = givenValuesFrame.winfo_children()
    values = []

    for i in widgets:
        for w in i.winfo_children():
            if w.cget('text') != "X":
                values.append(w.cget('text').split(':'))

    for index, value in enumerate(values):
        quan = value[0]
        val = value[1].split('in')[1].split()[0]
        unit = value[1].split('in')[1].split()[1].replace("None", "")
        obj = value[2]

        with open(path+"\\values.json",'r+',encoding="utf8") as file:
                JSON_FILE = json.load(file)
                count = int(JSON_FILE["count"]) + 1

                data = {f"value{count}": {"Quantity":quan, "Value":val, "Unit":unit, "Object":obj}}

                JSON_FILE.update(data)
                JSON_FILE["count"] = count
                JSON_FILE["order"].append(f'value{count}')

                file.seek(0)
                json.dump(JSON_FILE,file,indent=4)

        values[index] = [quan, val, unit, obj]
            
    widgets2 = requiredValuesFrameBar.winfo_children()
    requireds = []

    for i in widgets2:
        for w in i.winfo_children():
            if w.cget('text') != "X":
                requireds.append(w.cget('text').split(':'))

    for index, require in enumerate(requireds):
        quan2 = require[0]
        unit2 = require[1].replace(" in ", "").replace("None", "")
        obj2 = require[2]

        with open(path+"\\values.json",'r+',encoding="utf8") as file:
            JSON_FILE = json.load(file)
            count2 = int(JSON_FILE["count_required"]) + 1

            data = {f"required{count2}": {"Quantity":quan2, "Unit":unit2, "Object":obj2}}

            JSON_FILE.update(data)
            JSON_FILE["count_required"] = count2
            JSON_FILE["order"].append(f'required{count2}')

            file.seek(0)
            json.dump(JSON_FILE,file,indent=4)

        requireds[index] = [quan2, unit2, obj2]

    text, unit_circle_values = getSolution(values, requireds)
    
    plt.close("all")

    figure = plt.figure(figsize=(7,5))
    ax = figure.add_subplot(111)
    
    plt.rcParams['toolbar'] = 'None' 
    ax.text(0, 0, f"${text}$", fontsize=36).set_color("#000000")

    figure.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    plt.show()

    for c in unit_circle_values:
        if c.quantity == "Central Angle":
            if c.unit == "Degrees": unit_circle.showAngle(unit_circle.degreesToAngle(c.value))
            else: unit_circle.showAngle(unit_circle.radiansToAngle(c.value))
        elif c.quantity == "Tangent": unit_circle.showAngle(unit_circle.getAnglesByTangent(c.value))
        elif c.quantity == "Sine": unit_circle.showAngle(unit_circle.getAnglesBySine(c.value))
        elif c.quantity == "Cosine": unit_circle.showAngle(unit_circle.getAnglesByCosine(c.value))

        plt.grid(color="#000000")
        plt.show()

def showUnitCircle():
    with open(path+"\\values.json",'r+',encoding="utf8") as file:
        file.truncate(0)
        data = {
            "order":[],
            "count":0,
            "count_required":0
        }
        json.dump(data,file,indent=4)

    widgets = givenValuesFrame.winfo_children()
    values = []

    for i in widgets:
        for w in i.winfo_children():
            if w.cget('text') != "X":
                values.append(w.cget('text').split(':'))

    for index, value in enumerate(values):
        quan = value[0]
        val = value[1].split('in')[1].split()[0]
        unit = value[1].split('in')[1].split()[1].replace("None", "")
        obj = value[2]

        with open(path+"\\values.json",'r+',encoding="utf8") as file:
                JSON_FILE = json.load(file)
                count = int(JSON_FILE["count"]) + 1

                data = {f"value{count}": {"Quantity":quan, "Value":val, "Unit":unit, "Object":obj}}

                JSON_FILE.update(data)
                JSON_FILE["count"] = count
                JSON_FILE["order"].append(f'value{count}')

                file.seek(0)
                json.dump(JSON_FILE,file,indent=4)

        values[index] = [quan, val, unit, obj]
            
    widgets2 = requiredValuesFrameBar.winfo_children()
    requireds = []

    for i in widgets2:
        for w in i.winfo_children():
            if w.cget('text') != "X":
                requireds.append(w.cget('text').split(':'))

    for index, require in enumerate(requireds):
        quan2 = require[0]
        unit2 = require[1].replace(" in ", "").replace("None", "")
        obj2 = require[2]

        with open(path+"\\values.json",'r+',encoding="utf8") as file:
            JSON_FILE = json.load(file)
            count2 = int(JSON_FILE["count_required"]) + 1

            data = {f"required{count2}": {"Quantity":quan2, "Unit":unit2, "Object":obj2}}

            JSON_FILE.update(data)
            JSON_FILE["count_required"] = count2
            JSON_FILE["order"].append(f'required{count2}')

            file.seek(0)
            json.dump(JSON_FILE,file,indent=4)

        requireds[index] = [quan2, unit2, obj2]

    text, unit_circle_values = getSolution(values, requireds)
    
    plt.close("all")

    for c in unit_circle_values:
        if c.quantity == "Central Angle":
            if c.unit == "Degrees": unit_circle.showAngle(unit_circle.degreesToAngle(c.value))
            else: unit_circle.showAngle(unit_circle.radiansToAngle(c.value))
        elif c.quantity == "Tangent": unit_circle.showAngle(unit_circle.getAnglesByTangent(c.value))
        elif c.quantity == "Sine": unit_circle.showAngle(unit_circle.getAnglesBySine(c.value))
        elif c.quantity == "Cosine": unit_circle.showAngle(unit_circle.getAnglesByCosine(c.value))

        plt.grid(color="#000000")
        plt.show()

def changeFrame(newFrame: CTkFrame):


    frames: list[CTkFrame] = [AboutFrame, HomeFrame, problemsFrame, mandlebrotSetFrame]


    frames.remove(newFrame)



    newFrame.place(relx=0.239, rely=0.03, relwidth=0.4 * 1.8, relheight=(0.3999*3) - 0.2688)


    for frame in frames: frame.place_forget()
 


def addValues():


    if quantityMenuButton.get() == "Quantity" or not valuesEntery.get() or   unitsMenuButton.get() == "Unit" or not objectsEntery.get():CTkMessagebox(title="Error", message='Please enter a useful vaule!',icon='cancel', font=Desired2_font)


    else:
        _ = valuesEntery.get().replace('π','pi')
        frame = CTkFrame(givenValuesFrame,width=300,height=65);frame.pack(padx=5,pady=10, fill=X);CTkLabel(frame,text=f'{quantityMenuButton.get()}: in {_} {unitsMenuButton.get()}: {objectsEntery.get()}',font=Desired2_font).pack(side=LEFT,padx=10,pady=5);CTkButton(frame,fg_color=error_color,hover_color='#eb4034',text="X",font=Desired2_font,width=50,command=lambda: frame.destroy()).pack(side=RIGHT, padx=10,pady=5)



def addValues2():


    if quantityMenuButton2.get() == "Quantity"  or   unitsMenuButton2.get() == "Unit" or not objectsEntery2.get():CTkMessagebox(title="Error", message='Please enter a useful vaule!',icon='cancel', font=Desired2_font)


    else:frame = CTkFrame(requiredValuesFrameBar,width=300,height=65);frame.pack(padx=5,pady=10, fill=X);CTkLabel(frame,text=f'{quantityMenuButton2.get()}: in {unitsMenuButton2.get()}: {objectsEntery2.get()}',font=Desired2_font).pack(side=LEFT,padx=10,pady=5);CTkButton(frame,fg_color=error_color,hover_color='#eb4034',text="X",font=Desired2_font,width=50,command=lambda: frame.destroy()).pack(side=RIGHT, padx=10,pady=5)



def unit_quant(choice):


    units = quantites_units[choice]


    unitsMenuButton.configure(state=ACTIVE, values = units)


def unit_quant2(choice):


    units = quantites_units[choice]


    unitsMenuButton2.configure(state=ACTIVE, values = units)


#=========================== OLD CODE ====================================
path = os.path.dirname(__file__)


root = CTk()


root.geometry('1100x600+150+50')


root.minsize(width=1050, height=600)


root.title('Math Project')


root.protocol("WM_DELETE_WINDOW", quit_root)



validate_cmd = (root.register(validate_input), '%P')



"""img = ImageTk.PhotoImage(Image.open(path+'\\Data\\widgets images\\Chmicon.ico'))


root.iconphoto(False,img)"""



Desired_font = CTkFont(family="Comic Sans MS", size=30,)


Desired2_font = CTkFont(family="Comic Sans MS", size=20,)


Desired3_font = CTkFont(family="Comic Sans MS", size=50,)


Desired4_font = CTkFont(family="Comic Sans MS", size=50,)


Desired5_font = CTkFont(family="Comic Sans MS", size=35,)


Desired6_font = CTkFont(family="Comic Sans MS", size=40,)




HomeFrame = CTkFrame(root, height=800, width=500)


HomeFrame.place(relx=0.239, rely=0.03, relwidth=0.4 *


                1.8, relheight=(0.3999*3) - 0.2688)



MenuFrame = CTkFrame(root, corner_radius=4, height=3000, width=100)


MenuFrame.place(relx=.0, rely=.0, relwidth=.2001)


AboutFrame = CTkFrame(root, height=800, width=500)

mandlebrotSetFrame = CTkFrame(root, height=800, width=500)

figure = mandlebrot_set.getFigure()

canvas = FigureCanvasTkAgg(figure, master=mandlebrotSetFrame)
canvas.draw()
canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

# Add Matplotlib toolbar (optional)
toolbar = NavigationToolbar2Tk(canvas, mandlebrotSetFrame)
toolbar.update()
canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

HomesButton = CTkButton(MenuFrame, corner_radius=7, text='Trigonometry', font=Desired2_font, height=40, width=140, command=lambda: changeFrame(problemsFrame),fg_color=button_color,hover_color=hover_color,text_color=text_color)
HomesButton.place(relx=0.06666, rely=0.011, relheight=.017, relwidth=.87575)

AboutButton = CTkButton(MenuFrame, corner_radius=7, text='About Us', font=Desired2_font, height=60, width=140, command=lambda: changeFrame(AboutFrame),fg_color=button_color,hover_color=hover_color,text_color=text_color)


AboutButton.place(relx=0.06666, rely=0.061+0.025, relheight=.017, relwidth=.87575)



AButton = CTkButton(MenuFrame, corner_radius=7, text='Astronomy', font=CTkFont(family="Comic Sans MS", size=20,), height=40, width=140, command=lambda: changeFrame(HomeFrame),fg_color=button_color,hover_color=hover_color,text_color=text_color)


AButton.place(relx=0.06666, rely=0.061, relheight=.017, relwidth=.87575)



mandlebrotSetButton = CTkButton(MenuFrame, corner_radius=7, text='Mandlebrot Set', font=Desired2_font, height=40, width=140, command=lambda: changeFrame(mandlebrotSetFrame),fg_color=button_color,hover_color=hover_color,text_color=text_color)


mandlebrotSetButton.place(relx=0.06666, rely=0.036, relheight=.017, relwidth=.87575)



_f = fonts.Font(family="Courier", size=40, weight='bold')


AbtUsText = Text(AboutFrame, height=10,font=_f,  width=50, foreground='silver',  background='#2b2b2b', bd=0, border=0, borderwidth=0)



AbtUsText.place(relx=0.024, rely=0.0244,


                relheight=.97575, relwidth=0.99575)


AbtUsText.delete("1.0", "end")


AbtUsText.insert(END,abtUs)


AbtUsText.configure(state=DISABLED)



#=========================== END OLD CODE ====================================


#=========================== NEW CODE ========================================



problemsFrame = CTkFrame(root, height=800, width=500, fg_color='#2b2b2b')



valuesFrame = CTkFrame(problemsFrame,width=300,height=50,fg_color='#242424')


valuesFrame.place(relx=0.05004, rely=0.01, relheight=.117, relwidth=.887575)





CTkLabel(valuesFrame, text="Given Values", font=Desired2_font).pack(side=LEFT,padx=12,pady=5)


quantityMenuButton = CTkOptionMenu(valuesFrame,values=quantities,height=50,width=0, font=Desired2_font, button_color='#2b2b2b', fg_color='#2b2b2b', button_hover_color='#363434',command=unit_quant)


quantityMenuButton.pack(side=LEFT,padx = 10 , pady= 5)


quantityMenuButton.set("Quantity")



valuesEntery = CTkEntry(valuesFrame,width=70,height=50, fg_color='#2b2b2b',border_color='#2b2b2b', font=Desired2_font,placeholder_text="Value")


valuesEntery.pack(side=LEFT,padx = 10 , pady= 5)


valuesEntery.bind("<FocusIn>", on_entry_click)





unitsMenuButton = CTkOptionMenu(valuesFrame,height=50,width=0, font=Desired2_font, button_color='#2b2b2b', fg_color='#2b2b2b', button_hover_color='#363434',state=DISABLED)


unitsMenuButton.pack(side=LEFT,padx = 10 , pady= 5)


unitsMenuButton.set("Unit")



objectsEntery = CTkEntry(valuesFrame,width=100,height=50, fg_color='#2b2b2b',border_color='#2b2b2b', font=Desired2_font,placeholder_text="Objects")


objectsEntery.pack(side=LEFT,padx = 10 , pady= 5)



addValueButton = CTkButton(valuesFrame,text='+',font=Desired3_font,command=addValues,fg_color=button_color,hover_color=hover_color,text_color=text_color)


addValueButton.pack(side=LEFT,padx=10,pady=5)




givenValuesFrame = CTkScrollableFrame(problemsFrame,width=300,height=50,fg_color='#242424')


givenValuesFrame.place(relx=0.05004, rely=0.134, relwidth=.887575)




requiredValuesFrame = CTkFrame(problemsFrame,width=300,height=50,fg_color='#242424')


requiredValuesFrame.place(relx=0.05004, rely=0.5, relheight=.117, relwidth=.887575)





CTkLabel(requiredValuesFrame, text="Required Values", font=Desired2_font).pack(side=LEFT,padx=10,pady=5)


quantityMenuButton2 = CTkOptionMenu(requiredValuesFrame,values=quantities,height=40,width=0, font=Desired2_font, button_color='#2b2b2b', fg_color='#2b2b2b', button_hover_color='#363434',command=unit_quant2)


quantityMenuButton2.pack(side=LEFT,padx = 10 , pady= 5)


quantityMenuButton2.set("Quantity")




unitsMenuButton2 = CTkOptionMenu(requiredValuesFrame,height=40,width=0, font=Desired2_font, button_color='#2b2b2b', fg_color='#2b2b2b', button_hover_color='#363434',state=DISABLED)


unitsMenuButton2.pack(side=LEFT,padx = 10 , pady= 5)


unitsMenuButton2.set("Unit")



objectsEntery2 = CTkEntry(requiredValuesFrame,width=100,height=40, fg_color='#2b2b2b',border_color='#2b2b2b', font=Desired2_font,placeholder_text="Objects")


objectsEntery2.pack(side=LEFT,padx = 10 , pady= 5)



addValueButton2 = CTkButton(requiredValuesFrame,text='+',font=Desired3_font,text_color=text_color


                            ,command=addValues2,fg_color=button_color,hover_color=hover_color)


addValueButton2.pack(side=LEFT,padx=10,pady=5)



requiredValuesFrameBar = CTkScrollableFrame(problemsFrame,width=300,height=40,fg_color='#242424')


requiredValuesFrameBar.place(relx=0.05004, rely=0.62, relwidth=.887575)



solButton = CTkButton(problemsFrame,text="Get Soulutions", font=Desired2_font, height=40,


                      command=get_sol,fg_color=button_color,hover_color=hover_color,text_color=text_color)


solButton.place(relx=0.05004, rely=0.92, relwidth=.887575/2)

cirButton = CTkButton(problemsFrame,text="Show Unit Circles", font=Desired2_font, height=40,


                      command=showUnitCircle,fg_color=button_color,hover_color=hover_color,text_color=text_color)


cirButton.place(relx=0.05004*10, rely=0.92, relwidth=.887575/2)

ploter = PointPickerApp(HomeFrame)


root.mainloop()



"""widgets = givenValuesFrame.winfo_children()


values = []


for i in widgets:


    for widget in i.winfo_children():


        values.append(widget.cget('text').split(':'))



for value in values:


    if value == ["X"]:value.remove("X")


    else: 


        quan = value[0]


        val = value[1].split('in')[0]


        unit = value[1].split('in')[1]


        obj = value[2]


        print(quan,val,unit,obj)
        
"""