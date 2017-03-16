import pyodbc
from Queue import *
server = 'cmq.database.windows.net'
database = 'queues'
username = 'yeeadmin'
password = 'Deeznuts123'
#for mac
#driver = '{/usr/local/lib/libtdsodbc.so}'
#for linux of windows
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
def insertQueue(index,x):
	cursor.execute("select * from queue")
	z =[index,x.name,x.descriptions,x.course,x.location,x.category]
	cursor.execute("INSERT INTO queue(q_id,name,queuedescr,course,location,category) VALUES(?,?, ?, ?, ?, ?)",z)
	cnxn.commit()

def insertQueueUser(x):
	cursor.execute("select * from queueUser")
	z = [(len(cursor.fetchall())+1),x.name,x.andrewID]
	cursor.execute("INSERT INTO queueUser(u_id,name,andrewid) VALUES(?,?,?)",z)
	cnxn.commit()

def toQueue(index,node):
	z = [index,node.andrewID]
	cursor.execute("UPDATE queueUser SET q_id = ? WHERE andrewid LIKE ?",z)
	cnxn.commit()

def deQueue(node):
	z=[node.andrewID]
	cursor.execute("UPDATE queueUser SET q_id = NULL WHERE andrewID LIKE ?",z)
	cnxn.commit()

def dropQueue(index):
	z = [index]
	cursor.execute("DELETE FROM queue WHERE q_id = ?",z)
	cursor.execute("UPDATE queueUser SET q_id = NULL WHERE q_id = ?",z)	
	cnxn.commit()

# List for OH, Study, Sports, Dining
def getList(category):
	z = [category]
	(cursor.execute("SELECT queue.name FROM queue WHERE category LIKE ?",z))
	x = []
	row = cursor.fetchone()
	while row:
		x.append(row[0])
		row = cursor.fetchone()
	return x

def getQueueUsers(index):
	z = [index]
	cursor.execute("SELECT queueUser.name")

x = Queue('Name3','asdf', 'asdf','Sports','asdf')
y = Node('Kendrick Tse', 'ktse')
z = Node('Justin Chang', 'jychang1')
# insertQueue(3,x)
# insertQueueUser(y)
# insertQueueUser(z)
# toQueue(2,y)
# toQueue(2,z)
# deQueue(y)
# insertQueue(6,x)
# dropQueue(1)
# print(getList('Office Hours'))
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