from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox 
from ttkbootstrap import *
import ttkbootstrap as tb
from PIL import ImageTk,Image # This library is used for actual image processing
from pathlib import Path # This library is used to traverse through the directories
from Startup_Processes import * # A Custom module to perform basic tasks
from Image_Handler import * # A Custom module for handling images

global filename # This variable will hold the path directory of the project file
global startup # This will be an object of Startup Processes which will be used to access various variables
global project_filename # This is the string values which is retrieved after the 
global start_editor # A variable to know if to start the main editor or not
global image_name # Variable to hold the name of the image
global image_loc # Variable to hold the path of the original image

image_name = "" # Declaring it to be an empty string

#image_obj_list = list() # This list holds all the image handler objects

#current_images = -1 # This variable will hold the current number of images present 

# Creating an object of Startup Processes Class
startup = Startup_Processes()

# This global variable will be assigned as the object of the image handler class
global main_image

# Basic window setup
root = tb.Window(themename = "darkly") # Set the theme of the application using pre-defined stylenames
root.title("IMX Image Editor") # sets the title of the window
root.iconbitmap("Dependencies/System_Images/logo4.ico") # iconbitmap() member function takese the path of the *.ico file which is to assigned as the icon of the application
root.resizable(False,False) # You can disable resizing on a window by passing two False arguments in the resizable method
root.geometry(startup.new_res_list[3]) # takes a string of resolution the form "widthxheight"
root.position_center() # positions the window in the center of the screen at the launch
root.update_idletasks() # it helps the application perform background tasks and continue even in case of user inactivity

# making a canvas equal to the dimensions of the window
canv = tk.Canvas(root,width = startup.new_res_list[4],height = startup.new_res_list[5])
canv.pack(fill = "both",expand = True)

# Opening the resized image to be applied as the background image in the intro menu
logo_img = ImageTk.PhotoImage(Image.open("Dependencies/System_Images/logo.png")) # ImageTk.PhotoImage() converts the image into tkinter supported format
canv.create_image(int(0.4 * startup.new_res_list[4]),int(0.125 * startup.new_res_list[5]),image = logo_img,anchor = "nw") # Displaying the image on the canvas with proper positioning

