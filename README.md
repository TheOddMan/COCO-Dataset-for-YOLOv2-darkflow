
You can use getImage.py to download coco images from coco json file.

Sometimes you will get ConnectionResetError because of the remote server resctriction.
If this program is blocked, it will "ignore that image" and sleep 1 min and then continute to run.
So, after finishing the program, maybe you will miss some images.
You can run it and redownload. (Images you've downloaded won't be downloaded again.)
