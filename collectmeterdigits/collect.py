from urllib.error import HTTPError, URLError
import urllib.request
import re
import requests
import os
from PIL import Image
from datetime import date, timedelta
import imagehash
import secrets
import shutil
from collectmeterdigits.labeling import label
import time
import numpy as np



target_path = "./data"                   # root data path
target_raw_path =  "./data/raw_images"   # here all raw images will be stored
target_label_path = "./data/labeled"
target_store_dublicates = "./data/raw_images/dublicates"


def yesterday(daysbefore=1):
    ''' return the date of yesterday as string in format yyyymmdd'''
    yesterday = date.today() - timedelta(days=daysbefore)
    return yesterday.strftime("%Y%m%d")


def readimages(servername, output_dir, daysback=15):
    '''get all images taken yesterday and store it in target path'''
    serverurl = "http://" + servername
    count = 0
    print(f"Loading data from {servername} ...")
    for datesbefore in range(0, daysback):
        picturedate = yesterday(daysbefore=datesbefore)
        # only if not exists already
        for i in range(24):
            hour = f'{i:02d}'
            if not os.path.exists(path = output_dir + "/" + servername + "/" + picturedate + "/" + hour):
                try:
                    fp = urllib.request.urlopen(serverurl + "/fileserver/log/digit/" + picturedate + "/" + hour + "/")
                except HTTPError as h:
                    print( serverurl + "/fileserver/log/digit/" + picturedate + "/" + hour + "/ not found." )
                    continue
                except URLError as ue:
                    print("URL-Error! Server not available? Requested URL was: ", serverurl + "/fileserver/log/digit/" + picturedate + "/" + hour + "/" )
                    exit(1)
                print("Loading ... ",  servername + "/" + picturedate + "/" + hour)
                
                mybytes = fp.read()

                mystr = mybytes.decode("utf8")
                fp.close()

                urls = re.findall(r'href=[\'"]?([^\'" >]+)', mystr)
                path = output_dir + "/" + servername + "/" + picturedate + "/" + hour
                os.makedirs(path, exist_ok=True) 
                for url in urls:
                    if (url[-3:] != 'jpg'):
                        continue
                    prefix = os.path.basename(url).split('_', 1)[0]
                    if (prefix == os.path.basename(url)):
                        prefix = ''
                    else:
                        prefix = prefix + '_'
                    filename = secrets.token_hex(nbytes=16) + ".jpg"
                    countrepeat = 10
                    while countrepeat > 0:
                        if (not os.path.exists(path + "/" + prefix + filename)):
                            try:
                                print(serverurl + url)
                                image = requests.get(serverurl + url, stream=True)
                                count = count + 1
                                countrepeat = 0
                            except ConnectionError as h:
                                print(
                                    path + "/" + prefix + filename + " could not be loaded - Retry in 10 s ... " + str(
                                        countrepeat))
                                time.sleep(10)
                                countrepeat = countrepeat - 1
                                continue
                            except TimeoutError as h:
                                print(
                                    path + "/" + prefix + filename + " could not be loaded - Retry in 10 s ... " + str(
                                        countrepeat))
                                time.sleep(10)
                                countrepeat = countrepeat - 1
                                continue

                            try:
                                img = Image.open(image.raw)
                                img.save(path + "/" + prefix + filename)
                            except Exception as e:
                                print(path + "/" + prefix + filename + " could not be opened as an image: %r!" % e)

                            count = count + 1
                            countrepeat = 0
    print(f"{count} images are loaded from meter: {servername}")

def save_hash_file(images, hashfilename):
    f =  open(hashfilename, 'w', encoding='utf-8')
    for hash, img, meter, datum in images:
        f.write(datum + "\t" + meter+ "\t" + img + "\t" + str(hash)+'\n');
    f.close

