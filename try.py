'''import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('192.168.2.6', username='guest', password='aspyra',port=2805)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('python /tmp/9ib7YBG13Q9FcntIstgo.py')
print(ssh_stdout.read())'''

'''from subprocess import Popen, PIPE, STDOUT

cmd = 'ls -l'
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
output = p.stdout.read()
print output

cmd = 'ls '
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
output = p.stdout.read()
print output'''
import os
all =  os.listdir('/home/pshubham/Desktop/Aspyra_Flask/static')
print(all)

mypath = '/home/pshubham/Desktop/Aspyra_Flask/static'
from os.path import isfile, join
onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

print(onlyfiles)

dir = list(set(all) - set(onlyfiles))
print(dir)
