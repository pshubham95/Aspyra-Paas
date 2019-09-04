__author__ = 'pshubham'
import commands,subprocess
def single_container_create(data,mapp):
    if len(data['port']) == 2:
        cmd = 'docker run -d -p '+data['port'][0]+':4200 -p '+data['port'][1]+':22 --name '+data['name']+'.'+data['mis']+' -v '+data['dir']+':/tmp '+mapp[data['choice']]


    if len(data['port']) == 3:
        if mapp[data['choice']] == 'lamp_shell':
            cmd = 'docker run -d -p '+data['port'][0]+':4200 -p '+data['port'][1]+':80 -p '+data['port'][2]+':22 --name '+data['name']+'.'+data['mis']+' -v '+data['dir']+':/home '+mapp[data['choice']]
        else:
            cmd = 'docker run -d -p '+data['port'][0]+':4200 -p '+data['port'][1]+':8080 -p '+data['port'][2]+':22 --name '+data['name']+'.'+data['mis']+' -v '+data['dir']+':/home '+mapp[data['choice']]

    print(cmd)
    run = commands.getoutput(cmd)
    print(run)
    if 'Cannot' in run or 'Error' in run:
        return 'error'

    if len(data['port']) == 3:
        cmd = 'docker exec '+data['name']+'.'+data['mis']+' /usr/bin/shellinaboxd -t --debug --no-beep -u shellinabox -g shellinabox -c /var/lib/shellinabox -p 4200 &'
        subprocess.call(cmd,shell=True)

    cmd = 'docker exec '+data['name']+'.'+data['mis']+' service ssh start'
    subprocess.call(cmd,shell=True)

    return 'success'

