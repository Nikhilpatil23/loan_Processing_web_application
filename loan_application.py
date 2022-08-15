from flask import Flask , render_template, request
import sqlite3
import logging

#initializing logging

log_file = 'loanapp_log.txt'
logging.basicConfig(filename = log_file,
                    filemode= 'w',
                    format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt= '%m-%d %H:%M',
                    level= logging.DEBUG) #log file created

#initializing Ml model
from joblib import dump, load

#loading saved model
loan_app = load('loan_approval.joblib')

#initialize database
def db_connect() :
    #establish the connection
    db_name = 'loan_data.db'
    db_con = sqlite3.connect(db_name)
    logging.info('connected to '+db_name)
    return db_con

conn = db_connect()

#rest API service
app = Flask(__name__)

@app.route('/', methods = ['POST' , 'GET'])
def home() :
    homepage = '<html><h1>WELCOME TO NV PATIL BANK</h1><body><a href="/application">Click here to submit your loan application form</a></html>'
    return homepage

@app.route('/application', methods = ['POST', 'GET'])
def loan_application():
    loan_data = []
    loan_status = ''
    if request.method == 'POST' :
        try :
            logging.info('Capturing app data ' + request.form['name'])
            loan_data.append(request.form['name'])
            loan_data.append(request.form['email'])
            loan_data.append(request.form['age'])
            loan_data.append(request.form['gender'])
            loan_data.append(request.form['married'])
            loan_data.append(request.form['dependents'])
            loan_data.append(request.form['education'])
            loan_data.append(request.form['employment'])
            loan_data.append(request.form['appincome'])
            loan_data.append(request.form['coappincome'])
            loan_data.append(request.form['loan_amount'])
            loan_data.append(request.form['loan_term'])
            loan_data.append(request.form['credit_history'])
            loan_data.append(request.form['area'])

            logging.info(loan_data)
            refno = write_loan_data(loan_data)
            #ML model prediction
            pred = loan_app.predict([[int(x) for x in loan_data[3:]]])
            if pred == 1 :
                status = 'approved'
            else :
                status = 'rejected'

            loan_status = 'Your loan application with ID [' + str(refno) + '] is ' + status
            logging.info(loan_status)

        except :
            loan_status = 'ERROR'
            logging.exception(loan_status)

    return render_template('application.html', loan_status = loan_status)


# function to write loan data to db
def write_loan_data(loan_data):

    # establsih the connection
    conn = db_connect()

    # create a cursor
    cur = conn.cursor()
    # execute sql command
    sql = 'insert into loan_application(' \
          'name,' \
          'email,' \
          'age, ' \
          'gender, ' \
          'married, ' \
          'dependents, ' \
          'education,' \
          'employment, ' \
          'appincome, ' \
          'coappincome, ' \
          'loan_amount, ' \
          'loan_term, ' \
          'credit_history, ' \
          'area'  \
          ') values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    # verifying the sql statement for debug
    print(sql)
    cur.execute(sql,[x for x in loan_data])
    cur.execute("commit")
    refno = cur.lastrowid
    print(refno)
    cur.close()
    conn.close()
    logging.info("DB commit successful")
    return refno

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)