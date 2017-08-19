import io
import os
import sys

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

d={}
dlist=[]
d.clear()

file3 = open('/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/order_records.csv', 'r')
for line2 in file3:
    file2 = open(''.join(["/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/", line2.split(',')[1].rstrip()]), 'r')
    d['orderid']=line2.split(',')[0].rstrip()
    d['factory']=line2.split(',')[2].rstrip()
    for line in file2:
        d[line.split(',')[0].rstrip()]=line.split(',')[1].rstrip()
    
    file2.close()
    
    dlist.append(d.copy())
    d.clear()
    
file3.close()

input_weight={}

weight_file = open('/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/scoring_weight.csv', 'r')

for weight in weight_file:
    input_weight[weight.split(',')[0].rstrip()]=weight.split(',')[1].rstrip()
    
weight_file.close()

fac_dict={}
fac_list=[]

fac_file = open('/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/factory.csv', 'r')
for factory in fac_file:
    fac_dict['facid']=factory.split(',')[0].rstrip()
    fac_dict['capacity']=factory.split(',')[1].rstrip()
    fac_dict['performance']=factory.split(',')[2].rstrip()
    fac_dict['certified']=factory.split(',')[3].rstrip()
    
    fac_list.append(fac_dict.copy())
    fac_dict.clear()
    
fac_file.close()

#print(len(dlist))

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    str(sys.argv[1]))

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

response = client.label_detection(image=image)
labels = response.label_annotations

os.remove(''.join(["/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/", str(sys.argv[1]).split('.')[0], ".csv"]))

d2={}
d2.clear()

file = open(''.join(["/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/", str(sys.argv[1]).split('.')[0], ".csv"]),'a')

for label in labels:
    file.write(''.join([label.description, ",", str(round(label.score,9)), "\n"])) 
    d2[label.description.rstrip()]=str(round(label.score,9)).rstrip()
    
file.close()

fac_result_dict={}
temp_fac_dict={}
fac_result_list=[]

for fac_item in range(0,len(fac_list)):
	fac_result_dict.clear()
	fac_score=0
	
	temp_fac_dict = fac_list[fac_item]
	
	fac_result_dict['facid']=temp_fac_dict['facid']

	for fac_element in range(1,len(fac_list[fac_item])):
		if list(temp_fac_dict.keys())[fac_element] in input_weight:
			fac_score += round(float(temp_fac_dict[list(temp_fac_dict.keys())[fac_element]])*float(input_weight[list(temp_fac_dict.keys())[fac_element]]),2)
			fac_result_dict[list(temp_fac_dict.keys())[fac_element]]=str(round(float(temp_fac_dict[list(temp_fac_dict.keys())[fac_element]])*float(input_weight[list(temp_fac_dict.keys())[fac_element]]),2))
		else:
			fac_score += round(float(temp_fac_dict[list(temp_fac_dict.keys())[fac_element]]),2)
			fac_result_dict[list(temp_fac_dict.keys())[fac_element]]=str(round(float(temp_fac_dict[list(temp_fac_dict.keys())[fac_element]]),2))
	
	fac_result_dict['score']=str(round(fac_score,2))
	fac_result_list.append(fac_result_dict.copy())

sorted_fac_result_list = sorted(fac_result_list, key=lambda d: d['score'], reverse=True)

os.remove("/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/factory_evaluation.csv")

result_file = open('/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/factory_evaluation.csv','a')

for result in range(0,len(sorted_fac_result_list)):
    result_file.write(''.join([sorted_fac_result_list[result]["facid"], ",", sorted_fac_result_list[result]["score"], "\n"])) 
    
result_file.close()

os.remove("/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/fac_score_details.csv")

score_file = open('/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/fac_score_details.csv','a')

for score_result in range(0,len(sorted_fac_result_list)):
	score_file.write(str(sorted_fac_result_list[score_result]).strip("{").strip("}"))
	score_file.write("\n")
    
score_file.close()

result_dict={}
result_list=[]

for order in range(0,len(dlist)):
	result_dict.clear()
	score=0
	result_dict['orderid']=dlist[order]["orderid"]
	result_dict['factory']=dlist[order]["factory"]
	
	for element in range(0,len(d2)):
		if list(d2.keys())[element] in dlist[order]:
			if list(d2.keys())[element] in input_weight:
				score += round((1-abs(float(dlist[order][list(d2.keys())[element]]) - float(list(d2.values())[element])))*float(input_weight[list(d2.keys())[element]]),2)
				result_dict[list(d2.keys())[element]]=str(round((1-abs(float(dlist[order][list(d2.keys())[element]]) - float(list(d2.values())[element])))*float(input_weight[list(d2.keys())[element]]),2))
			else:
				score += round(1-abs(float(dlist[order][list(d2.keys())[element]]) - float(list(d2.values())[element])),2)
				result_dict[list(d2.keys())[element]]=str(round(1-abs(float(dlist[order][list(d2.keys())[element]]) - float(list(d2.values())[element])),2))
		else:
			result_dict[list(d2.keys())[element]]=0
	

	result_dict['score']=str(round(score,2))
	result_list.append(result_dict.copy())
	
sorted_result_list = sorted(result_list, key=lambda d: d['score'], reverse=True)

os.remove("/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/factory_ranking.csv")

result_file = open('/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/factory_ranking.csv','a')

for result in range(0,len(sorted_result_list)):
    result_file.write(''.join([sorted_result_list[result]["orderid"], ",", sorted_result_list[result]["factory"], ",", sorted_result_list[result]["score"], "\n"])) 
    
result_file.close()

os.remove("/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/order_score_details.csv")

score_file = open('/Users/LESTERMOK/Documents/Virtualenvs/smartmatch/smartmatch/order_score_details.csv','a')

for score_result in range(0,len(sorted_result_list)):
	score_file.write(str(sorted_result_list[score_result]).strip("{").strip("}"))
	score_file.write("\n")
    
score_file.close()



