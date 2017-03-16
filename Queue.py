class Node(object):
    def __init__(self, name, andrewID):
    	self.name = name
    	self.andrewID = andrewID

    def __hash__(self):
    	return hash(self.name)

    def __eq__(self, other):
    	return isinstance(other, Node) and self.name == other.name

    def __repr__(self):
    	return self.name

class Queue(object):
	def __init__(self, name, descriptions, location, index, category, course = None, coursenum = None):
		self.name = name
		self.descriptions = descriptions
		self.location = location
		self.course = course
		self.coursenum = coursenum
		self.list = []
		self.index = index
		self.category = category

	def enq(self, person, index=None):
		if (index == None):
			self.list.append(person)
		else:
			if (index >= 0 and index <= len(list)):
				self.list.insert(index, person)

	def deq(self, person=None):
		if (person == None):
			self.list = self.list[1:]
		if person in self.list:
			self.list.remove(person)

	def size(self):
		return len(self.list)

	def getQueueList(self):
		return self.list

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, other):
		return isinstance(other, Queue) and self.name == other.name

	def __repr__(self):
		return "Queue(" + self.name + ", " + str(self.list) + ")"