import MySQLdb
import json

'''name = (eg- test)
port = list of ports'''
def db_insert_app(mis, name, port, status,type,endpoint):

    db = MySQLdb.connect("localhost","root","shubham123","aspyra" )

    db_mis = int(mis)

    appname = name + "." + mis
    print(appname)

    num = len(port)

    db_port = ""

    if num == 1:
        db_port = '{"port1":%s}' % str(port[0])
    elif num == 2:
        db_port = '{"port1":%s, "port2":%s}' % (str(port[0]), str(port[1]))
    elif num == 3:
        db_port = '{"port1":%s, "port2":%s, "port3":%s}' % (str(port[0]), str(port[1]), str(port[2]))

    print(db_port)

    cursor = db.cursor()

    sql = "INSERT INTO app(mis, name, appname, port, status,type,endpoint) values ('%d','%s', '%s', '%s', '%s','%s','%s')" % (db_mis, name, appname, db_port, status,type,endpoint)

    try:
        cursor.execute(sql)

        db.commit()
    except:
        db.rollback()

    db.close()


'''here we are using appname because the docker engine will have appname not pid
### to be used only for backend purpose when some issue occurs on docker engine side
 this function will be called to change status### '''
def db_update_status(appname, status):

    db = MySQLdb.connect("localhost","root","shubham123","aspyra" )

    cursor = db.cursor()

    sql = "UPDATE app SET status = '%s' WHERE appname = '%s'" % (status, appname)
    try:
        cursor.execute(sql)

        db.commit()
    except:
        db.rollback()

    db.close()


'''this function to be used when the user himself starts or stops an already deployed container'''
def db_change_status(pid, status):
    db = MySQLdb.connect("localhost","root","shubham123","aspyra" )

    cursor = db.cursor()

    sql = "UPDATE app SET status = '%s' WHERE pid = '%s'" % (status, pid)
    try:
        cursor.execute(sql)

        db.commit()
    except:
        db.rollback()

    db.close()


'''here we use pid bcos the delete button will be pressed on front end by the user and it will pass pid'''
def db_delete_app(pid):
    db = MySQLdb.connect("localhost","root","shubham123","aspyra" )

    db_pid = int(pid)

    cursor = db.cursor()

    sql = "DELETE FROM app WHERE pid = '%s'" % (db_pid)
    try:
       cursor.execute(sql)
       db.commit()
    except:
       db.rollback()

    db.close()


'''this function will return details about apps deployed by particular user with given mis - on home page load
 the returned data structure is of the following format:
{ pid : [name, port (json string), status] }
example -
{ 1 : ["test", {"port1": 40000, "port2": 40001}, "success"],
2 : ["trial", {"port1": 40002, "port2": 40003}, "error"] }
'''
def db_get_using_mis(mis):
    db = MySQLdb.connect("localhost","root","shubham123","aspyra" )

    cursor = db.cursor()

    db_mis = int(mis)

    sql = "SELECT * FROM app where mis = '%d'" % (db_mis)

    retVal = {}
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            temp = []
            temp.append(row[2])
            j_str = json.loads(row[4])
            temp.append(j_str)
            temp.append(row[5])
            print(temp)
            retVal[row[1]] = temp

    except:
        print "Error: unable to fecth data"

    print(retVal)
    db.close()
    return retVal


'''this function useful while deploying app to check if that app name has been used'''
def db_get_names(mis):
    db = MySQLdb.connect("localhost","root","shubham123","aspyra" )

    cursor = db.cursor()

    db_mis = int(mis)

    sql = "SELECT name FROM app where mis = '%d'" % (db_mis)

    retVal = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
          retVal.append(row[0])

    except:
        print "Error: unable to fecth data"

    print(retVal)
    db.close()
    return retVal



'''this function will return details given pid'''
def db_get_details(pid):
    db = MySQLdb.connect("localhost","root","shubham123","aspyra" )

    cursor = db.cursor()

    db_pid = int(pid)

    sql = "SELECT * FROM app where pid = '%d'" % (db_pid)

    retVal = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            retVal.append(row[0])
            retVal.append(row[2])
            retVal.append(row[3])
            j_str = json.loads(row[4])
            retVal.append(j_str)
            retVal.append(row[7])
            print(retVal)
    except:
        print "Error: unable to fecth data"

    db.close()
    return retVal

'''this function will return only the appname given pid'''
def db_get_appname(pid):
    db = MySQLdb.connect("localhost","root","shubham123","aspyra" )

    cursor = db.cursor()

    db_pid = int(pid)

    sql = "SELECT appname FROM app where pid = '%d'" % (db_pid)

    retVal = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            retVal = row[0]
            print(retVal)
    except:
        print "Error: unable to fecth data"

    db.close()
    return retVal

