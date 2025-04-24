import csv
import re
import os
import shutil
import subprocess

#########################
# Remove special characters replace with file safe annotation, ex. -dash-
# "Win, Lose, or Navigate" becomes: Win-comma-_Lose-comma-_or_Navigate.html
#########################

def clean_file_title(title):
    escapes = {"-":"-dash-",
                ".":"-dot-",
                "/":"-slash-",
                ":":"-colon-",
                "#":"-hash-",
                ",":"-comma-",
                "'":"-appos-",
                '"':"-quote-",
                '?':"-question-",
                '=':"-equal-",
                '+':"-plus-",
                ' ':"_",
		'(':"-paren-",
		')':"-paren-",
		'&':"-amper-"
              }
    try:
        for char, uni in escapes.items():
            title = title.replace(char, uni).lower() 
        return title
    except UnicodeError as f:
        print('{f} there was a error continuing')

topicAndpresenters = set()

#########################
# Loop through csv file adding to topicAndpresenters set, skip blanks
#########################

with open('names_and_presentations.csv', newline='') as csvfile:
    FeedbackDictReader = csv.DictReader(csvfile, delimiter=',')
    for line in FeedbackDictReader:
        ids = line['ID']
        names = line['Presenters']
        topic = line['Presentation Title']
        dates = line['Date']
        topicAndpresenters[ids]=f'{names}@{topic}'

#########################
# List directory, check for "certs" folder remove / create if needed
#########################
dirList = os.listdir()
if "certs" in dirList:
    shutil.rmtree("certs")
    os.mkdir("certs")
elif "certs" not in dirList:
    os.mkdir("certs")

#########################
# Read set, read certificate (template), open template, replace name placeholder, replace topic placeholder. create new html file in certs folder.
#########################

for ids, topic in topicAndpresenters.items():
	values = topic.split('@')
	presenterNames = values[0]
	topicName = values[1]
	certificate = "dev/Certificate_01.html"
    with open(certificate, 'r', newline='', encoding='utf-8') as f:
        info = f.read()
        namesReplace = re.sub(r'{{participant}}', names, info)
        dateReplace = re.sub(r'{{date}}', dates, namesReplace)
        finalCertificate = re.sub(r'{{topic}}', topic, dateReplace)
    with open('certs/' + presenterNames + '_' + clean_file_title(topicName) + '.html', 'a', newline='', encoding='utf-8') as f:
        f.write(finalCertificate)
        print(f'created: {presenterNames}_{clean_file_title(topicName)}.html')
        f.close()
#########################
# Process HTML to pdfs. Comment section out if PDFs are not needed.
#########################

local = os.path.abspath('.')
print(local)
folderList = os.listdir('certs')
for file in folderList:
    print(file)
    path = os.path.join('certs', file)  
    print(path, end='\n\n')
    pdfFile = path.replace('.html', '.pdf')
    subprocess.run(['wkhtmltopdf', 
                    '--enable-local-file-access',
                    '--page-size', 'Letter',
                    '--print-media-type',
                    path, pdfFile])
