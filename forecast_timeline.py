""" Used to take in the directories of different file formats and plot the timeline over which they exist so that the dates may be compared. Calling either the xml or txt formatted timestamp function which will produce and time array and corresponding array of the same y value so that the plot is a straigh line, it plots them all onto the same graph."""

import xml.etree.cElementTree as ET
import datetime as dt
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
# Set up a path to the files and loop through the directory. Read them using Element Tree to extract the issue date of each forecast file. The specific issuetime child node is accessed using index [0],[1] in this particular case.

def timestamp_min_xml(path,height,data_label):
	file_list = []
	issuetimes = []
	y = []
	for filename in os.listdir(path):
		if not filename.endswith('.xml'): continue
		fullname = os.path.join(path, filename)
		file_list.append(fullname)
		tree = ET.parse(fullname)
		root = tree.getroot()
		# String converted to datetime format.
		issuetime = dt.datetime.strptime(root[0][1].text, '%Y-%m-%dT%H:%MZ')
		issuetimes.append(issuetime)
		y.append(height)

	x = issuetimes
	print data_label, "range of forecast", issuetimes[0], issuetimes[len(issuetimes)-1]
	return x, y



def timestamp_sec_xml(path,height,data_label):
	file_list = []
	issuetimes = []
	y = []
	for filename in os.listdir(path):
		if not filename.endswith('.xml'): continue
		fullname = os.path.join(path, filename)
		file_list.append(fullname)
		tree = ET.parse(fullname)
		root = tree.getroot()
		# String converted to datetime format.
		issuetime = dt.datetime.strptime(root[0][1].text, '%Y-%m-%dT%H:%M:%SZ')
		issuetimes.append(issuetime)
		y.append(height)

	x = issuetimes
	print data_label, "range of forecast", issuetimes[0], issuetimes[len(issuetimes)-1]
	return x, y 

def timestamp_xml_zless(path,height,data_label):
	file_list = []
	issuetimes = []
	y = []
	for filename in os.listdir(path):
		if not filename.endswith('.xml'): continue
		fullname = os.path.join(path, filename)
		file_list.append(fullname)
		tree = ET.parse(fullname)
		root = tree.getroot()
		# String converted to datetime format.
		issuetime = dt.datetime.strptime(root[0][1].text, '%Y-%m-%dT%H:%M:%S')
		issuetimes.append(issuetime)
		y.append(height)

	x = issuetimes
	print data_label, "range of forecast", issuetimes[0], issuetimes[len(issuetimes)-1]
	return x, y

def timestamp_txt(path,height,data_label):
	file_list = []
	issuetimes = []
	y = []
	for filename in os.listdir(path):
		fullname = os.path.join(path, filename)
		file_list.append(fullname)
		
		with open(fullname, 'r') as infile:
    			for line in infile:
        			if 'Issue Time' in line:
            				time_skipline = line.replace('Issue Time: ','')
					time = time_skipline.replace('\n','')
					issuetime = dt.datetime.strptime(time, '%Y-%m-%dT%H:%MZ')
					issuetimes.append(issuetime)
		y.append(height)

	x = issuetimes
	print data_label, "range of forecast", issuetimes[0], issuetimes[len(issuetimes)-1]
	return x, y

def timestamp_dat1(path,height,data_label):
	file_list = []
	issuetimes = []
	y = []
	for filename in os.listdir(path):
		fullname = os.path.join(path, filename)
		file_list.append(fullname)
		
		with open(fullname) as infile:
			next(infile)
			next(infile)	    		
			reader = csv.reader(infile, delimiter=" ")
			for line in reader:
				day = line[1]
				month = line[2]
				year = line[3]
				date = str(day)+':'+str(month)+':'+str(year)
				issuetime = dt.datetime.strptime(date, 'd0=%d:m0=%m:y0=%Y')
				issuetimes.append(issuetime)
				y.append(height)

	x = issuetimes
	print data_label, "range of forecast", issuetimes[0], issuetimes[len(issuetimes)-1]
	return x, y


def timestamp_txt2(path,height,data_label):
	file_list = []
	issuetimes = []
	y = []
	for filename in os.listdir(path):
		fullname = os.path.join(path, filename)
		file_list.append(fullname)
		
		with open(fullname) as infile:
			next(infile)   		
			reader = csv.reader(infile, delimiter=" ")
			for line in reader:
				year=line[0]
				month=line[1]
				day=line[2]
				hour = line[3]
				minute = line[4]
				date = str(year)+':'+str(month)+':'+str(day)+':'+str(hour)+':'+str(minute)
				issuetime = dt.datetime.strptime(date, '%Y:%m:%d:%H:%M')
				issuetimes.append(issuetime)
				y.append(height)

		

	x = issuetimes
	print data_label, "range of forecast", issuetimes[0], issuetimes[len(issuetimes)-1]
	return x, y




#Create list of paths to different model sets in the directory
directory = ['/home/aisling/Flare_Scoreboard/ASAP_v1_xml_min' , '/home/aisling/Flare_Scoreboard/BoM_flare1_xml_min','/home/aisling/Flare_Scoreboard/MO_TOT1_xml_sec','/home/aisling/Flare_Scoreboard/NOAA_1_xml_min','/home/aisling/Flare_Scoreboard/AMOS_v1_txt','/home/aisling/Flare_Scoreboard/ASSA_24H_1_txt','/home/aisling/Flare_Scoreboard/SIDC_v2_xml_zless','/home/aisling/Flare_Scoreboard/MOXray_FlareForecasts_dat1','/home/aisling/Flare_Scoreboard/solarmonitor_dat2']

# Create color array for different data sets and set n to one for updating throughout the loop.
data_label = ["ASAP_v1", "BoM_1","MO_TOT1","NOAA_1","AMOS_v1","ASSA_24H", "SIDC_v2","MOXrayFF","Sol_Mon"]
c = ['forestgreen','yellowgreen','orange','darkorange','orangered','maroon','darkslateblue','royalblue','steelblue']
n = 0 
height = 0

#The xml and txt files are separated as are relative min and sec based files, they are then run through the corresponding function to determine the range of time values that make up the x array for the plot and a y array is created to match it.

for path in directory:
	
	if 'xml_min' in path:
		x, y = timestamp_min_xml(path,height,data_label[n])
		plt.scatter(x,y,s=1, color=c[n])
	
	elif 'xml_sec' in path:
		x, y = timestamp_sec_xml(path,height,data_label[n])
		plt.scatter(x,y,s=1, color=c[n])
	
	elif 'xml_zless' in path:
		x, y = timestamp_xml_zless(path,height,data_label[n])
		plt.scatter(x,y,s=1, color=c[n])
	
	elif 'txt' in path:
		x,y = timestamp_txt(path,height,data_label[n])
		plt.scatter(x,y,s=1, color=c[n])
	elif 'dat1' in path:
		x,y = timestamp_dat1(path,height,data_label[n])
		plt.scatter(x,y,s=1, color=c[n])
	elif 'dat2' in path:
		x,y = timestamp_txt2(path,height,data_label[n])
		plt.scatter(x,y,s=1, color=c[n])

	n = n+1
	height = height + 1

# Timestamp the x-axis
plt.gcf().autofmt_xdate()

# Label the y-axis
y_axis = np.arange(0,len(data_label))
plt.yticks(y_axis, data_label)

#Add a title
plt.title('Flare Forecast Timeline Comparison')

plt.show()

