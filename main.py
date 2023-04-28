import sys
import os
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

# Very basic class to store settings for the application.
class Settings:
    '''
    Object to store application settings.
    Settings are stored in a dictionary, and accessed through various properties
        image_path = path to folder containing images to show
        title = title for the window created to show images
    '''

    def __init__(self):
        # start by storing all possible settings as their default values
        self._settings = {'image_path': '', 'title': ''}
        self.read_settings()

    def read_settings(self):
        # Read the settings from the config.txt file
        f = open("config.txt", "r")

        lines = f.readlines()
        for line in lines:
            parts = line.split("=")
            if parts[0] in self._settings.keys():
                self._settings[parts[0]] = parts[1].strip()
            else:
                print(f"{parts[0]} is not a valid setting name.")

        f.close()

    @property
    def image_path(self):
        return self._settings['image_path']

    @property
    def title(self):
        return self._settings['title']

# Class to manage list of image paths and moving to next, previous etc.
class ImageList:
    def __init__(self):
        self.curr_index = 0
        self.paths = get_image_paths(settings.image_path)

    def previous(self):
        # Move curr_index to the previous item in the list of paths.
        # If it hits the start, reset it to the end
        self.curr_index =- 1

        if self.curr_index == -1:
            self.curr_index = len(self.paths)-1

        return self.current()

    def current(self):
        # Return the path for the current image
        return self.paths[self.curr_index]

    def next(self):
        # Move curr_index to the next item in the list of paths.
        # If it hits the end, reset it to the begining

        self.curr_index += 1

        if self.curr_index == len(self.paths):
            self.curr_index = 0

        return self.current()

    def as_photo_image(self, path):
        img = Image.open(path)
        img = img.resize((150, 150), Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def print_paths(self):
        # Quick method to print all the paths to the console
        for path in self.paths:
            print(path)

# TODO: Need to think about how to periodically update the list of images, without losing the current index.
# I think the way to do this is to simply look at all the files found and see if it is already in the
# list of paths....if not append it.
# May need to use something like CRON to periodically Kill the app and restart it....for now, maybe have it update
# every 30 sec.

# Scan the specified path for image files to display
def get_image_paths(path):
   # Find all images in the specified path and return a list of sting paths to them

    paths = []

    for root, dirs, files in os.walk(path):
       for f in files:
           if f.endswith(".png") or f.endswith(".jpg"):
                img_path = os.path.join(root, f)
                if img_path not in paths:
                    paths.append(img_path)
    return paths








# Callback functions to handle changing image
def prev_image():
    # Move to next image
    prev = images.previous()
    if DEBUG:
        print(prev)

    new_photo_img=images.as_photo_image(prev)

    img_label.configure(image=new_photo_img)
    img_label.image = new_photo_img

def next_image():
    # Move to next image
    next = images.next()
    if DEBUG:
        print(next)

    new_photo_img=images.as_photo_image(next)

    img_label.configure(image=new_photo_img)
    img_label.image = new_photo_img

# Debug flag. Set to True / False to run debug code or not
DEBUG = True

# Instantiate a settings object and scan for images
settings = Settings()
images = ImageList()

# ----------------------------------------------------
# Tkinter - How to display images using a Label
#       https://www.activestate.com/resources/quick-reads/how-to-add-images-in-tkinter/
# ----------------------------------------------------

# Create an instance of tkinter frame
win = Tk()

# Configure some properties of the window
win.title(settings.title)
win.geometry("200x200") #TODO: This should be a setting?

# -----------------------------------------------------------------------------
# create the main sections of the layout, and lay them out
# -----------------------------------------------------------------------------
top = Frame(win)
bottom = Frame(win)
top.pack(side=TOP, fill=BOTH, expand=True)
bottom.pack(side=BOTTOM)

# -----------------------------------------------------------------------------
# create the widgets for the TOP part of the GUI, and lay them out
# -----------------------------------------------------------------------------
# Display the first photo automatically
photo_img = images.as_photo_image(images.current())
img_label = tk.Label(win, image=photo_img)
# TODO - Should we resize, reposition etc? Also need to do this as window resizes?
img_label.pack(in_=top, side=LEFT, fill=BOTH, expand=True)

# -----------------------------------------------------------------------------
# create the widgets for the BOTTOM part of the GUI, and lay them out
# -----------------------------------------------------------------------------
prev = tk.Button(win, text="<",
                   width=5, height=2,
                   bg="purple", fg="black",
                   command=prev_image)

next = tk.Button(win, text=">",
                   width=5, height=2,
                   bg="purple", fg="black",
                   command=next_image)

prev.pack(in_=bottom, side=LEFT)
next.pack(in_=bottom, side=RIGHT)

win.mainloop()