# Creating a top level for the main editor
def Main_Editor(project_filename):
    
    editor = Toplevel()
    editor.title("IMX Image Editor ~ " + str(project_filename))
    editor.geometry(startup.new_res_list[0])
    editor.iconbitmap("Dependencies/System_Images/logo4.ico")
    editor.state('zoomed')
    #editor.attributes('-fullscreen',True)
    editor.resizable(False,True)
    editor.position_center()
    
    # Creating one big canvas to hold other small canvases
    e_canv = tk.Canvas(editor,width = startup.new_res_list[1],height = startup.new_res_list[2])
    e_canv.pack(fill = "both",expand = True)
    
    # This rectangle will responsible for showing where area on the screen reserved for the image
    e_canv.create_rectangle(int(0.125 * startup.new_res_list[1]),int(0.10 * startup.new_res_list[2]),int(0.125 * startup.new_res_list[1] + 0.7 * startup.new_res_list[1]),int(0.10 * startup.new_res_list[2] + 0.8 * startup.new_res_list[2]),fill = "#808080")

    # This rectangle shows the area designated for the tools
    e_canv.create_rectangle(int(0.025 * startup.new_res_list[1]),int(0.10 * startup.new_res_list[2]),int(0.025 * startup.new_res_list[1] + 0.075 * startup.new_res_list[1]),int(0.10 * startup.new_res_list[2] + 0.8 * startup.new_res_list[2]),outline = "#808080")

    # This rectangle depicts the area reserved for the layers
    e_canv.create_rectangle(int(0.85 * startup.new_res_list[1]),int(0.10 * startup.new_res_list[2]),int(0.85 * startup.new_res_list[1] + 0.125 * startup.new_res_list[1]),int(0.10 * startup.new_res_list[2] + 0.38 * startup.new_res_list[2]),outline = "#808080")
    
    # This rectangle is for showing the functionality of the various tools
    e_canv.create_rectangle(int(0.85 * startup.new_res_list[1]),int(0.5 * startup.new_res_list[2]),int(0.85 * startup.new_res_list[1] + 0.125 * startup.new_res_list[1]),int(0.10 * startup.new_res_list[2] + 0.65 * startup.new_res_list[2]),outline = "#808080")
    
    # Declaration of functions

    def display_image():
        # Make a window here to display the image
        display = Toplevel()
        display.title("Original Image")
        main_image = Image_Handler("Project/original.png",image_name)
        display.geometry(str(main_image.image_size[0]) + "x" + str(main_image.image_size[1]) + "+" + str(int(0.475 * startup.new_res_list[1] - int(main_image.image_size[0] / 2))) + "+" + str(int(0.5 * startup.new_res_list[2] - int(main_image.image_size[1] / 2))))
        display.attributes("-topmost",True)
        main_image.save_image_locally()
        display_img = ImageTk.PhotoImage(main_image.image)
        image_label = tb.Label(display,bootstyle = "default",image = display_img)
        image_label.pack()
        display.mainloop()

    def add_image(): # This function is responsible for 
        image_path = filedialog.askopenfilenames(title = "Add Images",filetypes = (("PNG image","*.png"),("JPG image","*.jpg"),("JPEG image","*.jpeg"),("All Files","*.*")))
        if image_path == "":
            messagebox.showinfo("Alert","No image was selected!!!") # Displays a popup when no image is selected
        else:
            global image_name # Making this variable global in context to this function
            global image_loc # Similarly making this variable global in context to this function
            global current_images # Declaring this variable global to be used inside this function
            image_name = Path(image_path[0]).stem # Storing the original name of the image
            image_loc = image_path[0] # Assigning the original image path
            main_image = Image_Handler(image_path[0],image_name) # Creating an object of the Image Handler class
            main_image.save_image_locally() # Copies the image to the directory of the project
            e_canv.itemconfig(21,state = "normal")
            display_image() # This will show the image on the screen
        
    def close_editor():
        root.deiconify() # This command will show the editor again
        back_button() # This command will showcase the opening screen on the intro menu
        editor.destroy() # closes the editor window

    # This function will check the current tool selected and call another function to perform the specific task
    def check_tool():

        if tool_var.get() == 0:
            pass
        
        if tool_var.get() == 1:
            crop = Toplevel()
            crop.geometry("172x193+1160+407")
            crop.overrideredirect(True)
            
            def close_crop():
                crop.destroy()
            
            def read_entry():
                main_image = Image_Handler("Project/original.png",image_name)
                main_image.crop_image(int(posx1_entry_field.get()),int(posy1_entry_field.get()),int(posx2_entry_field.get()),int(posy2_entry_field.get()))
                main_image.show_image()
                close_crop()
            
            c_canv = tk.Canvas(crop,width = 171,height = 192)
            c_canv.pack(fill = "both",expand = True)
            c_canv.create_text(86,10,text = "Crop Tool",fill = "#adb5bd")
        
            c_canv.create_text(50,60,text = "Position (x1,y1)",fill = "#adb5bd")
            c_canv.create_text(50,100,text = "Position (x2,y2)",fill = "#adb5bd")
            
            c_canv.create_rectangle(0,0,171,192,outline = "#808080")

            posx1_entry_field = tb.Entry(crop,width = 2)
            posx1_entry_field.insert(0,"0")
            posy1_entry_field = tb.Entry(crop,width = 2)
            posy1_entry_field.insert(0,"0")
            c_canv.create_window(110,60,window = posx1_entry_field)
            c_canv.create_window(140,60,window = posy1_entry_field)
            
            posx2_entry_field = tb.Entry(crop,width = 2)
            posx2_entry_field.insert(0,"0")
            posy2_entry_field = tb.Entry(crop,width = 2)
            posy2_entry_field.insert(0,"0")
            c_canv.create_window(110,100,window = posx2_entry_field)
            c_canv.create_window(140,100,window = posy2_entry_field)
            
            crop_apply_but = tb.Button(crop,text = "Apply",bootstyle = "success,outline",width = 5,command = read_entry)
            w_crop_apply_but = c_canv.create_window(140,170,window = crop_apply_but)
        
            quit_but = tb.Button(crop,text = "Close",bootstyle = "danger,outline",command = close_crop)  
            w_quit_but = c_canv.create_window(80,172,window = quit_but)
            crop.mainloop()

        if tool_var.get() == 2:
            
            rotate = Toplevel()
            rotate.geometry("172x193+1160+407")
            rotate.overrideredirect(True)
            
            def close_rotate():
                rotate.destroy()
            
            def read_entry():
                main_image = Image_Handler("Project/original.png",image_name)
                main_image.rotate_image(int(rotate_entry_field.get()))
                main_image.show_image()
                close_rotate()
            
            r_canv = tk.Canvas(rotate,width = 171,height = 192)
            r_canv.pack(fill = "both",expand = True)
            r_canv.create_text(86,10,text = "Rotate Tool",fill = "#adb5bd")
        
            r_canv.create_text(63,100,text = "Rotation (in degrees)",fill = "#adb5bd")
            r_canv.create_rectangle(0,0,171,192,outline = "#808080")

            rotate_entry_field = tb.Entry(rotate,width = 5)
            rotate_entry_field.insert(0,"0")
            r_canv.create_window(145,100,window = rotate_entry_field)
            
            rotate_apply_but = tb.Button(rotate,text = "Apply",bootstyle = "success,outline",width = 5,command = read_entry)
            w_rotate_apply_but = r_canv.create_window(140,170,window = rotate_apply_but)
        
            quit_but = tb.Button(rotate,text = "Close",bootstyle = "danger,outline",command = close_rotate)  
            w_quit_but = r_canv.create_window(80,172,window = quit_but)
            rotate.mainloop()

        if tool_var.get() == 3:
            add_text = Toplevel()
            add_text.geometry("172x193+1160+407")
            add_text.overrideredirect(True)
            
            def close_add_text():
                add_text.destroy()
            
            def read_entry():
                main_image = Image_Handler("Project/original.png",image_name)
                main_image.add_text_image(str(text_entry_field.get()),int(pos1_entry_field.get()),int(pos2_entry_field.get()))
                main_image.show_image()
                close_add_text()
            
            t_canv = tk.Canvas(add_text,width = 171,height = 192)
            t_canv.pack(fill = "both",expand = True)
            t_canv.create_text(86,10,text = "Add Text Tool",fill = "#adb5bd")
        
            t_canv.create_text(30,65,text = "Text",fill = "#adb5bd")
            t_canv.create_text(61,110,text = "Position (x1,y1)",fill = "#adb5bd")
            
            t_canv.create_rectangle(0,0,171,192,outline = "#808080")

            text_entry_field = tb.Entry(add_text,width = 15)
            text_entry_field.insert(0,"Type here")
            t_canv.create_window(110,65,window = text_entry_field)
            
            pos1_entry_field = tb.Entry(add_text,width = 2)
            pos1_entry_field.insert(0,"0")
            
            pos2_entry_field = tb.Entry(add_text,width = 2)
            pos2_entry_field.insert(0,"0")
        
            t_canv.create_window(120,110,window = pos1_entry_field)
            t_canv.create_window(150,110,window = pos2_entry_field)

            text_apply_but = tb.Button(add_text,text = "Apply",bootstyle = "success,outline",width = 5,command = read_entry)
            w_rotate_apply_but = t_canv.create_window(140,170,window = text_apply_but)
        
            quit_but = tb.Button(add_text,text = "Close",bootstyle = "danger,outline",command = close_add_text)  
            w_quit_but = t_canv.create_window(80,172,window = quit_but)
            add_text.mainloop()

        if tool_var.get() == 4:
            levels = Toplevel()
            levels.geometry("172x193+1160+407")
            levels.overrideredirect(True)
            
            def close_levels():
                levels.destroy()
            
            def read_entry():
                main_image = Image_Handler("Project/original.png",image_name)
                main_image.adjust_levels(eval(b_entry_field.get()),eval(c_entry_field.get()),eval(s_entry_field.get()))
                main_image.show_image()
                close_levels()
            
            l_canv = tk.Canvas(levels,width = 171,height = 192)
            l_canv.pack(fill = "both",expand = True)
            l_canv.create_text(86,10,text = "Adjust Level Tool",fill = "#adb5bd")
        
            l_canv.create_text(50,50,text = "Brightness",fill = "#adb5bd")
            l_canv.create_text(46,90,text = "Contrast",fill = "#adb5bd")
            l_canv.create_text(50,130,text = "Saturation",fill = "#adb5bd")
            
            l_canv.create_rectangle(0,0,171,192,outline = "#808080")

            b_entry_field = tb.Entry(levels,width = 5)
            b_entry_field.insert(0,"0")
            l_canv.create_window(120,50,window = b_entry_field)
            
            c_entry_field = tb.Entry(levels,width = 5)
            c_entry_field.insert(0,"0")
            
            s_entry_field = tb.Entry(levels,width = 5)
            s_entry_field.insert(0,"0")
        
            l_canv.create_window(120,90,window = c_entry_field)
            l_canv.create_window(120,130,window = s_entry_field)

            levels_apply_but = tb.Button(levels,text = "Apply",bootstyle = "success,outline",width = 5,command = read_entry)
            w_levels_apply_but = l_canv.create_window(140,170,window = levels_apply_but)
        
            quit_but = tb.Button(levels,text = "Close",bootstyle = "danger,outline",command = close_levels)  
            w_quit_but = l_canv.create_window(80,172,window = quit_but)
            levels.mainloop()
            
        if tool_var.get() == 5:
            filter = Toplevel()
            filter.geometry("172x193+1160+407")
            filter.overrideredirect(True)
            
            def close_filter():
                filter.destroy()
            
            def read_entry():
                main_image = Image_Handler("Project/original.png",image_name)
                main_image.filter_image(int(blur_var.get()),int(contour_var.get()),int(emboss_var.get()),int(edge_var.get()))
                main_image.show_image()
                close_filter()
            
            f_canv = tk.Canvas(filter,width = 171,height = 192)
            f_canv.pack(fill = "both",expand = True)
            f_canv.create_text(86,10,text = "Filters",fill = "#adb5bd")
            
            f_canv.create_rectangle(0,0,171,192,outline = "#808080")    
    
            blur_var = IntVar()
            contour_var = IntVar()
            emboss_var = IntVar()
            edge_var = IntVar()
            
            blur_but = tb.Checkbutton(filter,text = "Blur",bootstyle = "light",variable = blur_var,onvalue = 1,offvalue = 0)
            contour_but = tb.Checkbutton(filter,text = "Contour",bootstyle = "light",variable = contour_var,onvalue = 1,offvalue = 0)
            emboss_but = tb.Checkbutton(filter,text = "Emboss",bootstyle = "light",variable = emboss_var,onvalue = 1,offvalue = 0)
            edge_but = tb.Checkbutton(filter,text = "Edge Enhance",bootstyle = "light",variable = edge_var,onvalue = 1,offvalue = 0)
            
            f_canv.create_window(70,45,window = blur_but)
            f_canv.create_window(80,75,window = contour_but)
            f_canv.create_window(79,105,window = emboss_but)
            f_canv.create_window(95,135,window = edge_but)
            
            rotate_apply_but = tb.Button(filter,text = "Apply",bootstyle = "success,outline",width = 5,command = read_entry)
            w_rotate_apply_but = f_canv.create_window(140,170,window = rotate_apply_but)
        
            quit_but = tb.Button(filter,text = "Close",bootstyle = "danger,outline",command = close_filter)  
            w_quit_but = f_canv.create_window(80,172,window = quit_but)
            filter.mainloop()
            
            
        if tool_var.get() == 6:
            main_image = Image_Handler("Project/temp.png",image_name)
            main_image.save_image_changes()
            messagebox.showinfo("Save Alert","Your changes have been successfully saved")
            
            
            
                   
    # Declaration of buttons
    tool_var = IntVar()
    tool_var.set("0")

    crop_img = ImageTk.PhotoImage(Image.open("Dependencies/System_Images/resized_crop.png"))
    crop_but = tb.Checkbutton(editor,text = "Crop",bootstyle = "light,toolbutton",image = crop_img,variable = tool_var,onvalue = 1,offvalue = 0,command = check_tool)
    w_crop_but = e_canv.create_window(int(0.065 * startup.new_res_list[1]),int(0.16 * startup.new_res_list[2]),window = crop_but)
    e_canv.create_text(int(0.065 * startup.new_res_list[1]),int(0.2175 * startup.new_res_list[2]),text = "Crop",fill = "#adb5bd")

    rotate_img = ImageTk.PhotoImage(Image.open("Dependencies/System_Images/resized_rotate.png"))
    rotate_but = tb.Checkbutton(editor,bootstyle = "light,toolbutton",image = rotate_img,variable = tool_var,onvalue = 2,offvalue = 0,command = check_tool)
    w_rotate_but = e_canv.create_window(int(0.065 * startup.new_res_list[1]),int(0.2875 * startup.new_res_list[2]),window = rotate_but)
    e_canv.create_text(int(0.065 * startup.new_res_list[1]),int(0.345 * startup.new_res_list[2]),text = "Rotate",fill = "#adb5bd")

    text_img = ImageTk.PhotoImage(Image.open("Dependencies/System_Images/resized_text.png"))
    text_but = tb.Checkbutton(editor,bootstyle = "light,toolbutton",image = text_img,variable = tool_var,onvalue = 3,offvalue = 0,command = check_tool)
    w_text_but = e_canv.create_window(int(0.065 * startup.new_res_list[1]),int(0.42 * startup.new_res_list[2]),window = text_but)
    e_canv.create_text(int(0.065 * startup.new_res_list[1]),int(0.4775 * startup.new_res_list[2]),text = "Add Text",fill = "#adb5bd")

    level_img = ImageTk.PhotoImage(Image.open("Dependencies/System_Images/resized_levels.png"))
    level_but = tb.Checkbutton(editor,bootstyle = "light,toolbutton",image = level_img,variable = tool_var,onvalue = 4,offvalue = 0,command = check_tool)
    w_level_but = e_canv.create_window(int(0.065 * startup.new_res_list[1]),int(0.56 * startup.new_res_list[2]),window = level_but)
    e_canv.create_text(int(0.065 * startup.new_res_list[1]),int(0.6175 * startup.new_res_list[2]),text = "Adjust Levels",fill = "#adb5bd")
  
    filter_img = ImageTk.PhotoImage(Image.open("Dependencies/System_Images/resized_filter.png"))
    filter_but = tb.Checkbutton(editor,bootstyle = "light,toolbutton",image = filter_img,variable = tool_var,onvalue = 5,offvalue = 0,command = check_tool)
    w_filter_but = e_canv.create_window(int(0.065 * startup.new_res_list[1]),int(0.70 * startup.new_res_list[2]),window = filter_but)
    e_canv.create_text(int(0.065 * startup.new_res_list[1]),int(0.7575 * startup.new_res_list[2]),text = "Filters",fill = "#adb5bd")

    save_img = ImageTk.PhotoImage(Image.open("Dependencies/System_Images/resized_save.png"))
    save_but = tb.Checkbutton(editor,bootstyle = "light,toolbutton",image = save_img,variable = tool_var,onvalue = 6,offvalue = 0,command = check_tool)
    w_save_but = e_canv.create_window(int(0.065 * startup.new_res_list[1]),int(0.835 * startup.new_res_list[2]),window = save_but)
    e_canv.create_text(int(0.065 * startup.new_res_list[1]),int(0.8875 * startup.new_res_list[2]),text = "Save",fill = "#adb5bd")
    
    # This button assigns the images to a specific image object
    add_img_but = tb.Button(editor,text = "Add Images",bootstyle = "primary,outline",width = 20,command = add_image)
    w_add_img_but = e_canv.create_window(int(0.9125 * startup.new_res_list[1]),int(0.14 * startup.new_res_list[2]),window = add_img_but)
    
    # Message for instruction  
    e_canv.create_text(int(0.91 * startup.new_res_list[1]),int(0.59 * startup.new_res_list[2]),text = "Instructions",fill = "#adb5bd")
    e_canv.create_text(int(0.91 * startup.new_res_list[1]),int(0.62 * startup.new_res_list[2]),text = "1. Select an image from above",fill = "#adb5bd")
    e_canv.create_text(int(0.90625 * startup.new_res_list[1]),int(0.64 * startup.new_res_list[2]),text = "2. Select a tool from toolbar",fill = "#adb5bd")
    
    
    # This is a common variable for the toolbuttons representing the different images
    img_but_var = IntVar()
    
    # These are all the buttons representing the images

    img_but_1 = tb.Checkbutton(editor,text = "Image 1",bootstyle = "light,toolbutton",variable = img_but_var,onvalue = 1,offvalue = 0,width = 20)
    w_img_but_1 = e_canv.create_window(int(0.9125 * startup.new_res_list[1]),int(0.20 * startup.new_res_list[2]),window = img_but_1)
    
    img_but_2 = tb.Checkbutton(editor,text = "Image 2",bootstyle = "light,toolbutton",variable = img_but_var,onvalue = 2,offvalue = 0,width = 20)
    w_img_but_2 = e_canv.create_window(int(0.9125 * startup.new_res_list[1]),int(0.26 * startup.new_res_list[2]),window = img_but_2)

    img_but_3 = tb.Checkbutton(editor,text = "Image 3",bootstyle = "light,toolbutton",variable = img_but_var,onvalue = 3,offvalue = 0,width = 20)
    w_img_but_3 = e_canv.create_window(int(0.9125 * startup.new_res_list[1]),int(0.32 * startup.new_res_list[2]),window = img_but_3)

    img_but_4 = tb.Checkbutton(editor,text = "Image 4",bootstyle = "light,toolbutton",variable = img_but_var,onvalue = 4,offvalue = 0,width = 20)
    w_img_but_4 = e_canv.create_window(int(0.9125 * startup.new_res_list[1]),int(0.38 * startup.new_res_list[2]),window = img_but_4)

    img_but_5 = tb.Checkbutton(editor,text = "Image 5",bootstyle = "light,toolbutton",variable = img_but_var,onvalue = 5,offvalue = 0,width = 20)
    w_img_but_5 = e_canv.create_window(int(0.9125 * startup.new_res_list[1]),int(0.44 * startup.new_res_list[2]),window = img_but_5)
    
    for i in range(21,26):
        e_canv.itemconfig(i,state = "hidden")
    
    # This is the quit button
    quit_but = Button(editor,text = "Quit",bootstyle = "danger,outline",command = close_editor)
    w_but = e_canv.create_window(int(0.9575 * startup.new_res_list[1]),int(0.05 * startup.new_res_list[2]),window = quit_but)
  
    editor.mainloop() # End of the Editor's loop
    

