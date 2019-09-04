from port_manage import *
from db_manage import *

def deploy_wordpress(data):
    ports = getPort(2)
    port1 = str(ports[0])
    port2 = str(ports[1])
    name = data["name"]
    mis = data["mis"]
    appname = name + "." + mis
    db_name = appname + ".db"
    password = data["pass"]

    import subprocess
    out = subprocess.check_output(["docker-wp", appname, db_name, password, port1, port2])

    print(out)

    retVal = {}
    retVal["appname"] = appname
    retVal["port1"] = port1
    retVal["port2"] = port2

    if "ERROR" in out or "error" in out or "Error" in out:
        print("Error")
        setPort(ports)
        retVal["status"] = "error"
        return retVal

    db_insert_app(mis, name, ports, "started","3", "/cms_app",)
    retVal["status"] = "started"
    return retVal

def deploy_joomla(data):
    print("J")
    ports = getPort(2)
    port1 = str(ports[0])
    port2 = str(ports[1])
    name = data["name"]
    mis = data["mis"]
    appname = name + "." + mis
    db_name = appname + ".db"
    password = data["pass"]
    import subprocess
    out = subprocess.check_output(["docker-joomla", appname, db_name, password, port1, port2])

    print(out)
    retVal = {}
    retVal["appname"] = appname
    retVal["port1"] = port1
    retVal["port2"] = port2

    if "ERROR" in out or "error" in out or "Error" in out:
        print("Error")
        setPort(ports)
        retVal["status"] = "error"
        return retVal

    db_insert_app(mis, name, ports, "started","3", "/cms_app",)
    retVal["status"] = "started"

    return retVal

def deploy_drupal_mysql(data):
    ports = getPort(2)
    port1 = str(ports[0])
    port2 = str(ports[1])
    name = data["name"]
    mis = data["mis"]
    appname = name + "." + mis
    db_name = appname + ".db"
    password = data["pass"]
    import subprocess
    out = subprocess.check_output(["docker-drupal-mysql", appname, db_name, password, port1, port2])

    print(out)

    retVal = {}
    retVal["appname"] = appname
    retVal["port1"] = port1
    retVal["port2"] = port2

    if "ERROR" in out or "error" in out or "Error" in out:
        print("Error")
        setPort(ports)
        retVal["status"] = "error"
        return retVal

    db_insert_app(mis, name, ports, "started","3", "/drupal_app",)
    retVal["status"] = "started"

    return retVal

def deploy_drupal_lite(data):
    ports = getPort(1)
    port1 = str(ports[0])
    name = data["name"]
    mis = data["mis"]
    appname = name + "." + mis
    import subprocess
    out = subprocess.check_output(["docker-drupal-sqlite", appname, port1])

    print(out)

    retVal = {}
    retVal["appname"] = appname
    retVal["port1"] = port1

    if "ERROR" in out or "error" in out or "Error" in out:
        print("Error")
        setPort(ports)
        retVal["status"] = "error"
        return retVal

    db_insert_app(mis, name, ports, "started","3", "/drupal_app",)
    retVal["status"] = "started"

    return retVal


def stop_cms(pid):
    appname = db_get_appname(pid)
    import subprocess
    out = subprocess.check_output(["docker", "stop", appname])
    print(out)
    db_name = appname + ".db"

    check = subprocess.check_output(["docker", "ps"])
    db_out = ""

    if db_name in check:
        db_out = subprocess.check_output(["docker", "stop", db_name])
    print(db_out)

    if "error" in out or "Error" in out or "ERROR" in out or\
        "error" in db_out or "Error" in db_out or "ERROR" in db_out:
        print("Error")
        return False
    db_change_status(pid, "stopped")
    return True

def start_cms(pid):
    appname = db_get_appname(pid)

    db_name = appname + ".db"

    import subprocess
    check = subprocess.check_output(["docker", "ps", "-a"])

    db_out = ""
    if db_name in check:
        db_out = subprocess.check_output(["docker", "start", db_name])
        subprocess.check_output(["sleep", "5"])
    print(db_out)

    out = subprocess.check_output(["docker", "start", appname])
    print(out)

    if "error" in out or "Error" in out or "ERROR" in out or\
        "error" in db_out or "Error" in db_out or "ERROR" in db_out:
        print("Error")
        return False
    db_change_status(pid, "started")
    return True

def delete_cms(pid):
    appname = db_get_appname(pid)
    db_name = appname + ".db"

    import subprocess
    check = subprocess.check_output(["docker", "ps"])

    out = ""
    db_out = ""
    db = 0
    del_db = ''
    if appname in check:
        out = subprocess.check_output(["docker", "stop", appname])

    print(out)

    if db_name in check:
        db_out = subprocess.check_output(["docker", "stop", db_name])
        db = 1

    print(db_out)

    if "error" in out or "Error" in out or "ERROR" in out or\
       "error" in db_out or "Error" in db_out or "ERROR" in db_out:
        print("Error")
        return False

    del_app = subprocess.check_output(["docker", "rm", appname])

    if db == 1:
        del_db = subprocess.check_output(["docker", "rm", db_name])

    if "error" in del_app or "Error" in del_app or "ERROR" in del_app or\
       "error" in del_db or "Error" in del_db or "ERROR" in del_db:
        print("Error")
        return False

    db_delete_app(pid)
    return True
