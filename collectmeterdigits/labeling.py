import os
from PIL import Image
import matplotlib
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.figure as fig
from matplotlib.widgets import Slider, Button, RadioButtons
import shutil
import pandas as pd
from collectmeterdigits.predict import predict

def ziffer_data_files(input_dir):
    '''return a list of all images in given input dir in all subdirectories'''
    imgfiles = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if (file.endswith(".jpg")):
                imgfiles.append(root + "/" + file)
    
    imgfiles = sorted(imgfiles, key=lambda x : os.path.basename(x))
    return  imgfiles


def label(path, startlabel=0, imageurlsfile=None):
    global filename
    global i
    global im
    global filelabel
    global title
    global ax
    global slabel
    global files
    global predbox

    print(f"Startlabel", startlabel)

    if (imageurlsfile!=None):
        files = pd.read_csv(imageurlsfile, index_col=0).to_numpy().reshape(-1)

        # remove files not exists
        for file in files:
            if (not os.path.exists(file)):
              files = files[~np.isin(files, file)]
    else:
        files = ziffer_data_files(path)

    if (len(files)==0):
        print("No images found in path")
        exit(1)
        
    i = 0
    img, img_2032, filelabel, filename, i = load_image(files, i, startlabel)

    # disable toolbar
    matplotlib.rcParams['toolbar'] = 'None'
    
    # set window title
    fig = plt.gcf()
    fig.canvas.manager.set_window_title('1 of ' + str(len(files)) + ' images')
   
    title = plt.title(filelabel)  # set title
    plt.yticks(np.arange(0, 1, step=0.1))
    im = plt.imshow(img, aspect='1.6', extent=[0, 1, 0, 1])
    for y in np.arange(0.1, 0.91, 0.1):
        if (int(y*10)%2==0):
            color='yellow'   
        else:
            color='blue'
        plt.axhline(y=y, xmin=0, xmax=0.2, color=color)
        plt.axhline(y=y, xmin=0.8, xmax=1, color=color)
        plt.axhline(y=y, xmin=0.2, xmax=0.8, color=color, linestyle="--")

    plt.axvline(x=0.2, ymin=0.0, ymax=1, linewidth=3, color='red', linestyle=":")
    plt.axvline(x=0.8, ymin=0.0, ymax=1, linewidth=3, color='red', linestyle=":")

    plt.text(1.1, 0.9, "You can use cursor key controll also:\n\nleft/right = prev/next\nup/down=in/decrease value\ndelete=remove.", fontsize=6)
    prediction = predict(img_2032)
    plt.text(-0.6, 0.7, "Prediction:", fontsize=8)
    predbox = plt.text(-0.6, 0.6, "{:.1f}".format(prediction), fontsize=24, bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'))
    ax=plt.gca()
    ax.get_xaxis().set_visible(False) 
    axlabel = plt.axes([0.1, 0.025, 0.7, 0.04])
    slabel = Slider(axlabel, label='Label',valmin= 0.0, valmax=9.9, valstep=0.1, 
                    valinit=filelabel,
                    orientation='horizontal')
    previousax = plt.axes([0.87, 0.225, 0.1, 0.04])
    bprevious = Button(previousax, 'previous', hovercolor='0.975')
    nextax = plt.axes([0.87, 0.025, 0.1, 0.04])
    bnext = Button(nextax, 'update', hovercolor='0.975')
    removeax = plt.axes([0.87, 0.4, 0.1, 0.04])
    bremove = Button(removeax, 'delete', hovercolor='0.975')
    
    increaselabel = plt.axes([0.93, 0.1, 0.05, 0.04])
    bincreaselabel = Button(increaselabel, '+0.1', hovercolor='0.975')
    decreaselabel = plt.axes([0.87, 0.1, 0.05, 0.04])
    bdecreaselabel = Button(decreaselabel, '-0.1', hovercolor='0.975')

    def load_previous():
        global im
        global title
        global slabel
        global i
        global filelabel
        global filename
        global predbox

        i = (i - 1) % len(files)
        img, img_2032, filelabel, filename, i = load_image(files, i)
        im.set_data(img)
        title.set_text(filelabel)
        slabel.set_val(filelabel)
        fig = plt.gcf()
        fig.canvas.manager.set_window_title(str(i) + ' of ' + str(len(files)) + ' images')
        predbox.set_text("{:.1f}".format(predict(img_2032)))
        plt.draw()


    def load_next(increaseindex = True):
        global im
        global title
        global slabel
        global i
        global filelabel
        global filename
        global predbox

        if increaseindex:
            i = (i + 1) % len(files)
        img, img_2032, filelabel, filename, i = load_image(files, i)
        im.set_data(img)
        title.set_text(filelabel)
        slabel.set_val(filelabel)
        fig = plt.gcf()
        fig.canvas.manager.set_window_title(str(i) + ' of ' + str(len(files)) + ' images')
        predbox.set_text("{:.1f}".format(predict(img_2032)))
        
        plt.draw()

    def increase_label(event):
        slabel.set_val((slabel.val + 0.1) % 10)

    def decrease_label(event):
        slabel.set_val((slabel.val - 0.1) % 10)

    def remove(event):
        global filename
        global files
        global i
        os.remove(filename)
        files = np.delete(files,i, 0)
        load_next(False)

    def previous(event):
        load_previous()

    def next(event):
        global filelabel
        global filename
        
        basename = os.path.basename(filename).split('_', 1)
        basename = basename[-1]
        if (filelabel != slabel.val):
            _zw = os.path.join(os.path.dirname(filename), "{:.1f}".format(slabel.val) + "_" + basename)
            files[i] = _zw
            shutil.move(filename, _zw)
        load_next()

    def on_press(event):
#        print('press', event.key)
        if event.key == 'right':
            next(event)
        if event.key == 'left':
            previous(event)
        if event.key == 'up':
            increase_label(event);
        if event.key == 'down':
            decrease_label(event)
        if event.key == 'enter':
            next(event)
        if event.key == 'delete':
            remove(event)

    fig.canvas.mpl_connect('key_press_event', on_press)
    
    
    bnext.on_clicked(next)
    bprevious.on_clicked(previous)
    bremove.on_clicked(remove)
    bincreaselabel.on_clicked(increase_label)
    bdecreaselabel.on_clicked(decrease_label)

    plt.show()

    
        


def load_image(files, i, startlabel = -1):

    while True:
        base = os.path.basename(files[i])
        # get label from filename (1.2_ new or 1_ old),
        if (base[1]=="."):
            target = base[0:3]
        else:
            target = base[0:1]
        try:
            category = float(target)
        except ValueError:
            category = 0.0
        if category >= startlabel:  
            break 
        else:
            i = (i + 1)

    filename = files[i]
    test_image = Image.open(filename)
    test_image_resized = test_image.resize((20, 32), Image.NEAREST)
    return test_image, test_image_resized, category, filename, i
    