# Function definitions for Intro_Menu
def new_project_file():
    # when new button is pressed we will hide all the existing button and make the new buttons appear
    for i in range(2,6):
        canv.itemconfig(i,state = "hidden")
    for i in range(6,10):
        canv.itemconfig(i,state = "normal")
    entry_field.insert(0,"Untitled") # By default we provide the entry menu with some value

def open_project_file():
    # This opens a file explorer dialog box through which the user can browse and select the project
    filename = filedialog.askopenfilenames(title = "Open Project Files",filetypes = (("IMX project","*.imx"),("All Files","*.*")))
    if filename == "":
        print("Empty")
    else:
        print(filename)

def options():
    pass

def create_project():
    project_filename = entry_field.get() # .get() retrieves whatever is typed on the entry field
    root.withdraw() # This command hides the main window
    Main_Editor(project_filename) # calling this function to start the editor
    

def back_button():
    # If back button pressed showing all the previous buttons and hiding the new ones
    for i in range(2,6):
        canv.itemconfig(i,state = "normal")
    for i in range(6,10):
        canv.itemconfig(i,state = "hidden")
    entry_field.delete(0,END)
    
def close_window(): 
    root.destroy() # This will close the window


# Varible Declaration
button_style = tb.Style() # This style widget will let us change the button size
button_style.configure('light.Outline.TButton',font = ("Helvetica",int(startup.new_res_list[5] / startup.button_size_factor[1])))

