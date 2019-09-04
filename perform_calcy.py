__author__ = 'pshubham'
import port_manage,subprocess,os,commands
from subprocess import PIPE
def perform_calc(data):
    status = {}
    name = data['name']
    if(not data['pr']):
        cmd = 'docker run -d -p '+data['op']+':4300 --name '+name+' '+data['type']
        run  = commands.getoutput(cmd)

        if 'Cannot' in run or 'Error' in run:
            status['status'] = run
            status['succ'] = 1
            return status

    cmd = 'docker cp '+data['dir']+'/'+data['f_name']+' '+name+':/tmp'
    print(subprocess.call(cmd,shell=True))
    #cmd = 'docker exec ' + name + ' kill ps au | grep "shellinaboxd -p" | awk' + "'{print$1}'"
    #print(subprocess.call(cmd,shell=True))
    if(data['type'] == 'calcy_alp_gcc'):
        if(data['pr']):
            subprocess.call('docker stop '+name,shell=True)
            subprocess.call('docker start '+name,shell=True)

        #subprocess.call('docker exec '+name+' gcc /tmp/'+data['fname'],shell=True)
        run =  commands.getoutput('docker exec '+name+' gcc /tmp/'+data['f_name'])
        print(run)
        if 'error:' in run:
            status['status'] = run
            status['succ'] = 0
            return status

        print subprocess.call('docker exec '+name+' sh -c "cd /tmp && shellinaboxd -p 4300 --service='+"'/shell':'shellboxuser':'shellboxuser':'/home/':'/a.out'"+'" &',shell=True)
        status['status'] = 'success'
        status['succ'] = 1
        return status

    if(data['type'] == 'calcy_alp_cplus'):
        if(data['pr']):
            subprocess.call('docker stop '+name,shell=True)
            subprocess.call('docker start '+name,shell=True)


        run = commands.getoutput('docker exec '+name+' g++ /tmp/'+data['f_name'])
        if 'error:' in run:
            status['status'] = run
            status['succ'] = 0
            return status

        print subprocess.call('docker exec '+name+' sh -c "cd /tmp && shellinaboxd -p 4300 --service='+"'/shell':'shellboxuser':'shellboxuser':'/home/':'/a.out'"+'" &',shell=True)
        status['status'] = 'success'
        status['succ'] = 1
        return status

    if(data['type'] == 'calcy_alp_py'):
        if(data['pr']):
            subprocess.call('docker stop '+name,shell=True)
            subprocess.call('docker start '+name,shell=True)

        run = ''
        if(data['pip'] != ''):
            for i in range(0,len(data['pip'])):
                run =+ commands.getoutput('docker exec '+name+' pip install '+data['pip'][i]) + '\n'

        print subprocess.call('docker exec '+name+' sh -c "cd /tmp && shellinaboxd -p 4300 --service='+"'/shell':'shellboxuser':'shellboxuser':'/home/':'python /tmp/"+data['f_name']+" ' "+'" &',shell=True)
        status['status'] = run
        status['succ'] = 1
        return status

    if(data['type'] == 'calcy_alp_java'):

        if(data['pr']):
            subprocess.call('docker stop '+name,shell=True)
            subprocess.call('docker start '+name,shell=True)

        run = commands.getoutput('docker exec '+name+' javac /tmp/'+data['f_name'])
        if 'error:' in run:
            status['status'] = run
            status['succ'] = 0
            return status

        print subprocess.call('docker exec '+name+' sh -c "cd /tmp && shellinaboxd -p 4300 --service='+"'/shell':'shellboxuser':'shellboxuser':'/tmp':'java "+data['class']+" ' "+'" &',shell=True)
        status['status'] = 'success'
        status['succ'] = 1
        return status

'''data = {'mis':'111203062','pr':False,'type':'calcy_alp_java','box':'4200','op':'4100','dir':'/home/pshubham/Desktop/Aspyra_Flask/static/uploads/111203062/calcy','f_name':'HelloWorld.java','class':'HelloWorld', 'name':'shubham'}
print perform_calc(data)'''
