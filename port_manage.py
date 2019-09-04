#check for already used host OS ports especially the ones already in use by the VM
#Though the ports allocated by this code will always be unique there are some ports
#which are pre-allocated for SSH in virtualbox NAT port forwarding rules

import MySQLdb

#To get available ports from DB
#input : number of ports req
#output: list of ports 
#check output list if it empty or not 
def getPort( num ):
	db = MySQLdb.connect("localhost","root","shubham123","aspyra" )
	cursor = db.cursor()
	portList = []
	query = "select port from PORTS LIMIT %d" % num
	try:
   		# Execute the SQL command
   		cursor.execute(query)
   		# Fetch all the rows in a list of lists.
   		results = cursor.fetchall()
		for row in results:
      			port = row[0]
      			portList.append(port)
	except:
   		print "Error: unable to fecth data"

	query = "delete from PORTS LIMIT %d" % num
	try:
		# Execute the SQL command
   		cursor.execute(query)
   		# Commit your changes in the database
   		db.commit()
	except:
		# Rollback in case there is any error
   		db.rollback()

	db.close()	
	return portList


#To put back ports into DB
#input: list of ports to be inserted back
#output: Boolean value - True / False depending on whether the query execution was
#sucessful or not
def setPort( portList ):
	db = MySQLdb.connect("localhost","root","shubham123","aspyra" )
	cursor = db.cursor()
	length = len(portList)
	for num in range(0, length):
		try:
	   		# Execute the SQL command
	   		cursor.execute("INSERT INTO PORTS (port) VALUES(%d)" % (portList[num]))
	   		# Commit your changes in the database
	   		db.commit()
		except:
	   		# Rollback in case there is any error
			db.rollback()
			return False
	db.close()
	return True
	

