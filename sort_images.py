
import argparse
import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS

date_file_pairs = {'':[]}
delim = '_'

def del_empty_folders(mypath):
    folders = list(os.walk(mypath,topdown=False))[:-1]

    for folder in folders:
        # folder is a tuple ('path', ['folders list'], ['files list'])
        if not folder[2]:
            os.rmdir(folder[0])

def count_files(mypath):
    num_of_files = 0
    #performing BFS on folders
    q=[mypath]
    while q:
        temp = q.pop(0)
        for item in os.listdir(temp):
            item = os.path.join(temp, item)
            if os.path.isfile(item):
                num_of_files+=1
            elif os.path.isdir(item):
                q.append(item)
    return num_of_files

def get_date_taken(img):
    exifdata = img._getexif()
    if exifdata:
        try:
            return img._getexif()[36867] # or maybe this [36868]
        except KeyError:
            pass
        try:
            return img._getexif()[36868]
        except:
            pass
    return ""

def store_file(mfile):
    try:
        img_obj = Image.open(mfile)
    except:
        # print('unable to open file :',end=' ');print(mfile)
        date_file_pairs[''].append(mfile)
        return
    date_str = get_date_taken(img_obj)
    if date_str == '':
        # print("couldn't find date on exif data :",end = ' ');print(mfile)
        date_file_pairs[''].append(mfile)
        return
    date_str = date_str[:7]
    date_str = date_str.replace(':',delim)
    if date_str in date_file_pairs:
        date_file_pairs[date_str].append(mfile)
    else:
        date_file_pairs[date_str] = [mfile]

def sort_files(mypath):
    q=[mypath]
    while q:
        temp = q.pop(0)
        for item in os.listdir(temp):
            item = os.path.join(temp, item)
            if os.path.isfile(item):
                store_file(item)
            elif os.path.isdir(item):
                q.append(item)


def move_files(root):
    if date_file_pairs=={}:return
    for date_str,path_list in date_file_pairs.items():
        # uncomment this line if you dont want to move file 
        # which don't have metadata or not jpg files
        # if date_str == '':continue
        new_path = os.path.join(root,date_str)
        try:
            os.mkdir(new_path)
        except FileExistsError:
            pass
        for i in path_list:
            try:
                shutil.move(i,new_path)
            except shutil.Error:
                # error occurs if dest path already exists
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description ='sort some integers.')
    parser.add_argument('-p','--path',help ='path of the directory to sort files',required=True)

    args = parser.parse_args()
    rootpath = args.path

    sort_files(rootpath)
    move_files(rootpath)
    del_empty_folders(rootpath)