# COMMAND LINE PROMPT: pip install bs4
# for general packages: pip install <package_name>
from bs4 import BeautifulSoup
import requests
import csv
from pathlib import Path
import os

def day_finder(text):
    days = []
    for i in range(len(text)):
        if text[i] == '(':
            word = text[i + 1:]
            for j in range(len(word)):
                if word[j] == ')':
                    word = word[:j] 
                    days.append(word)
                    break
    return days

def trimmer(text):
    for i in range(len(text)):
        if text[i] == ',':
            word = text[:i]
            return word

class_list = []
final_list = []

script_path = os.path.abspath(__file__) #Gives path to script file
script_dir = os.path.dirname(script_path) # Gets directory that script resides in

with open(Path(script_dir) / 'Input' / 'classes.csv') as csvr: # Path() overloads '/' operator into acting as file slash #mode = 'r' is default for open()
    csvread = csv.reader(csvr)
    for row in csvread:
        for string in row:
            if not string.find("Class"):
                continue
            class_list.append(string)

source = "https://www.unr.edu/admissions/records/academic-calendar/finals-schedule"

request = requests.get(source)

parser = BeautifulSoup(request.text, 'html.parser')
for table in parser.find_all('table'):
    # Displays the day of the final, though this can likely be overridden in favor of a counter which contains the exam day (i.e, 1 is thursday, 2 is friday...)
    caption = trimmer(table.find('caption').text)
    tbody = table.find('tbody')
    for tr in tbody.find_all('tr'):
        # Contains all exam info needed, first value is regular class start time, second value is what days the class regularly meets, third value is the time block for the final
        tdlist = tr.find_all('td')
        class_start = tdlist[0].text 
        class_day = day_finder(tdlist[1].text) 
        exam_start = tdlist[2].text 

        if class_start in class_list:
            index = class_list.index(class_start)
            seconds = 0
            try:
                seconds = class_list.index(class_start, index + 1)
            except ValueError:
                seconds = 0
            if class_list[index + 1] in class_day:
                final_list.append(class_list[index + 2])
                final_list.append(caption)
                final_list.append(exam_start)
            if seconds != 0:
                if class_list[seconds + 1] in class_day:
                    final_list.append(class_list[seconds + 2])
                    final_list.append(caption)
                    final_list.append(exam_start)

print(final_list)

os.makedirs(Path(script_dir) / 'Output', exist_ok=True) # Creates the Output folder, exist_ok allows for function after the folder already exists
with open(Path(script_dir) / 'Output' / 'finals.csv', mode = 'w') as output:
    csvwrite = csv.writer(output)
    csvwrite.writerow(['Class','Exam Day','Exam Time'])
    for i in range(len(class_list) // 3):
        csvwrite.writerow([final_list[3*(i-1)],final_list[3*(i-1)+1],final_list[3*(i-1)+2]])
    
# Final output: List [First exam class name, first exam day, first exam time, Second exam class name, second exam day, second exam time, ...]

#########################################################################################
#########################################################################################
###
###                 BEAUTIFUL SOUP / PYTHON PLAYGROUND
###
###     Playing around with basic python looping / Beautiful Soup parser
###
###     #print(parser.title)
        #print(parser.title.string)
        #print(parser.get_text())



        ###print(parser.find_all('table'))

        ###for table in parser.find_all('table'):
            ###print(table.find('caption'))

        #print(parser.find_all('tbody'))
        #print(parser.find_all('td'))



        ### Self Explanitory

            #for tr in table.find_all('tr', limit = 1):
        # Not necessarily useful, just shows the order in which the following values are displayed, gone into more detail in next comment
        #for th in tr.find_all('th'):
            #print(th.text)
        #print("*--------------------*--------------------*--------------------*--------------------*--------------------*")
