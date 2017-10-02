"""" 
Aisling Bergin 
27 Sept 2017


AIM: Take in the directories of different file formats and plot the timeline over which they exist so that the dates may be compared. Separating the xml/txt/dat formatted files and determining the issue times of each forecast, to produce a time array and corresponding array of equal y values (so that the plot is a straight line), it plots them all onto the same graph.

Input: directory of files of dat/xml/txt files labelled accordingly from a known directory with known structure.
Output: Graph of issue times for which data exists within the files.

"""

import xml.etree.cElementTree as ET
import datetime as dt
import os
import matplotlib.pyplot as plt
import numpy as np
import csv


DIR = '/home/aisling/Flare_Scoreboard/'

#Create list of paths to known model sets in the directory
directory = ['AMOS_v1_txt','ASAP_v1_xml_min', 'ASSA_24H_1_txt', 'BoM_flare1_xml_min', 'MO_TOT1_xml_sec', 'SIDC_v2_xml_zless', 'NOAA_1_xml_min', 'MOXray_FlareForecasts_dat1', 'solarmonitor_dat2']

short_name = [elem.split('_')[0] for elem in directory]  # convert to simple labels

# Create color array for different data sets shown in the graph. 
c = ['forestgreen','yellowgreen','orange','darkorange','orangered','maroon','darkslateblue','royalblue','steelblue']

# Set n and height to 0 for updating throughout the loop.
n = 0 
height = 0

#The xml,txt and dat files are separated and subsequently divided based on their time format. The range of time values that make up the x array for the plot are determined for each and an equal length y array is created to match it.

for data_label in directory:
	
	path = str(DIR) + str(data_label)  # create paths to the directory of files
	issuetimes = []	# Reset the list of issuetimes to empty for each iteration
	

	for filename in os.listdir(path):
		fullname = os.path.join(path, filename)

		# XML : Read files using Element Tree to extract the issue date of each forecast file. 		#
		# The specific issuetime child node is accessed using index [0],[1] in this particular case.	#

		if 'xml' in path:
			tree = ET.parse(fullname)
			root = tree.getroot()
							# String converted to datetime format based on second/minute classification.
			if 'xml_sec' in path:
				issuetime = dt.datetime.strptime(root[0][1].text, '%Y-%m-%dT%H:%M:%SZ')
			elif 'xml_min' in path:
				issuetime = dt.datetime.strptime(root[0][1].text, '%Y-%m-%dT%H:%MZ')
			elif 'xml_zless' in path:
				issuetime = dt.datetime.strptime(root[0][1].text, '%Y-%m-%dT%H:%M:%S')

			issuetimes.append(issuetime)
				

		# TXT : Read through files using the trigger 'Issue Time' to identify the line on which the issue 	#
		# time of each forecast file lies. This line is read in as a string with irrelevent title and line skip #
		# removed to extract the issue time.									#
		
		elif 'txt' in path:
			with open(fullname, 'r') as infile:
				for line in infile:
					if 'Issue Time' in line:
			 			time_skipline = line.replace('Issue Time: ','')
						time = time_skipline.replace('\n','')
						issuetime = dt.datetime.strptime(time, '%Y-%m-%dT%H:%MZ')
			issuetimes.append(issuetime)	
			


		# DAT : Read through files knowing the details of how many title rows to remove. csv is used to take	#
		# the file in as 'reader' and using knowledge of data postioned in the text the issue times are 	#
		# extracted and converted into relevent format. dat{1,2} are arbitrary numbers used to separate 	#
		# different table formats.


		elif 'dat' in path:
			with open(fullname) as infile:
				if 'dat1' in path:
					next(infile) 	# skip header
					next(infile)	# skip column label	    		
					reader = csv.reader(infile, delimiter=" ") 	# read file separated by spaces
					for line in reader:		# extract separate columns		
						day = line[1]
						month = line[2]
						year = line[3]
						date = str(day)+':'+str(month)+':'+str(year) # put columns into format easier to use with dt
						issuetime = dt.datetime.strptime(date, 'd0=%d:m0=%m:y0=%Y')
						issuetimes.append(issuetime)
						
				elif 'dat2' in path:
					next(infile)   	# skip header	
					reader = csv.reader(infile, delimiter=" ")	# read file separated by spaces
					for line in reader:		# extract separate columns
						year=line[0]
						month=line[1]
						day=line[2]
						hour = line[3]
						minute = line[4]
						# put columns into format easier to use with dt
						date = str(year)+':'+str(month)+':'+str(day)+':'+str(hour)+':'+str(minute)
						issuetime = dt.datetime.strptime(date, '%Y:%m:%d:%H:%M')
						issuetimes.append(issuetime)	

	print "Range of " , str(short_name[n]), " forecast:", issuetimes[0], " to ", issuetimes[len(issuetimes)-1]
	
	y=np.full(len(issuetimes),height)
	plt.scatter(issuetimes,y,s=1, color=c[n])

	n = n+1
	height = height + 1

# Timestamp the x-axis
plt.gcf().autofmt_xdate()

# Label the y-axis
y_axis = np.arange(0,len(short_name))
plt.yticks(y_axis, short_name)

#Add a title
plt.title('Flare Forecast Timeline Comparison'
 2016-08-25 22:00:00

plt.show()

