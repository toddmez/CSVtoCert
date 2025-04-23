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
        names = line['Presenters']
        topic = line['Presentation Title']
        values = names, topic
        if len(names) != 0:
            topicAndpresenters.add(values)

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

for names, topic in topicAndpresenters:
    certificate = "dev/Certificate_01.html"
    with open(certificate, 'r', newline='', encoding='utf-8') as f:
        info = f.read()
    namesReplace = re.sub(r'{{participant}}', names, info)
    finalCertificate = re.sub(r'{{topic}}', topic, namesReplace)
    with open('certs/' + clean_file_title(topic) + '.html', 'a', newline='', encoding='utf-8') as f:
        f.write(finalCertificate)
        print(f'created: {clean_file_title(topic)}.html')
        f.close()
#########################
# Process HTML to pdfs
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