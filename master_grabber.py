import requests as r
from bs4 import BeautifulSoup

regNo = input("Enter Registration Number Correctly: ")
passwd = input("Enter Password Correctly: ")

login_url = "https://online.udvash-unmesh.com/Account/Login"
data = {"RegistrationNumber": regNo, "Password": passwd}
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

course = input("1.Collect Master Class Links Of Engineering, Type 1 and Enter\n2.Collect Master Class Links Of Medical, Type 2 and Enter\n3.Collect Master Class Links Of Varsity, Type 3 and Enter\n>> ")
if course == '1':
	course_url = "https://online.udvash-unmesh.com/Content/ContentSubject?CourseTypeId=1&masterCourseId=1"
if course == '2':
	course_url = "https://online.udvash-unmesh.com/Content/ContentSubject?CourseTypeId=1&masterCourseId=2"
if course == '3':
	course_url = "https://online.udvash-unmesh.com/Content/ContentSubject?CourseTypeId=1&masterCourseId=3"	

print("Grab a cup of coffee, I am doing the rest...\n\n")


cookie = {}
def login():
    login_res = r.post(login_url,data=data,headers=headers,allow_redirects=False)
    cookie_string = login_res.headers["set-cookie"][10:]
    cookie[".ASPXAUTH"] = cookie_string

login();
course_tags = r.get(course_url, headers=headers, cookies=cookie).text

subjects = {}
course_soup = BeautifulSoup(course_tags, 'html.parser')
for course_link in course_soup.findAll('a', attrs = {'class':'d-between-middle btn-menu p-3'} ):
    subjects[course_link.h3.text] = "https://online.udvash-unmesh.com" + course_link['href']

subject_names = list(subjects.keys()) 
for i in range(len(subject_names)):
    print("## " + subject_names[i])

    subject_res = r.get(subjects[subject_names[i]], headers=headers, cookies=cookie).text
    subject_soup = BeautifulSoup(subject_res, 'html.parser')
    chapters = {}
    for subject_link in subject_soup.findAll('a', attrs = {'class':'d-between-middle btn-menu p-3'} ):
        rep = subject_link['href'].replace("DisplayContentType", "DisplayContentCard")
        chapters[subject_link.h3.text] = "https://online.udvash-unmesh.com" + rep + "&masterContentTypeId=1"
    
    chapter_names = list(chapters.keys())
    for j in range(len(chapter_names)):
        print("    ## " + chapter_names[j])

        chapter_res = r.get(chapters[chapter_names[j]], headers=headers, cookies=cookie).text
        chapter_soup = BeautifulSoup(chapter_res, 'html.parser')

        k = 1
        for chapter_link in chapter_soup.findAll('a', attrs = {'class':'btn btn-video mb-2'} ):
            print("        ## " + "Lecture " + str(k))

            lecture_res = r.get("https://online.udvash-unmesh.com" + chapter_link['href'], headers=headers, cookies=cookie).text
            soup = BeautifulSoup(lecture_res, 'html.parser')
            s = soup.find('li', attrs = {'class':'nav-item active d-none'})
            print("            => " + s['data-all-video-source'])
            print("            => " + "https://www.youtube.com/watch?v=" + s['data-youtube-video'])
            k+=1