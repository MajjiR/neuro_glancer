from PIL import Image
import os
path = "data/Folder/Folder"
images = [f for f in os.listdir(path) if '.tif' in f.lower()]

for i in images:
    im = Image.open(path+"\\"+i)
    print(images[0])

# JPG conversion
    rgb_im = im.convert("RGB")

# exporting the image and renaming
    rgb_im.save("OUTPUT_FOLDER//"+i.replace("tif", "jpg"))