# Component declaration and definition
new_but = tb.Button(text = "New Project",style = "light.Outline.TButton",width = int(startup.new_res_list[5] / startup.button_size_factor[0]),command = new_project_file) # Obtaining the button width in accordance with the menu resolution
w_new_but = canv.create_window(int(100 * startup.menu_position_factor[0]),int(60 * startup.menu_position_factor[1]),window = new_but) # Positioning the button w.r.t the position factors

op_but = tb.Button(text = "Open Project",style = "light.Outline.TButton",width = int(startup.new_res_list[5] / startup.button_size_factor[0]),command = open_project_file)
w_op_but = canv.create_window(int(100 * startup.menu_position_factor[0]),int(100 * startup.menu_position_factor[1]),window = op_but)

opt_but = tb.Button(text = "Options",style = "light.Outline.TButton",width = int(startup.new_res_list[5] / startup.button_size_factor[0]),command = options)
w_opt_but = canv.create_window(int(100 * startup.menu_position_factor[0]),int(140 * startup.menu_position_factor[1]),window = opt_but)

exit_but = tb.Button(text = "Quit",style = "light.Outline.TButton",width = int(startup.new_res_list[5] / startup.button_size_factor[0]),command = close_window)
w_exit_but = canv.create_window(int(100 * startup.menu_position_factor[0]),int(180 * startup.menu_position_factor[1]),window = exit_but)

