from math import sqrt
import pandas as pd
import json

data = pd.read_csv("C:/Users/Stasya/Desktop/HateCrime/DS_project/Hate_crime_data.csv")
geo_crime=data.loc[:,['Маркер_lat','Маркер_lng']]

crime_locs=[]

for index, row in geo_crime.iterrows():
    crime_locs.append((row['Маркер_lat'],row['Маркер_lng']))

def distance(point1, point2):
    d=sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    return d

def accuracy(precision,value):
    result=round(value,precision)
    return result

def distance_with_precision(precision,*dots):
    return accuracy(precision,distance(*dots))

myfile = "C:/Users/Stasya/Desktop/HateCrime/DS_project/Moscow_metro.json"
with open(myfile) as f:
    mydata = json.load(f)  
metro_lines={}
for element in mydata:
    metro_lines[element["name"]]=0
for dot in crime_locs:
    far=10000
    closest_line=None
    for element in mydata:
        for data in element["stations"]:
            new_dist=distance_with_precision(4,(dot),(float(data["lat"]),float(data["lng"])))
            if new_dist<far:
                far=new_dist
                closest_line=element["name"]
    if far<=0.004:#distance from the attack location to a closest metro station (no more than 300 m)
        metro_lines[closest_line]+=1            

def print_lines_rank(alist):
    most_dangerous=sorted(alist,key=alist.get,reverse=True)[:3]
    print("Most dangerous underground lines in Moscow are:")
    for i in range (len(most_dangerous)):
        print("{}.{}".format(i+1,most_dangerous[i]))

def print_stations_rank(alist):
    most_dangerous=sorted(alist,key=alist.get,reverse=True)[:3]
    print("Most dangerous stations in Moscow are:")
    for i in range (len(most_dangerous)):
        print("{}.{}".format(i+1,most_dangerous[i]))

metro_lines={}
for element in mydata:
    metro_lines[element["name"]]=0
for dot in crime_locs:
    far=10000
    closest_line=None
    for element in mydata:
        for data in element["stations"]:
            new_dist=distance_with_precision(4,(dot),(float(data["lat"]),float(data["lng"])))
            if new_dist<far:
                far=new_dist
                closest_line=element["name"]
    if far<=0.00914:#distance from the attack location to a closest metro station (no more than 1000 m)
        metro_lines[closest_line]+=1

print_lines_rank(metro_lines)

#Count incidents for stations
metro_stations={}
for element in mydata:
    for data in element["stations"]:
        metro_stations[data["name"]]=0
for dot in crime_locs:
    far=10000
    closest_line=None
    for element in mydata:
        for data in element["stations"]:
            new_dist=distance_with_precision(4,(dot),(float(data["lat"]),float(data["lng"])))
            if new_dist<far:
                far=new_dist
                closest_station=data["name"]
    if far<=0.00914:#distance from the attack location to a closest metro station (no more than 300 m)
        metro_stations[closest_station]+=1 


#print(metro_stations)
print_stations_rank(metro_stations)
 
 