def load_hash_file(hashfilename):
    images = []

    try:
        file1 = open(hashfilename, 'r')
        Lines = file1.readlines()
        file1.close
    except Exception as e:
        print('No historic Hashdata could be loaded (' + hashfilename + ')')
        return images

    for line in Lines:
        cut = line.strip('\n').split(sep="\t")
        datum = cut[0]
        meter = cut[1]
        _hash = imagehash.hex_to_hash(cut[3])
        images.append([_hash, cut[2], meter, datum])
    return images


def ziffer_data_files(input_dir):
    '''return a list of all images in given input dir in all subdirectories'''
    imgfiles = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if (file.endswith(".jpg")):
                imgfiles.append(root + "/" + file)
    return  imgfiles

def remove_similar_images(image_filenames, meter, hashfunc = imagehash.average_hash, savedublicates=False):
    '''removes similar images. 
    
    '''
    images = []
    count = 0
    cutoff = 3  # maximum bits that could be different between the hashes. 
    print(f"Find similar images now in {len(image_filenames)} images ..." )

    datum = date.today().strftime("%Y-%m-%d")

    for img in sorted(image_filenames):
        try:
            hash = hashfunc(Image.open(img).convert('L').resize((32,20)))
        except Exception as e:
            print('Problem: ', e, ' with ', img)
            continue
        images.append([hash, img, meter, datum])
  
    if (os.path.exists('./data/HistoricHashData.txt')):
        HistoricHashData = load_hash_file('./data/HistoricHashData.txt')
    else:
        HistoricHashData = []

    count = 0

    duplicates = {}
    for hash in images:
        if (hash[1] not in duplicates):
            similarimgs = [i for i in HistoricHashData if abs(i[0]-hash[0]) < cutoff and i[1]!=hash[1]]
            if len(similarimgs) > 0:               # es wurden in den alten hashes schon vergleichbare bilder gefunden
                if (duplicates == {}):
                    duplicates = set([hash[1]])
                else:
                    duplicates |= set([hash[1]])                
            else:                                   # es wird in den neuen Biler gesucht gefunden
                similarimgs = [i for i in images if abs(i[0]-hash[0]) < cutoff and i[1]!=hash[1]]
                # add duplicates
                if (duplicates == {}):
                    duplicates = set([row[1] for row in similarimgs])
                else:
                    duplicates |= set([row[1] for row in similarimgs])
        count = count + 1
        if not count % 1000:
            print("..." + str(count))

    # extend Historic Hash Data
    for _image in images:
        if not _image[1] in duplicates:
            HistoricHashData.append(_image)
    save_hash_file(HistoricHashData, './data/HistoricHashData.txt')
            
    # remove now all duplicates
    if savedublicates:
        print(f"{len(duplicates)} duplicates will moved to .data/raw_images/dublicates.")
        os.makedirs(target_store_dublicates, exist_ok=True)
        for image in duplicates:
            os.replace(image, os.path.join(target_store_dublicates, os.path.basename(image)))
    else:
        print(f"{len(duplicates)} duplicates will be removed.")
        for image in duplicates:
            os.remove(image)

def move_to_label(files, meter):
    print("Move to label")
    os.makedirs(target_label_path, exist_ok=True)
    for file in files:
        os.replace(file, os.path.join(target_label_path, os.path.basename(file)))

       


def collect(meter, days, keepolddata=False, download=True, startlabel=0, savedublicates=False):
    # ensure the target path exists
    os.makedirs(target_raw_path, exist_ok=True)
    print("Startlabel", startlabel)
    # read all images from meters
    if download:
        print("retrieve images")
        readimages(meter, target_raw_path, days)
    
    # remove all same or similar images and remove the empty folders
    remove_similar_images(ziffer_data_files(os.path.join(target_raw_path, meter)), meter, savedublicates=savedublicates)

    # move the files in one zip without directory structure
    move_to_label(ziffer_data_files(os.path.join(target_raw_path, meter)), meter)

    # cleanup
    if not keepolddata:
        shutil.rmtree(target_raw_path)

    # label now
    label(target_label_path, startlabel=startlabel)


