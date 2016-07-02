import smtplib, os,datetime,time,csv
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from recharge_panel_templates.config import Pool,operator_code_dict

def send_mail( send_from, send_to, subject, text, files=[], server="localhost", port=587, username='', password='', isTls=True):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject
    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
        msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com')
    if isTls: smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

def get_recharge_reports(start_date,end_date):
    sql_query = "select mobile_number,request_id,circle,operator_code,date_time ::timestamp AT TIME ZONE 'Asia/Kolkata',recharge_status,remark,balance,amount from recharge_reports where " \
                "date_time between '%s' and '%s' "%(start_date,end_date);
    instance = Pool()
    print instance
    cursor = instance.db
    cursor.execute(sql_query)
    records = cursor.fetchall()
    final_data = []
    for list_value in records:
        date_time = str(list_value[4]).split('.')[0]
        # print list_value[5],list_value[6]
        operator = 'NA'
        if list_value[3]:
            operator = operator_code_dict.keys()[operator_code_dict.values().index(list_value[3])]
        final_data.append({"mobile_number": list_value[0], "request_id": list_value[1],
                           "circle": list_value[2], "operator": operator, "date_time": date_time,
                           "recharge_status": list_value[5], "remark": list_value[6],
                           "balance": str(list_value[7]), "amount": list_value[8]})

    if not final_data:
        return None
    base_path = os.path.dirname(os.path.dirname(__file__))

    # base_path = base_path.rsplit('/', 1)[0]
    real_filename = '%s_%s.csv' % ('reports', int(time.time()))
    # real_filename = request.POST.get('file_name',False)
    filename = '/var/www/html/recharge_panel_latest/public/csv_report/%s' % ( real_filename)

    with open(filename, 'wb') as csvfile:
        fieldnames = ('mobile_number', 'request_id', 'circle', 'operator', 'date_time', 'recharge_status', 'remark',
                      'balance', 'amount')
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        headers = dict((n, n) for n in fieldnames)
        print headers
        writer.writerow(headers)
        # writer_handle = csv.writer(csvfile, delimiter=',')
        # writer_handle.writerow(['Mobile Number', 'Date/Time of Misscall', 'Circle', 'Operator', 'OBD Status','Call Start Time', 'Language'
        #                        , 'Gender', 'Age', 'Q1','Q2','Q3','Total Duration','Entry Status'])
        for data in final_data:
            writer.writerow(data)
    return filename

if __name__  == "__main__":

    start_date = datetime.datetime.today().date()
    prevday = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date() + datetime.timedelta(days=-1)
    end_date = "%s 23:59:59"%prevday
    start_date = "%s 00:00:00"%prevday
    filename = get_recharge_reports(start_date,end_date)
    if not filename:
        exit()
    username = "happypocket.recharge@gmail.com"
    password = "happypocket@123"
    email_to = ['patelzeeshan67@gmail.com','krnsyal147@gmail.com']
    files = []
    files.append(filename)
    subject = "Happy Pocket Recharge Report %s"%prevday
    text = "Please find attachment of recharge report for date %s"%prevday
    send_mail("Zeeshan Patel",email_to,subject,text,files,username=username,password=password)