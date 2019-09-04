__author__ = 'pshubham'
import subprocess
def delete_calc(name):
    subprocess.Popen('docker rm -f '+name,shell=True)