from flask import Flask, render_template, request, redirect, url_for
from Queue import *
from Database import *
import http.client
#import pyodbc 

app = Flask(__name__)
app.debug = True

# server = "cmq.database.windows.net"
# database = "queues"
# username = "yeeadmin"
# password = "Deeznuts123"
# # driver = '{/usr/local/lib/libtdsodbc.so}'
# # cnxn = pyodbc.connect('DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' 
# # 	+ database + ';UID=' + username + ';PWD:' + password)

users = getQueueUsers
curUser = None
ohqNames = getList("Office Hours")
studyqNames = getList("Study")
sportsqNames = getList("Sports")
diningqNames = getList("Dining")
ohq, studyq, sportsq, diningq = [], [], [], []
createdQueue = None
queueCount = None

for (index, name, description, course, location) in ohqNames:
	newqueue = Queue(name, description, location, index, "Office Hours", course)
	newqueue.list = getQueueUsers(newqueue)
	ohq.append(newqueue)

	if (queueCount == None or index > queueCount):
		queueCount = index

for (index, name, description, course, location) in studyqNames:
	newqueue = Queue(name, description, location, index, "Study", course)
	newqueue.list = getQueueUsers(newqueue)
	studyq.append(newqueue)
	if (queueCount == None or index > queueCount):
		queueCount = index

for (index, name, description, course, location) in sportsqNames:
	newqueue = Queue(name, description, location, index, "Sports", course)
	newqueue.list = getQueueUsers(newqueue)
	sportsq.append(newqueue)
	if (queueCount == None or index > queueCount):
		queueCount = index

for (index, name, description, course, location) in diningqNames:
	newqueue = Queue(name, description, location, index, "Dining", course)
	newqueue.list = getQueueUsers(newqueue)
	diningq.append(newqueue)
	if (queueCount == None or index > queueCount):
		queueCount = index

if (queueCount == None): queueCount = 0
else: queueCount += 1

@app.route("/")
def home():
	curUser = None
	return render_template("login.html")
@app.route("/gotocreate")
def gotocreate():
	return render_template("create.html", user = curUser.andrewID)
@app.route("/index")
def index():
	return render_template("index.html", user = curUser.andrewID)

@app.route("/gotojoin")
def gotojoin():
	return render_template("join.html", user = curUser.andrewID)

#create q page directs to manager page
@app.route("/create", methods = ["POST"])
def create():
	global queueCount
	global createdQueue
	qtype = request.form["check"]
	name = request.form["qname"]
	description = request.form["coursedesc"]
	location = request.form["location"]
	course = request.form["coursename"]
	coursenum = request.form["coursenum"]
	if (qtype == "1"): 
		newqueue = Queue(name, description, location, queueCount, "Office Hours", course, coursenum)
		ohq.append(newqueue)
	if (qtype == "2"): 
		newqueue = Queue(name, description, location, queueCount, "Study")
		studyq.append(newqueue)
	if (qtype == "3"): 
		newqueue = Queue(name, description, location, queueCount, "Sports")
		sportsq.append(newqueue)
	if (qtype == "4"): 
		newqueue = Queue(name, description, location, queueCount, "Dining")
		diningq.append(newqueue)
	queueCount += 1
	insertQueue(newqueue)
	createdQueue = newqueue
	return render_template("manageq.html", newqueue = newqueue.getQueueList(),
		                                   name = createdQueue.name,
		                                   size = str(createdQueue.size()),
		                                   description = createdQueue.descriptions,
		                                   user = curUser.andrewID)	

# 4 category redirectors
@app.route("/officehours")
def officehours():
	ohtemp = []
	size = []
	count = []
	location = []
	qsize = len(ohq)
	for i in range(qsize):
		ohtemp.append(ohq[i].name)
		size.append(str(ohq[i].size()))
		location.append(ohq[i].location)
		count.append(str(i))
	return render_template("listqOH.html", options = ohtemp, size= size, count=count, location=location,
		                                   user = curUser.andrewID) 

@app.route("/studyareas")
def studyareas():
	studyareas = []
	size = []
	count = []
	location = []
	qsize = len(studyq)
	for i in range(qsize):
		studyareas.append(studyq[i].name)
		size.append(str(studyq[i].size()))
		location.append(studyq[i].location)
		count.append(str(i))
	return render_template("listqStudy.html",options = studyareas, size=size, count=count, location=location,
		                                     user = curUser.andrewID)

@app.route("/sports")
def sports():
	places = []
	size = []
	count =[]
	location = []
	qsize = len(sportsq)
	for i in range(qsize):
		places.append(sportsq[i].name)
		size.append(str(sportsq[i].size()))
		location.append(sportsq[i].location)
		count.append(str(i))
	return render_template("listqSports.html",options=places,size=size, count=count, location=location,
		                                      user = curUser.andrewID)

