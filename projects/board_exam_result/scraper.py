import requests as r
from bs4 import BeautifulSoup

index_url = 'http://www.educationboardresults.gov.bd/index.php'
result_url = 'http://www.educationboardresults.gov.bd/result.php'


def scraper(exam_selection, board_selection, year, roll, reg):
	return_string = ""

	res = r.get(index_url)
	soup = BeautifulSoup(res.text, 'lxml')

	# Exam Type
	exam = {}
	exams = soup.find('select', attrs={'id': 'exam'})
	exam_options = exams.findAll('option')
	for i in exam_options:
		exam[i.text] = i['value']
	del exam['HSC/Alim/Equivalent']
	exam_keys = list(exam.keys())

	#board Type
	board={}
	boards = soup.find('select', attrs={'id': 'board'})
	board_options = boards.findAll('option')
	for i in board_options:
		board[i.text] = i['value']
	del board['Select One']
	board_keys = list(board.keys())

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

	res = r.post(result_url, data=data, cookies=cookie)
	soup = BeautifulSoup(res.text, 'lxml')
	table = soup.findAll('table')
	personal_info = table[9].findAll('td')
	subject_info = table[10].findAll('td')


	for i in range(0, len(personal_info), 2):
		return_string += f'''{personal_info[i].text} : {personal_info[i+1].text}\n'''
	return_string += '\n'
	for i in range(3, len(subject_info), 3):
		return_string += f'''{subject_info[i].text} - {subject_info[i+1].text} - {subject_info[i+2].text}\n'''

	return return_string