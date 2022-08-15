#creating Database
import sqlite3

conn = sqlite3.connect('loan_data.db')
c= conn.cursor()

#create table loan_application
c.execute('''
create table loan_application(
'loan_id' int default 1000 primary key autoincrement,
'Name' varchar(10),
'Email' varchar(10),
'Age' int ,
'Gender' varchar(10),
'Married' varchar(5),
'Dependents' int ,
'Education' int ,
'Employment' int  ,
'appincome' real ,
'coappincome' real ,
'loan_term' real ,
'loan_amount' int ,
'Credit_history' int ,
'Area' varchar(10) ,
'loan_status' int ) 
''')

conn.commit()

print('Database created successfully')


