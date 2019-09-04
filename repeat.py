import threading
def do_something():
    threading.Timer(5, do_something).start()
    print('y')