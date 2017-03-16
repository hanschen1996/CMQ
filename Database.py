import pyodbc
from Queue import *
server = 'cmq.database.windows.net'
database = 'queues'
username = 'yeeadmin'
password = 'Deeznuts123'
#for mac
#driver = '{/usr/local/lib/libtdsodbc.so}'
# run everything: 
# venv\Sripts\activate.bat 
# python main.py start
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# Create queue and add to database
def insertQueue(x):
	cursor.execute("select * from queue")
	z =[x.index,x.name,x.descriptions,x.course,x.location,x.category]
	cursor.execute("INSERT INTO queue(q_id,name,queuedescr,course,location,category) VALUES(?,?, ?, ?, ?, ?)",z)
	cnxn.commit()

# Create new user and add to database
#!!!!#
#!!!!#
def insertQueueUser(x):
	cursor.execute("select * from queueUser")
	z = [(len(cursor.fetchall())+1),x.name,x.andrewID]
	cursor.execute("INSERT INTO queueUser(u_id,name,andrewid) VALUES(?,?,?)",z)
	cnxn.commit()

# Add a given user to a given queue in the database
def toQueue(queue,node):
	z = [queue.index,node.andrewID]
	cursor.execute("UPDATE queueUser SET q_id = ? WHERE andrewid LIKE ?",z)
	cnxn.commit()

# Remove a person from a queue in the database
def deQueue(node):
	z=[node.andrewID]
	cursor.execute("UPDATE queueUser SET q_id = NULL WHERE andrewID LIKE ?",z)
	cnxn.commit()

# Remove a queue from the database and remove all people in the queue from that queue
# !!! #
# !!! #
# !!! #
def dropQueue(queue):
	z = [queue.index]
	cursor.execute("DELETE FROM queue WHERE q_id = ?",z)
	cursor.execute("UPDATE queueUser SET q_id = NULL WHERE q_id = ?",z)	
	cnxn.commit()

# List for OH, Study, Sports, Dining
def getList(category):
	z = [category]
	(cursor.execute("SELECT queue.q_id,queue.name,queue.queuedescr,queue.course,queue.location FROM queue WHERE category LIKE ?",z))
	x = []
	row = cursor.fetchone()
	while row:
		x.append((row[0],row[1],row[2],row[3],row[4]))
		row = cursor.fetchone()
	return x

# List for all users in a certain queue
def getQueueUsers(queue):
	z = [queue.index]
	cursor.execute("SELECT queueUser.name FROM queueUser WHERE queueUser.q_id = ?",z)
	x = []
	row = cursor.fetchone()
	while row:
		x.append(row[0])
		row = cursor.fetchone()
	return x

x = Queue('Name3','asdf', 'asdf',3,'Sports','asdf')
y = Node('Kendrick Tse', 'ktse')
z = Node('Justin Chang', 'jychang1')
# insertQueue(x)
# insertQueueUser(y)
# insertQueueUser(z)
# toQueue(,y)
# toQueue(,z)
# deQueue(y)
# insertQueue(6,x)
# dropQueue(1)
# print(getList('Office Hours'))
# print(getQueueUsers(x))
# cursor.execute("select * from queue")
# row = cursor.fetchone()
# while row:
#     print("\n")
#     for i in range(len(row)):
#     	print(str(row[i])+" ")
#     row = cursor.fetchone()
# cursor.execute("select * from queueUser")
# row = cursor.fetchone()
# while row:
#     print("\n")
#     for i in range(len(row)):
#     	print(str(row[i])+" ")
#     row = cursor.fetchone()
# cursor.execute("BEGIN TRANSACTION")
# SQLCommand = ("INSERT INTO queue (q_id, name, queuedescr, location) VALUES (150,'The Exchange','Capacity at The Exchange','Posner Hall')")
# cursor.execute(SQLCommand)
# cnxncnxn.commit()
# cursor.execute("select * from queue")
# row = cursor.fetchone()
# while row:
#     print("\n")
#     for i in range(len(row)):
#     	print(str(row[i])+" ")
#     row = cursor.fetchone()