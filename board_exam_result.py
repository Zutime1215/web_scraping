import requests as r
from bs4 import BeautifulSoup

index_url = 'http://www.educationboardresults.gov.bd/index.php'
res = r.get(index_url)
soup = BeautifulSoup(res.text, 'lxml')

# Exam Type Selection
exam = {}
exams = soup.find('select', attrs={'id': 'exam'})
exam_options = exams.findAll('option')
for i in exam_options:
	exam[i.text] = i['value']
del exam['HSC/Alim/Equivalent']

exam_keys = list(exam.keys())
print('Select Exam:')
for i in range(len(exam_keys)):
	print(f'  Type {i+1} for {exam_keys[i]}')
exam_selection = int(input(">> "))

# Board Type Selection
board={}
boards = soup.find('select', attrs={'id': 'board'})
board_options = boards.findAll('option')
for i in board_options:
	board[i.text] = i['value']
del board['Select One']

board_keys = list(board.keys())
print('Select Board:')
for i in range(len(board_keys)):
	print(f'  Type {i+1} for {board_keys[i]}')
board_selection = int(input(">> "))

# User Input Year, Roll, Registration
year = input("Enter Exam Year: ")
roll = input("Enter Roll Number: ")
reg = input("Enter Registration number: ")

print('\n')


table = soup.find('table', attrs={'class':"black12bold"})
tr = table.findAll('tr')[-3]
td = tr.findAll('td')[1].text.split()
value_s = int(td[0]) + int(td[-1])

cookie = {'PHPSESSID':res.headers['Set-Cookie'][10:36]}
data = {
	'et': 3,
	'sr': 3,
	'exam': exam[exam_keys[exam_selection-1]],
	'year': year,
	'board': board[board_keys[board_selection-1]],
	'roll': roll,
	'reg': reg,
	'value_s': value_s,
	'button2': 'Submit'
}

result_url = 'http://www.educationboardresults.gov.bd/result.php'
res = r.post(result_url, data=data, cookies=cookie)
soup = BeautifulSoup(res.text, 'lxml')
table = soup.findAll('table')
personal_info = table[9].findAll('td')
subject_info = table[10].findAll('td')


for i in range(0, len(personal_info), 2):
	print(f'''{personal_info[i].text} : {personal_info[i+1].text}''')
print()
for i in range(3, len(subject_info), 3):
	print(f'''{subject_info[i].text} - {subject_info[i+1].text} - {subject_info[i+2].text}''')