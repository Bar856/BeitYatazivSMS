from flask import Flask, request
from functions import *
import filesandfolders_check

app = Flask(__name__)


# Listening to new msgs (In & Out)
@app.route("/sms", methods=['GET', 'POST'])
def sms():
    msg = request.args.get('msg')
    to = request.args.get('to')
    sender = request.args.get('from')
    if sender != beityaziv_number:
        update_status(csv_file_path, getJobNum(msg), getStatus(msg),sender)
        send_log("התקבלה הודעה מ-{0} תוכן ההודעה:{1}".format(get_cantact_name(sender), msg), "msgs")
    else:
        newJobId = add_row(sender, get_cantact_name(to), msg, '0')
        send_sms(to, "מספר עבודה:{0}\nאנא השב עם מספר עבודה, רווח בטיפול/טופל/בלתי אפשרי לטיפול/(דוגמא 2 טופל)".format(newJobId), False)
    return "got the msg"


# Run the flask App
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
