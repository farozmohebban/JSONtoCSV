#import libraries
import csv
import json

#open, read, and load the .har file
input_file = open('vendor.har')
json_str = input_file.read()
json_data = json.loads(json_str)
input_file.close()

#apply initial values
cnt_get, cnt_post, cnt = 0,0,0
unique_v1, unique_v2 = [],[]

#create a new parameter to make the code shorter 
json_entries=json_data['log']["entries"]

#for loop to loop through all the enteries
for item in json_entries:

	#count number of GET and POST for all methods of entry
	cnt_get += item['request']['method'].count("GET")
	cnt_post += item['request']['method'].count("POST")

	#loop through cookies of all entries to find the list of entries in 'sessionid' in them
	for j in range(len(item['request']['cookies'])):
		if (item['request']['cookies'][j]['name'] == 'sessionid') : 

			#store sessionid values for entries with 'sessionid' in their cookies
			unique_v1.append(item['request']['cookies'][j]['value'])

			#store `csrftoken` values for all the entries that have 'sessionid' in their cookies.
			#`csrftoken` list always comes right before 'sessionid' list
			unique_v2.append(item['request']['cookies'][j-1]['value'])


#answers to the questions in the test
print ("Number of GETs in the file: "+str(cnt_get)+" out of overall "+str(len(json_entries))+" entries")
print ("Number of POSTs in the file: "+str(cnt_post)+" out of overall "+str(len(json_entries))+" entries")
print ("Set of unique values for sessionid is: "+str(set(unique_v1)))
print ("Set of unique values for csrftoken is: "+str(set(unique_v2)))




#This Python code returns two csv files:
#1. CSV created for items in 'response' dicionary
output_file = open('csv_srsexam.csv', 'w')
output = csv.writer(output_file)

output.writerow(("status", 
	"statusText", "cookies", "headers",
    "redirectURL",
    "headersSize",
    "bodySize"))

for line in json_entries:
	output.writerow((line['response']['status'],
		line['response']['statusText'],
		line['response']['cookies'],
		line['response']['headers'],
		line['response']['redirectURL'],
		line['response']['headersSize'],
		line['response']['bodySize']
		))

#2. JSON filed dumped in a CSV file
with open("job_postings.csv", "w") as write_file:
    json.dump(json_data, write_file)


print ("CSV file 'csv_srsexam.csv' and 'job_postings.csv' are created")