@app.route("/dining")
def dining():
	spots = []
	size = []
	location = []
	qsize = len(diningq)
	count = []

	for i in range(qsize):
		spots.append(diningq[i].name)
		size.append(str(diningq[i].size()))
		location.append(diningq[i].location)
		count.append(str(i))
	return render_template("listqDining.html", options=spots, size=size, count=count, location=location,
		                                       user = curUser.andrewID)


#join the queue
@app.route("/queuejoinOH", methods = ["POST"])
def queuejoinOH():
	result = request.form["index"]
	index = ohq.index(Queue(result[5:], "queue", "gates", 0, "Office Hours"))
	ohq[index].enq(curUser)
	toQueue(ohq[index], curUser)

	return render_template("inq.html", qlist = ohq[index].getQueueList(), name = ohq[index].name, 
		                               descriptions=ohq[index].descriptions,
	                                   index=ohq[index].getQueueList().index(curUser)+1,
	                                   size=ohq[index].size(),
	                                   user=curUser.andrewID)

@app.route("/queuejoinSports", methods = ["POST"])
def queuejoinSports():
	result = request.form["index"]
	index = sportsq.index(Queue(result[5:], "queue", "gates", 0, "Office Hours"))
	sportsq[index].enq(curUser)
	toQueue(sportsq[index], curUser)

	return render_template("inq.html", qlist = sportsq[index].getQueueList(), name=sportsq[index].name, 
		                               descriptions=sportsq[index].descriptions,
		                               index=sportsq[index].getQueueList().index(curUser)+1,
		                               size=sportsq[index].size(),
		                               user = curUser.andrewID)

@app.route("/queuejoinDining", methods = ["POST"])
def queuejoinDining():
	result = request.form["index"]
	index = diningq.index(Queue(result[5:], "queue", "gates", 0, "Office Hours"))
	diningq[index].enq(curUser)
	toQueue(diningq[index], curUser)

	return render_template("inq.html", qlist = diningq[index].getQueueList(), name=diningq[index].name, 
		                               descriptions=diningq[index].descriptions,
		                               index=diningq[index].getQueueList().index(curUser)+1,
	                                   size=diningq[index].size(),
	                                   user = curUser.andrewID)

@app.route("/queuejoinStudy", methods = ["POST"])
def queuejoinStudy():
	result = request.form["index"]
	index = studyq.index(Queue(result[5:], "queue", "gates", 0, "Office Hours"))
	studyq[index].enq(curUser)
	toQueue(studyq[index], curUser)

	return render_template("inq.html", qlist = studyq[index].getQueueList(), name=studyq[index].name, 
		                               descriptions=studyq[index].descriptions,
	                                   index=studyq[index].getQueueList().index(curUser)+1,
	                                   size=studyq[index].size(),
	                                   user = curUser.andrewID)

@app.route("/managerdeq", methods = ["POST"])
def managerdeq():
	print ("dequing")
	name = request.form["deqlistname"]
	check = Queue(name, "queue", "gates", 0, "Office Hours")
	if check in ohq:
		index = ohq.index(check)
		ohq[index].deq()
		deQueue(curUser)
		return render_template("manageq.html", newqueue = ohq[index].getQueueList(),queuename = name,
			                                   user = curUser.andrewID)
	if check in studyq:
		index = studyq.index(check)
		studyq[index].deq()
		deQueue(curUser)
		return render_template("manageq.html", newqueue = studyq[index].getQueueList(),queuename = name, user=curUser.andrewID)
	if check in sportsq:
		index = sportsq.index(check)
		sportsq[index].deq()
		deQueue(curUser)
		return render_template("manageq.html", newqueue =sportsq[index].getQueueList(),queuename = name, user=curUser.andrewID)
	if check in diningq:
		index = diningq.index(check)
		diningq[index].deq()
		deQueue(curUser)
		return render_template("manageq.html", newqueue = diningq[index].getQueueList(),queuename = name, user = curUser.andrewID)

def validate(andrewId):
    conn = http.client.HTTPConnection("apis.scottylabs.org")
    link = "/directory/v1/andrewID/" + andrewId
    conn.request("HEAD", link)
    res = conn.getresponse()
    if res.reason == "OK": return True
    elif res.reason == "Not Found": return False

@app.route("/login", methods=["POST"])
def login():
	global curUser
	andrewid = request.form["andrewid"]
	if not validate(andrewid): 
		return render_template("login.html")
	else:
		curUser = Node(andrewid, andrewid)
		return render_template("index.html", user = curUser.andrewID)

@app.route("/viewq")
def viewq():
	if (createdQueue == None): return render_template("index.html", user = curUser.andrewID)
	return render_template("manageq.html",newqueue = createdQueue.getQueueList(),
		                                  name = createdQueue.name,
		                                  size = str(createdQueue.size()),
		                                  description = createdQueue.descriptions, user = curUser.andrewID)

@app.route("/logout")
def logout():
	return render_template("login.html")

if __name__ == "__main__":
  app.run()


