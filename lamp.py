__author__ = 'pshubham'
__author__ = 'mihir'
from port_manage import *
from db_manage import *

def run_db_app(data):
    path = data["path"]
    name = data["name"]
    mis = data["mis"]
    filename = data["filename"]
    dbName = data["dbName"]
    dump = data["dump"]
    sql = data["sql"]
    port = getPort(2)
    port1 = str(port[0])
    port2 = str(port[1])
    print("Path: %s , \nName: %s, \nMIS: %s, \nFilename: %s, \nDatabase Name: %s, \nDatabase Dump: %s, \
          \nPort1: %s, \nPort2: %s, \nSQL Path: %s\n"
          % (path, name, mis, filename, dbName, dump, port1, port2, sql))

    import subprocess
    output = subprocess.check_output(["docker-lamp-db", path, name, mis, filename, dbName, dump, port1, port2, sql])
    subprocess.call('mysql -u admin -paspyra -h 0.0.0.0 -P '+port2+' -e "create database '+dbName+'"',shell=True)
    subprocess.call('mysql -u admin -paspyra -h 0.0.0.0 -P '+port2+' '+dbName+' < '+dump,shell=True)
    outString = output.decode("utf-8")

    retString = {}
    retString["mis"] = mis
    retString["appName"] = name + "." + mis
    retString["Port"] = port1

    if "Error" in outString or "error" in outString or "ERROR" in outString:
        retString["status"] = "error"
        if "SQL" in outString or "sql" in outString:
            retString["Error"] = "Wrong SQL syntax. Check SQL dump file"
        else:
            retString["Error"] = "Error"
        setPort(port)
        return retString

    retString["status"] = "started"
    db_insert_app(mis, name, port, "started","2", "/lamp_app" )

    retString["Error"] = "None"
    return retString

def run_lamp_app(data):
    path = data["path"]
    name = data["name"]
    mis = data["mis"]
    filename = data["filename"]
    port = getPort(1)
    print(port)
    port1 = str(port[0])

    print("Path: %s , \nName: %s, \nMIS: %s, \nFilename: %s, \nPort1: %s\n" % (path, name, mis, filename, port1))

    import subprocess
    output = subprocess.check_output(["docker-lamp-app", path, name, mis, filename, port1])

    outString = output.decode("utf-8")

    retString = {}
    retString["mis"] = mis
    retString["appName"] = name + "." + mis
    retString["Port"] = port1
    print(outString)

    if "Error" in outString or "error" in outString or "ERROR" in outString:
        retString["status"] = "error"
        return retString

    retString["status"] = "started"
    db_insert_app(mis, name, port, "started","2", "/lamp_app" )

    return retString

def run_tomcat_app(data):
    name = data["name"]
    mis = data['mis']
    ports = getPort(1)
    password = data["pass"]
    port1 = str(ports[0])

    import subprocess
    outString = subprocess.check_output(["docker-tomcat-app", name, mis, port1, password])

    retString = {}
    retString["mis"] = mis
    retString["appName"] = name + "." + mis
    retString["Port"] = port1
    print(outString)

    if "Error" in outString or "error" in outString or "ERROR" in outString:
       retString["status"] = "error"
       setPort(ports)
       return retString

    retString["status"] = "started"
    db_insert_app(mis, name, ports, "started","2", "/tomcat_app" )

    return retString

def stop_deploy(pid):
    appname = db_get_appname(pid)
    import subprocess
    out = subprocess.check_output(["docker", "stop", appname])
    print(out)

    if "error" in out or "Error" in out or "ERROR" in out:
        print("Error")
        return False
    db_change_status(pid, "stopped")
    return True

def start_deploy(pid):
    appname = db_get_appname(pid)

    from subprocess import check_output
    out = check_output(["docker", "start", appname])
    print(out)

    if "error" in out or "Error" in out or "ERROR" in out:
        print("Error")
        return False
    db_change_status(pid, "started")
    return True

def delete_deploy_app(pid):
    ret = db_get_details(pid)

    appname = ret[2]

    image_name = ret[1] +"/" + str(ret[0])

    import subprocess
    check = subprocess.check_output(["docker", "ps"])

    out = ""
    db = 0
    del_db = ''
    if appname in check:
        out = subprocess.check_output(["docker", "stop", appname])

    print(out)

    if "error" in out or "Error" in out or "ERROR" in out:
        print("Error")
        return False

    del_app = subprocess.check_output(["docker", "rm", appname])

    if "error" in del_app or "Error" in del_app or "ERROR" in del_app:
        print("Error")
        return False
    del_img = ""
    if "/tomcat_app" != ret[4]:
        del_img = subprocess.check_output(["docker", "rmi", image_name])

    if "error" in del_img or "Error" in del_img or "ERROR" in del_img:
        print("Error")
        return False

    db_delete_app(pid)
    return True

