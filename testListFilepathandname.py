import os

path = "E:\APP UItesting"
for fpath,dirname,fnames in os.walk(path):
    #print(fpath)
    print(dirname)