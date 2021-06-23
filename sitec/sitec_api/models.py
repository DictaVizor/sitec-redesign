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
        response = self.session.get(self.PANEL_URL)
        html = response.text.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        personal_information_html = soup.find_all('div', class_='student-school-info-escolar')[0]
        personal_information = {}

        student_name = soup.select('.student-name')[0]
        personal_information['control_number'] = student_name.span.string.replace('(', '').replace(')', '')

        if student_name.span:
            student_name.span.decompose()
        if student_name.br:
            student_name.br.decompose()

        personal_information['name'] = student_name.text.strip().title()

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


    def _retrieve_subject_data(self, grouped_table):
        subject_data = {'schedules': [] , 'units': []}
        subject_data['title'] = grouped_table[0].find_all('tr')[0].find_all('td')[1].string
        subject_data['name'] = grouped_table[0].find_all('tr')[1].find_all('td')[1].string
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
        return subject_data

    def retrieve_cycle_advance_data(self):
        html = self.session.get(self.CYCLE_ADVANCE_URL).text

        html = '''
        <body class="page-template-default page page-id-395 custom-background sie" cz-shortcut-listen="true">
   
<header id="site_header" class="site_header">
	 
	<div class="container">
     	<div class="header">
       		<!--
            <div class="search_section">
                                
                <form  class="search-form" id="search-form" method="get" action="https://sitec.tijuana.tecnm.mx" role="search">
                    <input type="text" name="s" placeholder="Buscar" title="Ingresa tu b�squeda"/>
                    <button type="submit">Buscar</button>
                </form>
            </div>
            -->
            <div class="encabezado">
				<div class="logo-tnm">
                	<a href="javascript:void(null);"><img src="/wp-content/themes/fuente/images/LogoTNM.png"></a>
                </div>
                <div class="text-tnm">
                	<a href="javascript:void(null);"> <img src="/wp-content/themes/fuente/images/LogoTecNM_Horizontal.svg"></a>
                </div>
                <div class="logo">
                    <a href="https://sitec.tijuana.tecnm.mx"><img src="https://sitec.tectijuana.edu.mx/wp-content/plugins/website-logo/images/logo_ITT1.png" title="Instituto Tecnológico de Tijuana" alt="Instituto Tecnológico de Tijuana"></a>
                </div><!--logo-->
            </div>            
            <nav class="site_nav">
                <div class="nav_section">
                                <div id="mega-menu-wrap-header_navigation-2" class="mega-menu-wrap"><input type="checkbox" id="mega-menu-toggle-header_navigation-2" class="mega-menu-toggle">
                <label for="mega-menu-toggle-header_navigation-2"></label>
                <ul id="mega-menu-header_navigation-2" class="mega-menu mega-menu-horizontal mega-no-js" data-event="hover" data-effect="slide">
                                        <li class="mega-menu-item mega-menu-item-type-post_type mega-menu-item-object-page mega-align-bottom-left mega-menu-flyout mega-menu-item-313" id="mega-menu-item-313"><a href="https://sitec.tijuana.tecnm.mx/panel/">Mi Panel</a></li>
                                        <li class="mega-menu-item mega-menu-item-type-post_type mega-menu-item-object-page mega-align-bottom-left mega-menu-flyout mega-menu-item-311" id="mega-menu-item-311"><a href="https://sitec.tijuana.tecnm.mx/cambiar-clave/">Cambiar clave</a></li>
                    <li class="mega-menu-item mega-menu-item-type-post_type mega-menu-item-object-page mega-align-bottom-left mega-menu-flyout mega-menu-item-312" id="mega-menu-item-312"><a href="https://sitec.tijuana.tecnm.mx/email/">Cambiar email</a></li>
                    <li class="mega-menu-item mega-menu-item-type-post_type mega-menu-item-object-page mega-align-bottom-left mega-menu-flyout mega-menu-item-314" id="mega-menu-item-314"><a href="https://sitec.tijuana.tecnm.mx/reinscripcion/">Reinscripción</a></li>
                                        <li class="mega-menu-item mega-menu-item-type-post_type mega-menu-item-object-page mega-align-bottom-left mega-menu-flyout mega-menu-item-319" id="mega-menu-item-319"><a href="https://sitec.tijuana.tecnm.mx/avance-ciclo/">Avance Ciclo</a></li>
                                        <li class="mega-menu-item mega-menu-item-type-post_type mega-menu-item-object-page mega-align-bottom-left mega-menu-flyout mega-menu-item-319" id="mega-menu-item-319"><a href="https://sitec.tijuana.tecnm.mx/kardex/">Kardex</a></li>
                    <li class="mega-menu-item mega-menu-item-type-post_type mega-menu-item-object-page mega-align-bottom-left mega-menu-flyout mega-menu-item-312" id="mega-menu-item-312"><a href="https://sitec.tijuana.tecnm.mx/log/">Log</a></li>
                                        <li class="mega-menu-item mega-menu-item-type-custom mega-menu-item-object-custom mega-align-bottom-left mega-menu-flyout mega-menu-item-315" id="mega-menu-item-315"><a href="https://sitec.tijuana.tecnm.mx/wp-content/themes/fuente/base/validacion.php?doLogout=true">Salir Sistema</a></li>
                </ul>
                </div>
                            </div><!--nav_section-->
            </nav><!-- #site-nav --> 
        </div><!--header-->
   </div> <!--wrapper-->
   	   
	<div id="barraAlertas" style="">
		
	</div>
	</header><!-- #site-header -->


        
<div class="con_bg all_con_bg">
	<div class="container">
		<div id="content"> 
             <div class="content_section bg1">
                <div class="col12 generic_page">
                  	
                  	<div class="animateblock top common">
<h1 class="title">Avance del Ciclo</h1>
<h2 class="student-name">DANIEL GONZALEZ SALDA�A <br> <span>(19210498 – FEB-JUL 21)</span></h2>
<p>A continuación se muestran las materias que fueron cargadas y las evaluaciones correspondientes por unidades para el presente ciclo. La columna REP indica si la materia fue cargada por reprobación o curso espacial. U01 indica la calificación para la unidad 1 de la materia y así sucesivamente. Opción es el tipo de evaluación de la unidad NP: No Presentó, ORD: Ordinario/Normal, REG: Regularización y EXT: Extraordinario. Prom Est es el promedio estimado en la materia para el alumno y solo el que se muestra en el Kardex es el definitivo. Si existe alguna duda sobre la presente información verifícalo con el maestro o el coordinador de carrera.</p>
					<table width="100%" border="0">
					  <tbody><tr style="background-color:#900; color:#FFF;">
						<td width="15%"><strong>Materia</strong></td>
						<td width="85%">ACF-0905SC4B – ING. MARIANA HUIZAR TEJADA</td>
					  </tr>
					  <tr>
						<td>&nbsp;</td>
						<td>ECUACIONES DIFERENCIALES</td>
					  </tr>
					  <tr>
						<td>&nbsp;</td>
						<td><table width="100%" border="0">
							<tbody><tr>
							  <td><p align="center">Lunes</p></td>
							  <td><p align="center">Martes</p></td>
							  <td><p align="center">Miercoles</p></td>
							  <td><p align="center">Jueves</p></td>
							  <td><p align="center">Viernes</p></td>
							  <td><p align="center">Sabado</p></td>
							  <td><p align="center">Domingo</p></td>
							</tr>
							<tr>
								<td><p align="center">11001200<br>
							  9302</p></td>
								<td><p align="center">11001200<br>
							  9302</p></td>
								<td><p align="center">11001200<br>
							  9302</p></td>
								<td><p align="center">11001200<br>
							  9302</p></td>
								<td><p align="center">11001200<br>
							  9302</p></td>
								<td><p align="center"><br>
							  </p></td>
								<td><p align="center"><br>
							  </p></td>
							</tr>
						</tbody></table></td>
					  </tr>
					</tbody></table>
										<table border="0" width="100%">
					  <tbody><tr>
						<td><p align="center">Rep</p></td>
					 						<td><p align="center">U01</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U02</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U03</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U04</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U05</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					                                                 <td><p align="center">Prom Est</p></td>
					 </tr>
					                                                     <tr>
                                                        <td><p align="center">—</p></td>                                                        <td><p align="center"><input id="P01" name="LISPA01" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F01" name="LISFA01" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">Ord</p></td>
                                                                                                                <td><p align="center"><input id="P02" name="LISPA02" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F02" name="LISFA02" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">NP</p></td>
                                                                                                                <td><p align="center"><input id="P03" name="LISPA03" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F03" name="LISFA03" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">NP</p></td>
                                                                                                                <td><p align="center"><input id="P04" name="LISPA04" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F04" name="LISFA04" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">NP</p></td>
                                                                                                                <td><p align="center"><input id="P05" name="LISPA05" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F05" name="LISFA05" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">NP</p></td>
                                                                                                                <td><p align="center"><input id="-ACF-0905" name="-ACF-0905" type="text" size="2" value="0" readonly=""></p></td>
                                                    </tr>
                                                										</tbody></table>
					<p>&nbsp;</p>
									<table width="100%" border="0">
					  <tbody><tr style="background-color:#900; color:#FFF;">
						<td width="15%"><strong>Materia</strong></td>
						<td width="85%">SCC-1013SC3C – ING. IGREYNE ARACELY RUIZ ROMERO</td>
					  </tr>
					  <tr>
						<td>&nbsp;</td>
						<td>INVESTIGACION DE OPERACIONES</td>
					  </tr>
					  <tr>
						<td>&nbsp;</td>
						<td><table width="100%" border="0">
							<tbody><tr>
							  <td><p align="center">Lunes</p></td>
							  <td><p align="center">Martes</p></td>
							  <td><p align="center">Miercoles</p></td>
							  <td><p align="center">Jueves</p></td>
							  <td><p align="center">Viernes</p></td>
							  <td><p align="center">Sabado</p></td>
							  <td><p align="center">Domingo</p></td>
							</tr>
							<tr>
								<td><p align="center">13001400<br>
							  0311</p></td>
								<td><p align="center">13001400<br>
							  0311</p></td>
								<td><p align="center">13001400<br>
							  0311</p></td>
								<td><p align="center">13001400<br>
							  0311</p></td>
								<td><p align="center"><br>
							  </p></td>
								<td><p align="center"><br>
							  </p></td>
								<td><p align="center"><br>
							  </p></td>
							</tr>
						</tbody></table></td>
					  </tr>
					</tbody></table>
										<table border="0" width="100%">
					  <tbody><tr>
						<td><p align="center">Rep</p></td>
					 						<td><p align="center">U01</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U02</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U03</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U04</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U05</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					                                                 <td><p align="center">Prom Est</p></td>
					 </tr>
					                                                     <tr>
                                                        <td><p align="center">—</p></td>                                                        <td><p align="center"><input id="P01" name="LISPA01" type="text" size="2" value="78" readonly=""></p></td>
                                                        <td><p align="center"><input id="F01" name="LISFA01" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">Ord</p></td>
                                                                                                                <td><p align="center"><input id="P02" name="LISPA02" type="text" size="2" value="81" readonly=""></p></td>
                                                        <td><p align="center"><input id="F02" name="LISFA02" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">Ord</p></td>
                                                                                                                <td><p align="center"><input id="P03" name="LISPA03" type="text" size="2" value="84" readonly=""></p></td>
                                                        <td><p align="center"><input id="F03" name="LISFA03" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">Ord</p></td>
                                                                                                                <td><p align="center"><input id="P04" name="LISPA04" type="text" size="2" value="83" readonly=""></p></td>
                                                        <td><p align="center"><input id="F04" name="LISFA04" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">Ord</p></td>
                                                                                                                <td><p align="center"><input id="P05" name="LISPA05" type="text" size="2" value="100" readonly=""></p></td>
                                                        <td><p align="center"><input id="F05" name="LISFA05" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">Ord</p></td>
                                                                                                                <td><p align="center"><input id="-SCC-1013" name="-SCC-1013" type="text" size="2" value="85" readonly=""></p></td>
                                                    </tr>
                                                										</tbody></table>
					<p>&nbsp;</p>
									<table width="100%" border="0">
					  <tbody><tr style="background-color:#900; color:#FFF;">
						<td width="15%"><strong>Materia</strong></td>
						<td width="85%">SCC-1017SC4B – ING. TONALLI CUAUHTEMOC GALICIA LOPEZ</td>
					  </tr>
					  <tr>
						<td>&nbsp;</td>
						<td>METODOS NUMERICOS</td>
					  </tr>
					  <tr>
						<td>&nbsp;</td>
						<td><table width="100%" border="0">
							<tbody><tr>
							  <td><p align="center">Lunes</p></td>
							  <td><p align="center">Martes</p></td>
							  <td><p align="center">Miercoles</p></td>
							  <td><p align="center">Jueves</p></td>
							  <td><p align="center">Viernes</p></td>
							  <td><p align="center">Sabado</p></td>
							  <td><p align="center">Domingo</p></td>
							</tr>
							<tr>
								<td><p align="center">10001100<br>
							  9302</p></td>
								<td><p align="center">10001100<br>
							  9302</p></td>
								<td><p align="center">10001100<br>
							  9302</p></td>
								<td><p align="center">10001100<br>
							  9302</p></td>
								<td><p align="center"><br>
							  </p></td>
								<td><p align="center"><br>
							  </p></td>
								<td><p align="center"><br>
							  </p></td>
							</tr>
						</tbody></table></td>
					  </tr>
					</tbody></table>
										<table border="0" width="100%">
					  <tbody><tr>
						<td><p align="center">Rep</p></td>
					 						<td><p align="center">U01</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U02</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U03</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U04</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U05</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U06</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					                                                 <td><p align="center">Prom Est</p></td>
					 </tr>
					                                                     <tr>
                                                        <td><p align="center">—</p></td>                                                        <td><p align="center"><input id="P01" name="LISPA01" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F01" name="LISFA01" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">Ord</p></td>
                                                                                                                <td><p align="center"><input id="P02" name="LISPA02" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F02" name="LISFA02" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">Ord</p></td>
                                                                                                                <td><p align="center"><input id="P03" name="LISPA03" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F03" name="LISFA03" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">NP</p></td>
                                                                                                                <td><p align="center"><input id="P04" name="LISPA04" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F04" name="LISFA04" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">NP</p></td>
                                                                                                                <td><p align="center"><input id="P05" name="LISPA05" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F05" name="LISFA05" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">NP</p></td>
                                                                                                                <td><p align="center"><input id="P06" name="LISPA06" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F06" name="LISFA06" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">NP</p></td>
                                                                                                                <td><p align="center"><input id="-SCC-1017" name="-SCC-1017" type="text" size="2" value="0" readonly=""></p></td>
                                                    </tr>
                                                										</tbody></table>
					<p>&nbsp;</p>
									<table width="100%" border="0">
					  <tbody><tr style="background-color:#900; color:#FFF;">
						<td width="15%"><strong>Materia</strong></td>
						<td width="85%">SCD-1003SC4A – DRA JOHANA MARIA GARCIA ORTEGA</td>
					  </tr>
					  <tr>
						<td>&nbsp;</td>
						<td>ARQUITECTURA DE COMPUTADORAS</td>
					  </tr>
					  <tr>
						<td>&nbsp;</td>
						<td><table width="100%" border="0">
							<tbody><tr>
							  <td><p align="center">Lunes</p></td>
							  <td><p align="center">Martes</p></td>
							  <td><p align="center">Miercoles</p></td>
							  <td><p align="center">Jueves</p></td>
							  <td><p align="center">Viernes</p></td>
							  <td><p align="center">Sabado</p></td>
							  <td><p align="center">Domingo</p></td>
							</tr>
							<tr>
								<td><p align="center">09001000<br>
							  9206</p></td>
								<td><p align="center">09001000<br>
							  9206</p></td>
								<td><p align="center">09001000<br>
							  9206</p></td>
								<td><p align="center">09001000<br>
							  9206</p></td>
								<td><p align="center">09001000<br>
							  9206</p></td>
								<td><p align="center"><br>
							  </p></td>
								<td><p align="center"><br>
							  </p></td>
							</tr>
						</tbody></table></td>
					  </tr>
					</tbody></table>
										<table border="0" width="100%">
					  <tbody><tr>
						<td><p align="center">Rep</p></td>
					 						<td><p align="center">U01</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U02</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U03</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U04</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					                                                 <td><p align="center">Prom Est</p></td>
					 </tr>
					                                                     <tr>
                                                        <td><p align="center">—</p></td>                                                        <td><p align="center"><input id="P01" name="LISPA01" type="text" size="2" value="93" readonly=""></p></td>
                                                        <td><p align="center"><input id="F01" name="LISFA01" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">Ord</p></td>
                                                                                                                <td><p align="center"><input id="P02" name="LISPA02" type="text" size="2" value="95" readonly=""></p></td>
                                                        <td><p align="center"><input id="F02" name="LISFA02" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">Ord</p></td>
                                                                                                                <td><p align="center"><input id="P03" name="LISPA03" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F03" name="LISFA03" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">NP</p></td>
                                                                                                                <td><p align="center"><input id="P04" name="LISPA04" type="text" size="2" value="0" readonly=""></p></td>
                                                        <td><p align="center"><input id="F04" name="LISFA04" type="text" size="2" value="0" readonly=""></p></td>                                                        <td><p align="center">NP</p></td>
                                                                                                                <td><p align="center"><input id="-SCD-1003" name="-SCD-1003" type="text" size="2" value="0" readonly=""></p></td>
                                                    </tr>
                                                										</tbody></table>
					<p>&nbsp;</p>
									<table width="100%" border="0">
					  <tbody><tr style="background-color:#900; color:#FFF;">
						<td width="15%"><strong>Materia</strong></td>
						<td width="85%">SCD-1027SC4A – M.C. MARIA MAGDALENA SERRANO ORTEGA</td>
					  </tr>
					  <tr>
						<td>&nbsp;</td>
						<td>TOPICOS AVANZADOS DE PROGRAMACION</td>
					  </tr>
					  <tr>
						<td>&nbsp;</td>
						<td><table width="100%" border="0">
							<tbody><tr>
							  <td><p align="center">Lunes</p></td>
							  <td><p align="center">Martes</p></td>
							  <td><p align="center">Miercoles</p></td>
							  <td><p align="center">Jueves</p></td>
							  <td><p align="center">Viernes</p></td>
							  <td><p align="center">Sabado</p></td>
							  <td><p align="center">Domingo</p></td>
							</tr>
							<tr>
								<td><p align="center">08000900<br>
							  9206</p></td>
								<td><p align="center">08000900<br>
							  9206</p></td>
								<td><p align="center">08000900<br>
							  9206</p></td>
								<td><p align="center">08000900<br>
							  9206</p></td>
								<td><p align="center">08000900<br>
							  9206</p></td>
								<td><p align="center"><br>
							  </p></td>
								<td><p align="center"><br>
							  </p></td>
							</tr>
						</tbody></table></td>
					  </tr>
					</tbody></table>
										<table border="0" width="100%">
					  <tbody><tr>
						<td><p align="center">Rep</p></td>
					 						<td><p align="center">U01</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U02</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U03</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U04</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					 						<td><p align="center">U05</p></td>
						<td><p align="center">Faltas</p></td>
						<td><p align="center">Opción</p></td>
					                                                 <td><p align="center">Prom Est</p></td>
					 </tr>
					                                                         </tbody></table><table width="100%" border="0">
                                                            <tbody>
                                                                <tr style="background-color:#CCC; color:#FFF;">
                                                                        <td width="15%"></td>
                                                                        <td width="85%">BLOQUEADO POR DESERCIÓN EN:</td>
                                                                </tr>
                                                                
                                                    <tr style="background-color:#CCC; color:#000;">
                                                            <td width="15%" align="center">SCD-1027SC4A</td>
                                                            <td width="85%">TOPICOS AVANZADOS DE PROGRAMACION</td>
                                                    </tr>                                                                <tr>
                                                                        <td>&nbsp;</td>
                                                                        <td>Debes visitar al coordinador para aclarar tu situación.</td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                										
					<p>&nbsp;</p>
				<!-- AQUI ESTA EL ALERT -->
<div id="dialog-message" title="SITEC - Informa" style="display:none !important;">
  <p>
      <span class="ui-icon ui-icon-circle-check" style="float: left; margin: 0 7px 50px 0;"></span>
      <span id="msg"></span>
  </p>              
</div>	
<!-- AQUI TERMINA EL ALERT -->
<script type="text/javascript">
$(document).ready(function() {
	});
</script></div>
				                  </div><!--col12-->
            </div><!--row home_content--> 
		</div> <!--content-->      
	</div><!-- #wrapper -->
</div><!--con_bg-->
<div class="clear"></div>
<div class="container">
<footer id="site-footer">	
        <div class="bottom">
            <div id="text-27" class="widget_text">			<div class="textwidget"><p>Instituto Tecnológico de Tijuana<br>
Calzada Del Tecnológico S/N, Fraccionamiento Tomas Aquino. Tijuana, Baja California. C.P. 22414 Teléfono: +52 (664) 607 8400<br>
Tecnológico Nacional de México – Algunos derechos reservados © 2014-2018<br>
<a href="/politica-de-privacidad/">Política de Privacidad</a></p>
<p>SITEC v5.7</p>
</div>
		</div>			<center>2021-06-23 11:31:16</center>        </div>
    </footer></div><!-- #wrapper -->

<!-- #site-footer -->
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-58411122-1', 'auto');
  ga('send', 'pageview');

</script>

</body>
        '''


        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')
        grouped_tables = list(chunks(tables, 3))
        subjects = []
        for grouped_table in grouped_tables:
            try:
                subject_data = self._retrieve_subject_data(grouped_table)
                subjects.append(subject_data)
            except:
                print(grouped_table)
                pass
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