back_img = ImageTk.PhotoImage(Image.open("Dependencies/System_Images/small_back_arrow.png")) # Adding an image to the back button
back_but = tb.Button(style = "light.Outline.TButton",image = back_img,width = int((startup.new_res_list[5] / 2 ) / startup.button_size_factor[0]),command = back_button)
w_back_but = canv.create_window(int(45 * startup.menu_position_factor[0]),int(60 * startup.menu_position_factor[1]),window = back_but) 

create_but = tb.Button(text = "Create",style = "light.Outline.TButton",width = int((startup.new_res_list[5] / 2 ) / startup.button_size_factor[0]),command = create_project)
w_create_but = canv.create_window(int(136 * startup.menu_position_factor[0]),int(180 * startup.menu_position_factor[1]),window = create_but) 

# Creating an entry field to take input from the user
entry_field = tb.Entry(text = "Project Name",style = "light.TEntry",width = int(startup.new_res_list[5] / (startup.button_size_factor[0] / 1.25)))
entry_field.place(height = 50)
w_entry_field = canv.create_window(int(100 * startup.menu_position_factor[0]),int(130 * startup.menu_position_factor[1]),window = entry_field)


canv.create_text(int(100 * startup.menu_position_factor[0]),int(100 * startup.menu_position_factor[1]),text = "Project Name",font = ("Helvetica",int(startup.new_res_list[5] / startup.button_size_factor[1])),fill = "#808080")

for i in range(6,10): # By default we are hiding 4 elements
    canv.itemconfig(i,state = "hidden")
             
# A text with names of all the project members
canv.create_text(int(270 * startup.menu_position_factor[0]),int(280 * startup.menu_position_factor[1]),text = "-- Project by : Anant Raj --",font = ("Helvetica",int(startup.new_res_list[5] / startup.button_size_factor[1])),fill = "#adb5bd")

root.mainloop() # The whole application runs in a loop from the creation of the window to this very method 
