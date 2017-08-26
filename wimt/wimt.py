
# wimt - Where is my train?
# Python script to find your train's current location

import configparser
import os
import re
import textwrap
import smtplib
from email.message import EmailMessage

import requests
from lxml import html
from jinja2 import Environment, PackageLoader

BASE_URL = 'https://runningstatus.in/status/{}-today'

# Requests' default user agent might get blocked, so use a more
# appropriate one
USER_AGENT= ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
           '(KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36')
HEADERS = {'User-Agent' : USER_AGENT}

TEMPLATE_FILE='tabl_tmpl.j2'

# wimt configuration file
CONF_FILE = os.path.expanduser('~/.config/wimt.conf')

def get_train_data(train_no, boarding_station):
    response = requests.get(BASE_URL.format(train_no), headers=HEADERS)
    tree = html.fromstring(response.content)
    
    train_data = {}
    
    train_title = tree.xpath('//div[@class="runningstatus-widget-title"]/span/h1/text()')
    train_name = re.match(r'(^.*\))', train_title[0]).group(1)
    train_data['name'] = train_name

    train_current_status = re.match(
            r'^.*\d\.\s*(.*)$',
            tree.xpath('//div[@class="runningstatus-widget-content"]/p')[0].text_content()
        ).group(1)
    train_data['status'] = train_current_status

    train_timings = tree.xpath('//tbody/tr')
    rows = [] 

    for r in train_timings:
        raw_station_val = next(iter(r.xpath('td[1]/text()')), '-')
        station_code = re.match(r'^.*\((\w+)\)', raw_station_val).group(1)
        station_name = re.sub(r'\s*\(.*$', '', next(iter(r.xpath('td[1]/text()')), '-'))

        departure = re.sub(r'^.*\/\s', '', next(iter(r.xpath('td[5]/text()')), '-'))
        delay = r.xpath('td[7]/font')

        if not delay:
            delay = '-'
        else:
            delay = delay[1].text

        rows.append((station_name, departure, delay))

        if station_code == boarding_station:
            break

    train_data['rows'] = rows
    return train_data 

def create_text_timetable(data):
    wrapped_status = '\n '.join(textwrap.wrap(data['status'], width=90))
    train_status = ''.join(('\n','Train : ', data['name'], '\n',
                            '\n ', wrapped_status, '\n'))

    header = '{:30}{:30}{:30}'.format(
        'Station Name',
        'Departure Time',
        'Delay Status')
    divider = '-' * 90

    rows = [train_status, header, divider]
    for station,departure,delay in data['rows']:
        rows.append('{:30}{:30}{:30}'.format(
            station, departure, delay))

    return '\n'.join(rows)

def send_email_report(data, email):
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    username = config['SMTP']['From']
    password = config['SMTP']['Password']
    smtp_host = config['SMTP']['Host']
    smtp_port = config['SMTP']['Port'] or 25
    tls_needed = config['SMTP']['TLS']
    
    msg = EmailMessage()
    msg['Subject'] = 'Check your train timings!'
    msg['From'] = username
    msg['To'] = email 

    env = Environment(
        loader=PackageLoader('wimt', ''),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template(TEMPLATE_FILE)

    text = create_text_timetable(data)
    html = template.render(name=data['name'], status=data['status'], rows=data['rows']) 

    msg.set_content(text)
    msg.add_alternative(html, subtype='html')

    with smtplib.SMTP(host=smtp_host, port=smtp_port) as s:
        if tls_needed:
            s.starttls()
            s.ehlo()
        if password:
            s.login(username, password)
        s.send_message(msg)
