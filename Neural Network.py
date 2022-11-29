import tkinter as tk
import numpy as np
from PIL import ImageTk, Image
from tkinter import filedialog
import os

class main():
    
    #i don't know why I declared these variables out here, but it works, so shut the up
    imageAddress = None
    currentImage = None
    root = tk.Tk()
    imgSelected = False
    chosenProcess = tk.StringVar()
    chosenProcess.set("edge detection")
    
    #interface is created
    def __init__(self):
        print("Program start!")
        self.button = tk.Button(self.root, text="Choose image", command=lambda: self.chooseImage())
        self.label = tk.Label(self.root)
        self.label["text"] = "Please select an image!"
        self.imageLabel = tk.Label(self.root, image=None)
        self.button.pack()
        self.label.pack()
        self.root.mainloop()
    
    #main interface functionality
    def chooseImage(self):
        #opens the file browser and lets the user select an image
        self.imageAddress = filedialog.askopenfilename(initialdir="C:/Users/gregl/.spyder-py3/projects/image processing/test images", title="Select A File", filetypes=[("BMP Files", "*.bmp")])
        #image and image address are displayed
        self.label["text"] = self.imageAddress
        self.currentImage = ImageTk.PhotoImage(Image.open(self.imageAddress))
        self.imageLabel["image"] = self.currentImage
        self.imageLabel.pack()
        #dropdown and process button are displayed if an image is chosen
        self.dropdown = tk.OptionMenu(self.root, self.chosenProcess, "edge detection", "blur", "pixelate", "???", "horizontal lines", "vertical lines")
        self.processButton = tk.Button(self.root, text="Process the image!", command=lambda: self.processImage())
        if self.imgSelected == False:
            self.dropdown.pack()
            self.processButton.pack()
            self.imgSelected = True
        print("Image opened")
        #the image is then parsed
        self.parseImage()
        
    #image is converted into an array, and image height, width, and bit depth are collected
    def parseImage(self):
        self.imgArray = np.array(Image.open(self.imageAddress).convert("RGB"))
        self.imgy = self.imgArray.shape[0]
        self.imgx = self.imgArray.shape[1]
        self.imgDepth = self.imgArray.shape[2]
        print("The image's width is " + str(self.imgx))
        print("The image's height is " + str(self.imgy))
    
    #called on processButton press
    def processImage(self):
        self.neuralNetwork = False
        self.imgR = np.empty([self.imgy, self.imgx])
        self.imgG = np.empty([self.imgy, self.imgx])
        self.imgB = np.empty([self.imgy, self.imgx])
        
        #process to be applied is chosen based on dropdown menu choice
        if self.chosenProcess.get() == "horizontal lines":
            self.newArray = self.imgArray
            for y in range(0,self.imgy,2):
                for x in range(self.imgx):
                    for clr in range(3):
                        self.newArray[y,x,clr] = 255
                        
                        
        elif self.chosenProcess.get() == "vertical lines":
            self.newArray = self.imgArray
            for x in range(0,self.imgx,2):
                    for y in range(self.imgy):
                        for clr in range(3):
                            self.newArray[y,x,clr] = 255
        
                            
        elif self.chosenProcess.get() == "blur" or self.chosenProcess.get() == "edge detection" or self.chosenProcess.get() == "pixelate":
            #split image into R G and B channels
            for y in range(self.imgy):
                for x in range(self.imgx):
                    self.imgR[y,x] = self.imgArray[y,x,0]
                    self.imgG[y,x] = self.imgArray[y,x,1]
                    self.imgB[y,x] = self.imgArray[y,x,2]
                    
            #create weight matrix for blur
            weights = np.zeros([self.imgx,self.imgx])
            if self.chosenProcess.get() == "blur":
                weightVal = 0.33
                for y in range(self.imgx-3):
                    weights[y,y] = weightVal
                    weights[y,y+1] = weightVal
                    weights[y,y+2] = weightVal
                weights[self.imgx-3,self.imgx-1] = weightVal
                weights[self.imgx-3,self.imgx-2] = weightVal
                weights[self.imgx-3,self.imgx-3] = weightVal
                weights[self.imgx-2,0] = weightVal
                weights[self.imgx-2,self.imgx-1] = weightVal
                weights[self.imgx-2,self.imgx-2] = weightVal
                weights[self.imgx-1,0] = weightVal
                weights[self.imgx-1,1] = weightVal
                weights[self.imgx-1,self.imgx-1] = weightVal
                
            elif self.chosenProcess.get() == "edge detection":
                weightVal = -0.1
                for y in range(self.imgx):
                    weights[y,y] = weightVal
                    
                weightVal = 0.1
                for y in range(self.imgx-1):
                    weights[y,y+1] = weightVal
                weights[self.imgx-1, 0] = weightVal
                print(weights)
                        
            elif self.chosenProcess.get() == "pixelate":
                weightVal = 1
                cumRange = 0
                for x in range(0, self.imgx, 3):
                    for y in range(3):
                        weights[y+cumRange,x] = weightVal
                    if cumRange < self.imgx-5:
                        cumRange = cumRange + 3
                    
                print(weights)

            #create an array for the new image with the dimensions of the original image
            self.newArray = np.ndarray(shape=(self.imgy, self.imgx, self.imgDepth))
            
            #each line of each colour channel is multiplied by the weights matrix and stored in the new image array
            for y in range(self.imgR.shape[0]):
                self.newArray[y,0:,0] = np.matmul(weights, self.imgR[y,0:])
                
            for y in range(self.imgG.shape[0]):   
                self.newArray[y,0:,1] = np.matmul(weights, self.imgG[y,0:])
                
            for y in range(self.imgG.shape[0]):   
                self.newArray[y,0:,2] = np.matmul(weights, self.imgB[y,0:])
            
            #values in the array are rounded to remove floats
            self.newArray = np.around(self.newArray)
            #all values in the array are turned into integers, just in case
            for y in range(self.imgy):
                for x in range(self.imgx):
                    for clr in range(3):
                        self.newArray[y,x,clr] = int(self.newArray[y,x,clr])
            
                    
        elif self.chosenProcess.get() == "???":
            #split image into R G and B channels
            for y in range(self.imgy):
                for x in range(self.imgx):
                    self.imgR[y,x] = self.imgArray[y,x,0]
                    self.imgG[y,x] = self.imgArray[y,x,1]
                    self.imgB[y,x] = self.imgArray[y,x,2]
                    
            #create weight matrix for ???
            weights = np.zeros([self.imgx,self.imgx])
            weightVal = 0.5
            for y in range(self.imgx-3):
                weights[y,y] = weightVal
                weights[y,y+1] = weightVal
                weights[y,y+2] = weightVal
                
                
            weights[self.imgx-3,self.imgx-1] = weightVal
            weights[self.imgx-3,self.imgx-2] = weightVal
            weights[self.imgx-3,self.imgx-3] = weightVal
            weights[self.imgx-2,0] = weightVal
            weights[self.imgx-2,self.imgx-1] = weightVal
            weights[self.imgx-2,self.imgx-2] = weightVal
            weights[self.imgx-1,0] = weightVal
            weights[self.imgx-1,1] = weightVal
            weights[self.imgx-1,self.imgx-1] = weightVal
            

            #create an array for the new image with the dimensions of the original image
            self.newArray = np.ndarray(shape=(self.imgy, self.imgx, self.imgDepth))
            
            #each line of each colour channel is multiplied by the weights matrix and stored in the new image array
            for y in range(self.imgR.shape[0]):
                self.newArray[y,0:,0] = np.matmul(weights, self.imgR[y,0:])
                
            for y in range(self.imgG.shape[0]):   
                self.newArray[y,0:,1] = np.matmul(weights, self.imgG[y,0:])
                
            for y in range(self.imgG.shape[0]):   
                self.newArray[y,0:,2] = np.matmul(weights, self.imgB[y,0:])
            
            #values in the array are rounded to remove floats
            self.newArray = np.around(self.newArray)
            #all values in the array are turned into integers, just in case
            for y in range(self.imgy):
                for x in range(self.imgx):
                    for clr in range(3):
                        self.newArray[y,x,clr] = int(self.newArray[y,x,clr])
                        
                        
        #new array is converted into uint8 dtype to be compatible with PIL
        self.newArray = self.newArray.astype("uint8")
        #array is converted into image
        self.newImg = Image.fromarray(self.newArray)
        #the new array becomes the current image array
        self.imgArray = self.newArray
        #new image is saved with the _processed suffix
        self.newImg.save(str(os.path.splitext(os.path.basename(self.imageAddress))[0]) + "_processed.bmp")
        #processed image is displayed in the window
        self.currentImage = ImageTk.PhotoImage(self.newImg)
        self.imageLabel["image"] = self.currentImage
        self.imageLabel.pack()
        
        print('The image has been processed and saved as "' + str(os.path.splitext(os.path.basename(self.imageAddress))[0]) + '_processed.bmp"')
                
        
main()
    