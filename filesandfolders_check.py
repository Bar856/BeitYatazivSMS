import os
ROOT_DIR = os.path.dirname(os.path.abspath("functions.py"))

if not(os.path.isdir('logs')):
    os.mkdir(ROOT_DIR + "/logs")
if not(os.path.isdir('csvs')):
    os.mkdir(ROOT_DIR + "/csvs")
if not os.path.exists(os.path.join(os.getcwd(), 'csvs', 'jobs.csv')):
    f = open("csvs/jobs.csv", "w+")
    f.write("job_id,sender,reciver,job_data,status\n")
    f.close()
if not os.path.exists(os.path.join(os.getcwd(), 'logs', 'log-msgs.txt')):
    f = open("logs/log-msgs.txt", "w+")
    f.close()
if not os.path.exists(os.path.join(os.getcwd(), 'logs', 'log-errors.txt')):
    f = open("logs/log-errors.txt", "w+")
    f.close()
