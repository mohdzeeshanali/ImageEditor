from PIL import Image,ImageFont,ImageDraw,ImageEnhance,ImageFilter

class Image_Handler:

    global image
    global image_size
    global image_name
    global image_location

    def __init__(self,image_loc,name): # Constructor called at the start of 
        self.image_location = image_loc
        self.image = Image.open(image_loc)
        self.image_size = self.image.size
        self.image_name = name

    def rotate_image(self,angle):
        self.image = self.image.rotate(angle)
        self.image.save("Project/temp.png")
        self.image = Image.open("Project/temp.png")
    
    def crop_image(self,x1,y1,x2,y2):
        self.image = self.image.crop((x1,y1,x2,y2))
        self.image.save("Project/temp.png")
        self.image = Image.open("Project/temp.png")

    def add_text_image(self,img_text,x1,y1):
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype("OpenSans-Bold.ttf",30)
        draw.text((x1,y1),img_text,(255,255,255),font = font)
        self.image.save("Project/temp.png")
        self.image = Image.open("Project/temp.png")

    def adjust_levels(self,b_value,c_value,s_value):
        bright_img = ImageEnhance.Brightness(self.image)
        bright_img.enhance(b_value).save("Project/temp.png")
        self.image = Image.open("Project/temp.png")
        
        contrast_img = ImageEnhance.Contrast(self.image)
        contrast_img.enhance(c_value).save("Project/temp.png")
        self.image = Image.open("Project/temp.png")

        saturated_img = ImageEnhance.Color(self.image)
        saturated_img.enhance(s_value).save("Project/temp.png")
        self.image = Image.open("Project/temp.png")
        
    def filter_image(self,b_var,c_var,e_var,ed_var):
        if b_var == 1:
            self.image = self.image.filter(ImageFilter.BLUR)
            self.image.save("Project/temp.png")
        if c_var == 1:
            self.image = Image.open("Project/temp.png")
            self.image = self.image.filter(ImageFilter.CONTOUR)
            self.image.save("Project/temp.png")
        if e_var == 1:
            self.image = Image.open("Project/temp.png")
            self.image = self.image.filter(ImageFilter.EMBOSS)
            self.image.save("Project/temp.png")
        if ed_var == 1:
            self.image = Image.open("Project/temp.png")
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            self.image.save("Project/temp.png")
            

    def save_image_changes(self):
        self.image.save("Project/original.png")
        
    def get_image(self):
        return self.image

    def show_image(self):
        self.image.show()

    def save_image_locally(self):
        self.image.save("Project/original.png")
        self.image = Image.open("Project/original.png")
        self.image.save("Project/temp.png")
        self.image = Image.open("Project/original.png")
            


    