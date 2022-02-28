import requests
from datetime import datetime
import csv
import pandas as pd
import os
import filesandfolders_check

ROOT_DIR = os.path.dirname(os.path.abspath("functions.py"))
print(ROOT_DIR)
csv_file_path = ROOT_DIR + "/csvs/jobs.csv"
log_folder_path = ROOT_DIR + "/logs"


# Contacts DB
class Contact:
    def __init__(self, name, phone_number, role):
        self.name = name
        self.phone_number = phone_number
        self.role = role

    def __str__(self):
        return self.name

    def get_num(self):
        return self.phone_number


# INFO
beityaziv_number = '0588888888'
departments = ['אחזקה', 'קבלה', 'מחשוב', 'משרד החינוך', 'משק']
contacts = [Contact('a', '050', 'אחזקה'),
            Contact('v', '050', 'אחזקה'),
            Contact('c', '050', 'אחזקה'),
            Contact('d', '050', 'אחזקה'),
            Contact('e', '050', 'אחזקה'),
            Contact('f', '050', 'קבלה'),
            Contact('g', '050', 'קבלה'),
            Contact('e', '050', 'קבלה'),
            Contact('g', '050', 'מחשוב'),
            Contact('d', '050', 'מחשוב'),
            Contact('g', '050', 'מחשוב'),
            Contact('sa', '050', 'משרד החינוך'),
            Contact('a', '050', 'משרד החינוך'),
            Contact('t', '050', 'משק'),
            Contact('u', '050', 'משק'),
            Contact('p', '050', 'משק'),
            Contact('z', '050', 'משק')]

global last_log_error
last_log_error = ''
headers = ['job_id', 'sender', 'reciver', 'job_data', 'status']


def toString(list2):
    return ''.join(list2)


def removeSpaces(string):
    res = []
    for i in range(0, len(string) - 1):
        if string[i] == ' ':
            if string[i - 1].isalpha() and string[i + 1].isalpha() and 1 < i < len(string) - 1:
                res.append(string[i])
        elif string[i].isdigit():
            pass
        else:
            res.append(string[i])
    return toString(res)


# Sending to log file - for ERRORS and MSGS log
def send_log(txt, log_name):
    global last_log_error
    if txt != last_log_error:
        with open(log_folder_path + '/log-{0}.txt'.format(log_name), 'a') as fs:
            fs.write(datetime.now().strftime("%d/%m/%Y %H:%M:\n") + txt + "\n")
        last_log_error = txt


# Sending sms - 2 get requests, handling exceptions
def send_sms(to, msg, withRequewst):
    try:
        r = requests.get(
            "https://sms.deals/api/ws.php?service=send_sms"
            "&username="
            "&password="
            "&message={0}&dest={1}"
            "&sender=".format(msg, to))
        if r.ok and withRequewst:
            send_log("הודעה נשלחה אל-{0} תוכן: {1}".format(get_cantact_name(to), msg), "msgs")
            pload = {'msg': msg, 'from': beityaziv_number, 'to': to}
            requests.get('https://hook.integromat.com/xxx', data=pload)
            return True
        elif r.ok and withRequewst is False:
            send_log("הודעה נשלחה אל-{0} תוכן: {1}".format(get_cantact_name(to), msg), "msgs")
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return "ex1"
    except Exception as e:
        send_log(str(e), "errors")


# add row with job id generate automatically and fields given
def add_row(*args):
    try:
        new_args = []
        results = pd.read_csv(csv_file_path)
        job_id = len(results) + 1
        new_args.append(job_id)
        for i in args:
            new_args.append(i)
        with open(csv_file_path, 'a', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(new_args)
        return job_id
    except Exception as e:
        send_log("error - open_csv() - {0}" + str(e), "errors")


# update status of a job
def update_status(file, job_id, status, reciever2):
    op = open(file, "r")
    dt = csv.DictReader(op)
    up_dt = []
    for r in dt:
        if r['job_id'] == str(job_id) and r['reciver'] == get_cantact_name(reciever2):
            row = {'job_id': r['job_id'],
                   'sender': r['sender'],
                   'reciver': r['reciver'],
                   'job_data': r['job_data'],
                   'status': status
                   }
        else:
            row = {'job_id': r['job_id'],
                   'sender': r['sender'],
                   'reciver': r['reciver'],
                   'job_data': r['job_data'],
                   'status': r['status']
                   }
        up_dt.append(row)
    op.close()
    op = open(file, "w", newline='')
    data = csv.DictWriter(op, delimiter=',', fieldnames=headers)
    data.writerow(dict((heads, heads) for heads in headers))
    data.writerows(up_dt)
    op.close()


# Return a List contacts by depart
def get_contacts_by_depart(depart):
    res = []
    for i in contacts:
        if i.role == depart:
            res.append(i.name)
    return res


# Return Contact name - (return the number if number not shown on contacts)
def get_cantact_name(num):
    for i in contacts:
        if i.phone_number == num:
            return i.name
    return num


def get_contact_num(name):
    for i in contacts:
        if i.name == name:
            return i.phone_number


def getJobNum(tx):
    return tx[0:tx.index(" ")]


def getStatus(tx):
    return tx[tx.index(" ") + 1: len(tx)]


statusDefs = [{1: "בטיפול"}, {2: "טופל"}, {3: "בלתי אפשרי לטיפול"}]
