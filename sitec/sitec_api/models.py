from django.db import models
import requests
from bs4 import BeautifulSoup
from enum import IntEnum
from .utils import chunks

DAYS = {
    1: 'Lunes',
    2: 'Martes',
    3: 'Miercoles',
    4: 'Jueves',
    5: 'Viernes',
    6: 'Sabado',
    7: 'Domingo'
}

class NotConnectedException(Exception):
    def __init__(self, message='Not connected to API.'):
        self.message = message
        super().__init__(self.message)


class SitecApi:

    BASE_URL = 'https://sitec.tijuana.tecnm.mx/'
    PANEL_URL = BASE_URL + 'panel/'
    REINSCRIPTION_URL = BASE_URL + 'reinscripcion/'
    CYCLE_ADVANCE_URL = BASE_URL + 'avance-ciclo/'
    KARDEX_URL = BASE_URL + 'wp-content/themes/fuente/base/ver_kardex.php?aluctr=0' 
    LOG_URL = BASE_URL + 'log/'
    LOGIN_URL = BASE_URL + 'wp-content/themes/fuente/base/validacion.php'
    PROXIES = {
        'http': "http://10.10.1.10:3128",
        'https': "https://10.10.1.11:1080"
    }

    is_connected = False
    HEADERS = { 'User-Agent': 'Mozilla/5.0'}

    def __init__(self, session=None):
        self.session = session
        if not session:
            self.session = requests.Session()
            self.session.proxies.update(self.PROXIES)
            self.session.headers.update(self.HEADERS)
            self.is_connected = True
        
    def login(self, **kwargs):
        response = self.session.post(self.LOGIN_URL, data={
            'numero_control': kwargs.pop('username'),
            'clave': kwargs.pop('password'),
            'g-recaptcha-response': kwargs.pop('captcha')
        })
        if response.status_code == 200:
            self.is_connected = True
        return response

    def retrieve_captcha(self):
        response = self.session.get(self.LOGIN_URL)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            captcha = None
            return captcha
        return None

    def retrieve_panel_data(self):
        if not self.is_connected:
            raise NotConnectedException()
        
        html = self.session.get(self.PANEL_URL).text
        soup = BeautifulSoup(html, 'html.parser')
        personal_information_html = soup.find_all('div', class_='student-school-info-escolar')[0]
        personal_information = {}
        for div in personal_information_html.find_all('div'):
            name = div.get('class')[0]
            title = div.find('strong').text
            value = div.find('span').text
            personal_information[name] = {
                'title': title,
                'value': value
            }
        return personal_information
            

    def retrieve_reinscription_data(self):
        return None

    def retrieve_cycle_advance_data(self):
        html = self.session.get(self.CYCLE_ADVANCE_URL).text
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')
        grouped_tables = list(chunks(tables, 3))
        subjects = []
        for grouped_table in grouped_tables:
            subject_data = {'schedules': [] , 'units': []}
            subject_data['title'] = grouped_table[0].find_all('tr')[0].find_all('td')[1].string

            day_count = 1
            for day_td in grouped_table[1].find_all('tr')[1].find_all('td'):
                day_data = day_td.get_text().split()
                if len(day_data) == 2:
                    day_schedule = list(chunks(day_data[0], 4)) #Start and end time always have 4 chars, so the schedule is splitted by 4 chars.
                    subject_data['schedules'].append({
                        'name': DAYS[day_count],
                        'start': day_schedule[0],
                        'end': day_schedule[1],
                        'classroom': day_data[1],
                    })
                    day_count += 1
            units = grouped_table[2].find_all('tr')[1].find_all('td')[1:]#Skip the first element since its s**t
            units = list(chunks(units, 3))
            unit_count = 0
            for unit in units:
                if(len(unit) <= 1):
                    subject_data['average_score'] = unit[0].find('input').get('value')
                    continue

                unit_data = {}
                unit_data['number'] = unit_count
                unit_data['score'] = unit[0].find('input').get('value')
                unit_data['missed_days'] = unit[1].find('input').get('value')
                unit_data['type'] = unit[2].find('p').text
                unit_count += 1
                subject_data['units'].append(unit_data)

            subjects.append(subject_data)
        return subjects

    def retrieve_kardex_data(self):
        html = self.session.get(self.KARDEX_URL).text
        soup = BeautifulSoup(html, 'html.parser')
        subject_rows = soup.find('table', {'id': 'alumno'}).find_all('tr')
        subjects = []
        for subject_row in subject_rows:
            semester = 1
            for subject_column in subject_row.find_all('td'):
                id = subject_column.get('id')
                #Get rid of all strongs to get the a    ctual data without the "title"
                for strong in subject_column.find_all('strong'):
                    strong.decompose()
                if id is not None:
                    status = subject_column.get('class')[0]
                    subject_data = {}
                    subject_data['semester'] = semester
                    subject_data['status'] = status
                    subject_data['slug'] = subject_column.select('.matcve')[0].string
                    subject_data['name'] = subject_column.select('.matnom')[0].string
                    subject_data['credits'] = subject_column.select('.matcre')[0].string
                    if status == 'aprobada':
                        subject_data['score'] = subject_column.select('.karcal')[0].string
                        subject_data['tc'] = subject_column.select('.tcacve')[0].string
                        subject_data['period'] = subject_column.select('.pdocve')[0].string
                        subject_data['taken_on'] = subject_column.select('.karnpe')[0].string
                    subjects.append(subject_data)
                semester += 1
        return subjects
                    
        

    def retrieve_log_data(self):
        return None

    def retrieve_all_data(self):
        return {
            'panel_data': self.retrieve_panel_data(),
            'reinscription_data': self.retrieve_reinscription_data(),
            'cycle_advance_data': self.retrieve_cycle_advance_data(),
            'kardex_data': self.retrieve_kardex_data(),
            'log_data': self.retrieve_log_data()
        }

