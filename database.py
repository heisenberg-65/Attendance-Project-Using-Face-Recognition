import mysql.connector
from datetime import date

class Database:
	def __init__(self):
		self.mydb = mysql.connector.connect(host='localhost', user='root', passwd='root', database='attendance')
		self.mycur = self.mydb.cursor()
		command = "CREATE TABLE IF NOT EXISTS ROLLNO (Scholar INT(10), Name VARCHAR(50))"
		self.mycur.execute(command)
		command = "CREATE TABLE IF NOT EXISTS ATTENDANCE (Scholar INT(10), date DATE, time TIME, Attend VARCHAR(2))"
		self.mycur.execute(command)
		self.mydb.commit()

	def get_data(self):
		command = 'SELECT * FROM ROLLNO'
		self.mycur.execute(command)
		data = self.mycur.fetchall()
		return data

	def get_returnable_data(self):
		data = self.get_data()
		new_data = []
		today_date = date.today().strftime("%Y-%m-%d")
		for x in data:
			new_data.append([x[0], x[1], today_date, '00:00:00', 'A'])
		return new_data

	def upload(self, data):
		new_data = []
		for x in data:
			new_data.append((str(x[0]), str(x[2]), str(x[3]), str(x[4])))
		command = "INSERT INTO attendance (Scholar, date, time, Attend) VALUES (%s, %s, %s, %s)"
		self.mycur.executemany(command, new_data)
		self.mydb.commit()

	def get_record(self, start_date="1900-01-01", end_date="2500-12-31",flag=0,sch=0):
		detail = self.get_data()
		for x in detail:
			command = "select * from attendance where Scholar = %s && date >= %s && date <= %s"
			self.mycur.execute(command, (x[0],start_date,end_date ))
			z = self.mycur.fetchall()
			total = len(z)
			command = "select * from attendance where Scholar = %s && Attend = 'P' && date >= %s && date <= %s"
			self.mycur.execute(command, (x[0],start_date,end_date ))
			y = self.mycur.fetchall()
			pp = len(y)
			if flag == 1 :
				print('Scholar ID : ' + str(x[0]))
				print('Name : ' + str(x[1]))
				print('Attendance Percentage = '+str((pp / total)*100)+'%')
			elif int(x[0])==sch :
					print('Scholar ID : ' + str(x[0]))
					print('Name : ' + str(x[1]))
					print('Attendance Percentage = ' + str((pp / total) * 100) + '%')

	def insert_stu(self,name="a"):
		command = "select * FROM ROLLNO "
		self.mycur.execute(command)
		var = self.mycur.fetchall()
		tot=int(len(var))
		self.mydb.commit()
		command = "INSERT INTO ROLLNO (Scholar, Name) VALUES (%s, %s)"
		self.mycur.execute(command, (tot+1,name))
		self.mydb.commit()
