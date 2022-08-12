import os
import shutil
import tempfile
import cv2
import numpy
import json
from wand.image import Image
from PIL import Image


########################################################################################################################
temp_folder = tempfile.TemporaryDirectory()
temp_folder_path = temp_folder.name
print("Temporary folder one",temp_folder_path)
#########################################################################################


path = "data/Folder/Folder"
images = [f for f in os.listdir(path) if '.tif' in f.lower()]


for image in images:
    new_path = temp_folder_path+"\\" +image
    #print(new_path)
    shutil.copy(path +"\\"+image, new_path)
print(".TIF images have been copied to the temporary folder")

#############################################################################################
temp_folder_0 = tempfile.TemporaryDirectory()
temp_folder_path_0 = temp_folder_0.name
print("Temporary folder two",temp_folder_path_0)

path = temp_folder_path
images = [f for f in os.listdir(path) if '.tif' in f.lower()]

for i in images:
    im = Image.open(path+"\\"+i)
    print(i)

# JPG conversion
    rgb_im = im.convert("RGB")
    print("Converting"+i)

# exporting the image and renaming
    rgb_im.save(temp_folder_path_0+"//"+i.replace("tif", "jpg"))
for i in os.listdir(temp_folder_path_0):
    print(i)






########################################################################################################################


path = "data/Folder/Folder"
counter = [f for f in os.listdir(temp_folder_path) if '.tif' in f.lower()]




########################################################################################################################

#EXTRACTING DATA FROM THE INFO FILE

images = [f for f in os.listdir(path) if '.info' in f.lower()]



with open(path+"//"+images[0]) as f:
    lines = f.readlines()
    da = [i for i in lines if "pixelsize" in i.lower()]
    la = [i for i in lines if "tif" in i.lower()]
    pixel_size = da[0].split()
    pixel_x = pixel_size[1]
    pixel_y = pixel_size[2]
   # print(la)
    z_axis = la[0].split()
    z_value = float(z_axis[1])
    f.close()
#print(z_axis, pixel_x, pixel_y)

with open(path+"//"+images[1]) as f:
    lines = f.readlines()
    la = [i for i in lines if "tif" in i.lower()]
    z_axis = la[0].split()
    z_value_2 = float(z_axis[1])
    volume_data = int(z_value_2 - z_value)
    f.close()
#print(volume_data)
########################################################################################################################




########################################################################################################################
counter = [f for f in os.listdir(temp_folder_path_0) if '.jpg' in f.lower()]
slices = len(counter)
image = cv2.imread(temp_folder_path_0 + "\\" + counter[0])
dimensions = image.shape
height = image.shape[0]
width = image.shape[1]
channels = image.shape[2]
array_out = {
   "type": "image",
  "data_type": str(image.dtype),
  "num_channels": channels,
  "scales": [
    {
      "chunk_sizes": [],
      "encoding": "jpeg",
      "key": "full",
      "resolution": [int(pixel_x), int(pixel_y), volume_data],
      "size": [height, width, slices],
      "voxel_offset": [0, 0, 0]
    }
  ]

  }

with open('data.json', 'w') as f:
    json.dump(array_out, f)


########################################################################################################################

os.system("generate-scales-info data.json output --target-chunk-size 128")
os.system("dir" + " "+ temp_folder_path_0)
os.system("slices-to-precomputed --input-orientation RPS "+ temp_folder_path_0 + " "+ "output")
