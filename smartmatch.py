import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

d={}
dlist=[]
d.clear()

file3 = open('/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/order_records.csv', 'r')
for line2 in file3:
    file2 = open(''.join(["/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/", line2.split(',')[1].rstrip()]), 'r')
    d['orderid']=line2.split(',')[1].rstrip()
    d['factory']=line2.split(',')[2].rstrip()
    for line in file2:
        d[line.split(',')[0].rstrip()]=line.split(',')[1].rstrip()
    
    file2.close()
    
    dlist.append(d.copy())
    d.clear()
    
file3.close()

#print(len(dlist))

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'shirt02.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

response = client.label_detection(image=image)
labels = response.label_annotations

os.remove("/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/input_image.csv")

d2={}
d2.clear()

file = open('/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/input_image.csv','a')

for label in labels:
    file.write(''.join([label.description, ",", str(round(label.score,9)), "\n"])) 
    d2[label.description.rstrip()]=str(round(label.score,9)).rstrip()
    
file.close()

print (dlist[0])

#for order in range(0,len(dlist)):
#	score=0
#	if list(d2.keys())[order] in dlist[order]
#	    print(list(d2.keys())[order])
#	    print("OK")
 #   else
  #      print(list(d2.keys())[order])
   #     print("NOT OK")

#print(list(d2.keys())[0])
#print(list(d2.values())[0])

#if 'key1' in dict:
#  print "blah"
#else:
#  print "boo"

