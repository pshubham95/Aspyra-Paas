from flask import *
from OpenSSL import SSL
from flask import session
import image_save
from nocache import nocache
import os,hashlib
from flask.ext.mysql import MySQL
from flask.ext.compress import Compress
compress = Compress()
from werkzeug import secure_filename
from hurry.filesize import size
import generate_random,generate_hash,mail,random_string,datetime,port_manage,perform_calcy,delete_calc,repeat,port_manage,single_container,db_manage
import datetime,getdisk,subprocess
import cms,getfile
from lamp import *
mysql = MySQL()



app = Flask(__name__)
compress.init_app(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'shubham123'
app.config['MYSQL_DATABASE_DB'] = 'aspyra'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = os.urandom(24)
thread = None

mysql.init_app(app)

basedir = os.path.abspath(os.path.dirname(__file__))
user_session = {}
user_data = {}
key = ''

@app.route('/')
@nocache
def main():
    return render_template('landing.html')

@app.route('/sign')
@nocache
def sign():
    resp = make_response(render_template('signin.html'))
    if 'key' in request.cookies:
        return resp
    else:
        resp.set_cookie('key',random_string.id_generator())
        return resp


@app.route('/checksession',methods=['POST'])
def checksession():
    key  = request.cookies.get('key')
    if key in session:
        return json.dumps({'status':'200'})
    return json.dumps({'status':'500'})

@app.route('/signIn',methods=['POST'])
@nocache
def signIn():
    global user_session
    _username = request.form['username']
    _password = request.form['password']
    _r = str(request.form['r'])
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "select salt from secure_login where MIS = '" + _username+ "'"
    cursor.execute(query)
    data = cursor.fetchone()
    if data is None:
        return json.dumps({'status':'Username does not exist'})
    _password = _password + data[0]
    _password = generate_hash.hash(_password)
    query = "select * from secure_login where MIS = '" + _username + "' and password = '" + _password + "'"
    cursor.execute(query)
    data = cursor.fetchone()
    if data is not None:
        global user_data
        query = "select * from secure_data"
        cursor.execute(query)
        temp = {}
        k = cursor.fetchone()
        key = str(k[0])
        #h = generate_hash.hash(str(data[3])+key)
        temp['name']= str(data[1])
        temp['number'] = str(data[2])
        temp['email'] = str(data[6])
        temp['url'] = str(data[7])
        temp['fg'] = str(data[8])
        temp['mis'] = str(data[3])
        temp['id'] = str(data[0])
        temp['calcy_alp_gcc'] = False
        temp['calcy_alp_cplus'] = False
        temp['calcy_alp_java'] = False
        temp['calcy_alp_py'] = False
        temp['password'] = request.form['password']
        resp = make_response(json.dumps({'status':'200'}))
        if _r == '1':
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=90)
            resp.set_cookie('key', request.cookies.get('key'), expires=expire_date)

        session[request.cookies.get('key')] = temp


        #user_session['username'] = _username

        return resp
    else:
        return json.dumps({'status':'Incorrect Password'})


@app.route('/SignUp',methods=['POST'])
def SignUp():
    connection = mysql.connect()
    cursor = connection.cursor()
    _mis = request.form['mis']
    _fname = request.form['f_name']
    _passwd = request.form['passwd_reg']
    _email = request.form['email_reg']
    _phone = request.form['number_reg']
    _salt = generate_random.generate_random()
    _passwd = _passwd + _salt
    _passwd = generate_hash.hash(_passwd)
    os.makedirs(basedir+'/static/uploads/'+_mis)
    os.makedirs(basedir+'/static/uploads/'+_mis+'/apps')
    os.makedirs(basedir+'/static/uploads/'+_mis+'/calcy')
    os.makedirs(basedir+'/static/uploads/'+_mis+'/store')
    os.makedirs(basedir+'/static/uploads/'+_mis+'/share')



    query = "INSERT INTO secure_login (email,password,salt,name,number,MIS) VALUES ('" + _email + "','" + _passwd + "','" + _salt + "','" + _fname + "','" + _phone + "','" + _mis + "' )"
    cursor.execute(query)
    connection.commit()
    mail.sendmail(_email)
    return json.dumps({'status':'200'})


@app.route('/forgot_pass')
@nocache
def forgot_pass():
    return render_template('forgot.html')


@app.route('/forgot',methods=['POST'])
def forgot():
    _mis = request.form['mis']
    _email = request.form['username']
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "select id from secure_login where MIS = '" + _mis+ "' and email = '" + _email + "'"
    cursor.execute(query)
    data = cursor.fetchone()
    if data is None:
        return json.dumps({'html':'404'})
    _salt = generate_random.generate_random()
    _pass = generate_random.generate_random()
    _passwd = _pass + _salt
    _passwd = generate_hash.hash(_passwd)
    query = "update secure_login set salt = '" + _salt + "' , password = '" + _passwd + "' , fg = '1' where MIS = '" + _mis + "' and email = '" + _email + "'"
    cursor.execute(query)
    connection.commit()
    mail.forgot(_email,_pass)
    return json.dumps({'r':query})


@app.route('/checkfg',methods=['POST'])
def checkfg():
    mis = request.form['key']
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "select fg from secure_login where id = '" + session[mis]['id']+ "'"
    cursor.execute(query)
    data = cursor.fetchone()
    if data[0] == '1':
        return json.dumps({'status':'forgot'})
    else:
        return json.dumps({'status':'nfg'})


@app.route('/photo',methods=['POST','GET'])
def photo():
    connection = mysql.connect()
    cursor = connection.cursor()
    files = request.files['input-file-preview']
    mis = str(request.form['mis'])
    if files :
        updir = os.path.join(basedir, 'static/uploads/'+mis)
        files.save(os.path.join(updir, mis+'.png'))
        image_save.save_image(os.path.join(updir, mis+'.png'),mis,updir)
        up = '../static/uploads/'+mis+'/'+mis
        query = "update secure_login set profile_url = '" + up + "' WHERE MIS = '" + mis + "'"
        cursor.execute(query)
        connection.commit()
        return json.dumps({'html':query})



@app.route('/checkusername',methods=['POST'])
def checkusername():
    _mis = request.form['mis']

    connection = mysql.connect()
    cursor = connection.cursor()
    query = "select id from secure_login where MIS = '" + _mis +"'"
    cursor.execute(query)
    connection.commit()
    data = cursor.fetchone()
    if data is None:
        return json.dumps({'status':'available'})
    else:
        return json.dumps({'status':'na'})

@app.route('/checkappname',methods=['POST'])
def checkappname():
    appname = request.form['name']
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "select pid from app where name = '" + appname +"'"
    cursor.execute(query)
    connection.commit()
    data = cursor.fetchone()
    if data is None:
        return json.dumps({'status':'available'})
    else:
        return json.dumps({'status':'na'})


@app.route('/login')
@nocache
def login():

    id =  request.cookies.get('key')
    if id in session:
        return render_template('src/index.html')

    return render_template('no_login.html')


@app.route('/check_login',methods=['GET'])
def check_login():
    global user_session
    if 'username' in user_session:
        return json.dumps({'status':'200' + str(user_session)})
    else:
        return json.dumps({'status':'500'})


@app.route('/change_pass')
@nocache
def change_pass():
    id =  request.args.get('id')
    if id in session:
        return render_template('change_pass.html')
    return render_template('no_login.html')



@app.route('/change_pass_db',methods=['POST'])
def change_pass_db():
    connection = mysql.connect()
    cursor = connection.cursor()
    _passwd = request.form['form']
    _salt = generate_random.generate_random()
    _passwd = _passwd + _salt
    _passwd = generate_hash.hash(_passwd)
    id = request.form['id']
    query = "update secure_login set password = '" +_passwd+"' , salt = '" + _salt + "' , fg = '0' where id = '" + session[id]['id'] +"'"
    cursor.execute(query)
    connection.commit()
    return json.dumps({'status':'200'})

@app.route('/del_con',methods=['POST'])
def del_con():
    id =  request.cookies.get('key')
    if(session[id]['calcy_alp_gcc']):
        if(session[id]['calcy_alp_gcc']['back'] == 'false'):
            delete_calc.delete_calc(session[id]['calcy_alp_gcc']['name'])
            port_manage.setPort([session[id]['calcy_alp_gcc']['op']])
            session[id]['calcy_alp_gcc'] = False
        else:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = 'INSERT INTO calcy (mis,con_name,port,con_type) VALUES ("'+session[id]['mis']+'","'+session[id]['calcy_alp_gcc']['name']+'","'+session[id]['calcy_alp_gcc']['op']+'","gcc")'
            cursor.execute(query)
            connection.commit()


    if(session[id]['calcy_alp_py']):
        if(session[id]['calcy_alp_py']['back'] == 'false'):

            delete_calc.delete_calc(session[id]['calcy_alp_py']['name'])
            port_manage.setPort([session[id]['calcy_alp_py']['op']])
            session[id]['calcy_alp_py'] = False
        else:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = 'INSERT INTO calcy (mis,con_name,port,con_type) VALUES ("'+session[id]['mis']+'","'+session[id]['calcy_alp_py']['name']+'","'+session[id]['calcy_alp_py']['op']+'","py")'
            cursor.execute(query)
            connection.commit()


    if(session[id]['calcy_alp_cplus']):
        if(session[id]['calcy_alp_cplus']['back'] == 'false'):
            delete_calc.delete_calc(session[id]['calcy_alp_cplus']['name'])
            port_manage.setPort([session[id]['calcy_alp_cplus']['op']])
            session[id]['calcy_alp_cplus'] = False

        else:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = 'INSERT INTO calcy (mis,con_name,port,con_type) VALUES ("'+session[id]['mis']+'","'+session[id]['calcy_alp_cplus']['name']+'","'+session[id]['calcy_alp_cplus']['op']+'","cplus")'
            cursor.execute(query)
            connection.commit()


    if(session[id]['calcy_alp_java']):
        if(session[id]['calcy_alp_java']['back'] == 'false'):
            delete_calc.delete_calc(session[id]['calcy_alp_java']['name'])
            port_manage.setPort([session[id]['calcy_alp_java']['op']])
            session[id]['calcy_alp_java'] = False

        else:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = 'INSERT INTO calcy (mis,con_name,port,con_type) VALUES ("'+session[id]['mis']+'","'+session[id]['calcy_alp_java']['name']+'","'+session[id]['calcy_alp_java']['op']+'","java")'
            cursor.execute(query)
            connection.commit()


    return json.dumps({'status':'success'})



@app.route('/logout',methods=['POST','GET'])
def logout():
    id =  request.cookies.get('key')
    resp = make_response(render_template('logout.html'))
    if 'key' in request.cookies and id in session:
        resp.set_cookie('key', '', expires=0)
        if(session[id]['calcy_alp_gcc']):
            #delete_calc.delete_calc(session[id]['calcy_alp_gcc']['name'])
            port_manage.setPort([session[id]['calcy_alp_gcc']['op']])

        if(session[id]['calcy_alp_py']):
            #delete_calc.delete_calc(session[id]['calcy_alp_py']['name'])
            port_manage.setPort([session[id]['calcy_alp_py']['op']])


        if(session[id]['calcy_alp_cplus']):
            #delete_calc.delete_calc(session[id]['calcy_alp_cplus']['name'])
            port_manage.setPort([session[id]['calcy_alp_cplus']['op']])


        if(session[id]['calcy_alp_java']):
            #delete_calc.delete_calc(session[id]['calcy_alp_java']['name'])
            port_manage.setPort([session[id]['calcy_alp_java']['op']])

        del_con()
        session.pop(id,None)

        return resp
    return render_template('no_login.html')


@app.route('/getuser_data',methods=['POST'])
def getuser_data():
    mis = request.form['key']
    return json.dumps({'name':session[mis]['name'],'number':session[mis]['number'],'mis':session[mis]['mis'],'email':session[mis]['email'],'url':session[mis]['url'],'id':session[mis]['id']})





@app.route('/profile')
@nocache
def profile():
    id =  request.cookies.get('key')
    if id in session:
        return render_template('profile.html')
    return render_template('no_login.html')



@app.route('/faq')
@nocache
def faq():
    id =  request.args.get('id')
    if id in session:
        return render_template('draft_1/faq.html')
    return render_template('no_login.html')


@app.route('/getkey',methods=['POST'])
@nocache
def getkey():
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "select * from secure_data"
    cursor.execute(query)
    k = cursor.fetchone()
    return json.dumps({'key':str(k[0])})

@app.route('/shellinabox')
@nocache
def shellinabox():
    id = request.args.get('id')
    if id in session:
        return render_template('draft_1/shubham.html')
    return render_template('no_login.html')

@app.route('/deploy_test')
@nocache
def deploy_test():
    id =  request.cookies.get('key')
    if id in session:
        return render_template('deploy_test.html')
    return render_template('no_login.html')

@app.route('/stop_calcy')
@nocache
def stop_calcy():
    id = request.cookies.get('key')
    name = request.args.get('id')
    if id in session:
        subprocess.call('docker rm -f '+name,shell=True)
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "delete from calcy where mis = '"+session[id]['mis']+"' and con_name = '"+name+"'"
        print(query)
        cursor.execute(query)
        connection.commit()
        return render_template('src/index.html')
    return render_template('no_login.html')


@app.route('/deploy_test_handle',methods=['POST'])
def deploy_test_handle():
    files = request.files['exec']
    id = request.cookies.get('key')
    mis = session[id]['mis']
    data = {}
    data['name'] = request.form['name']
    data['mis'] = mis
    data['choice'] = request.form['choice']
    mapp = {'1':'ubuntu_gcc','2':'ubuntu_cplus_shell','3':'ubuntu_java','4':'ubuntu_python2.7','5':'lamp_shell','6':'tomcat_mysql','7':'flask_shell','8':'ubuntu_python3.4'}
    data['dir'] = os.path.join(basedir, 'static/uploads/'+mis+'/apps/'+data['name'])
    endpoint = ''
    if id in session:
        if(data['choice'] == '1' or data['choice'] == '2' or data['choice'] == '3' or data['choice'] == '4' or data['choice'] == '8'):
            endpoint = '/single_port'
            port = port_manage.getPort(2)

        if(data['choice'] == '5'):
            endpoint = '/apache'
            port = port_manage.getPort(3)

        if(data['choice'] == '7' or data['choice'] == '6'):
            if(data['choice'] == '7'):
                endpoint = '/flask'
            else:
                endpoint = '/tomcat'
            port = port_manage.getPort(3)
        data['port'] = port
        os.makedirs(basedir+'/static/uploads/'+mis+'/apps/'+data['name'])
        ret = single_container.single_container_create(data,mapp)
        if ret == 'success':
            db_manage.db_insert_app(mis,data['name'],port,'started','1',endpoint)
            filename = secure_filename(files.filename)
            updir = data['dir']
            files.save(os.path.join(updir, filename))
            return json.dumps({'status':'success'})
        os.system('rm -rf '+data['dir'])
        return json.dumps({'status':'error'})

    return json.dumps({'status':'error'})

@app.route('/file_handle_deploy',methods=['POST'])
@nocache
def file_handle_deploy():
    id = request.cookies.get('key')
    if id in session:
        appn = request.form['name']
        files = request.files['exec']
        updir = os.path.join(basedir, 'static/uploads/'+session[id]['mis']+'/apps/'+appn)
        filename = secure_filename(files.filename)
        files.save(os.path.join(updir, filename))
        return json.dumps({'status':'success'})
    return json.dumps({'status':'error'})



@app.route('/deploy_test_success')
@nocache
def deploy_test_success():
    id = request.cookies.get('key')
    if id in session:
        return render_template('deploy_success.html')
    return render_template('no_login.html')

@app.route('/drupal_app')
@nocache
def drupal_app():
    id = request.cookies.get('key')
    if id in session:
        return render_template('drupalApp.html')
    return render_template('no_login.html')

@app.route('/single_port')
@nocache
def single_port():
    id = request.cookies.get('key')
    if id in session:
        return render_template('single_portapps.html')
    return render_template('no_login.html')

@app.route('/getdisk',methods=['POST'])
@nocache
def get_disk():
    id = request.cookies.get('key')
    if id in session:
        pid = request.form['pid']
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "select name from app where mis = '" + session[id]['mis'] + "' and pid = '" + pid + "'"
        cursor.execute(query)
        data = cursor.fetchone()
        updir = os.path.join(basedir, 'static/uploads/'+session[id]['mis']+'/apps/'+data[0])
        return json.dumps({'size':size(getdisk.getFolderSize(updir)),'real':getdisk.getFolderSize(updir)})


@app.route('/getstore',methods=['POST'])
@nocache
def getstore():
    id = request.cookies.get('key')
    updir = os.path.join(basedir, 'static/uploads/'+session[id]['mis']+'/store')
    return json.dumps({'size':size(getdisk.getFolderSize(updir)),'real':getdisk.getFolderSize(updir)})

@app.route('/get_file_dir',methods=['POST'])
@nocache
def get_file_dir():
    id = request.cookies.get('key')
    updir = os.path.join(basedir, 'static/uploads/'+session[id]['mis']+'/store')
    return json.dumps({'dir':getfile.getdir(updir),'file':getfile.getfile(updir)})

@app.route('/get_file_dir_share',methods=['POST'])
@nocache
def get_file_dir_share():
    id = request.cookies.get('key')
    updir = os.path.join(basedir, 'static/uploads/'+session[id]['mis']+'/share')
    return json.dumps({'dir':getfile.getdir(updir),'file':getfile.getfile(updir)})


@app.route('/store_file',methods=['POST'])
def store_file():
    id = request.cookies.get('key')
    if id in session:
        files = request.files['zipup']
        updir = os.path.join(basedir, 'static/uploads/'+session[id]['mis']+'/store/')
        filename = secure_filename(files.filename)
        files.save(os.path.join(updir, filename))
        return json.dumps({'status':'success'})
    return render_template('no_login.html')




@app.route('/apache')
@nocache
def apache():
    id = request.cookies.get('key')
    if id in session:
        return render_template('apache.html')
    return render_template('no_login.html')

@app.route('/tomcat')
@nocache
def tomcat():
    id = request.cookies.get('key')
    if id in session:
        return render_template('tomcat.html')
    return render_template('no_login.html')

@app.route('/flask')
@nocache
def flask():
    id = request.cookies.get('key')
    if id in session:
        return render_template('flask.html')
    return render_template('no_login.html')

@app.route('/cms_app')
@nocache
def cms_app():
    id = request.cookies.get('key')
    if id in session:
        return render_template('cmsApp.html')
    return render_template('no_login.html')

@app.route('/lamp_app')
@nocache
def lamp_app():
    id = request.cookies.get('key')
    if id in session:
        return render_template('lampApp.html')
    return render_template('no_login.html')

@app.route('/tomcat_app')
@nocache
def tomcat_app():
    id = request.cookies.get('key')
    if id in session:
        return render_template('tomcatApp.html')
    return render_template('no_login.html')

@app.route('/deploy_db_app')
@nocache
def deploy_db_app():
    id = request.cookies.get('key')
    if id in session:
        return render_template('deployDbApp.html')
    return render_template('no_login.html')

def drupal_app():
    id = request.cookies.get('key')
    if id in session:
        return render_template('tomcatApp.html')
    return render_template('no_login.html')





@app.route('/deploy_test_err')
@nocache
def deploy_test_err():
    id = request.cookies.get('key')
    if id in session:
        return render_template('deploy_err.html')
    return render_template('no_login.html')

@app.route('/deploy')
@nocache
def deploy():
    id = request.cookies.get('key')

    if id in session:
        return render_template('deploy.html')
    return render_template('no_login.html')

@app.route('/deploy_cms')
@nocache
def deploy_cms():
    id = request.cookies.get('key')
    if id in session:
        return render_template('deploy_cms.html')
    return render_template('no_login.html')

@app.route('/cms_stop',methods=['POST'])
@nocache
def cms_stop():
    pid = request.form['pid']
    id = request.cookies.get('key')
    if id in session:
        cms.stop_cms(pid)
        return json.dumps({'status':'success'})
    return render_template('no_login.html')

@app.route('/type2_stop',methods=['POST'])
@nocache
def type2_stop():
    pid = request.form['pid']
    id = request.cookies.get('key')
    if id in session:
        stop_deploy(pid)
        return json.dumps({'status':'success'})
    return render_template('no_login.html')

@app.route('/type2_start',methods=['POST'])
@nocache
def type2_start():
    pid = request.form['pid']
    id = request.cookies.get('key')
    if id in session:
        start_deploy(pid)
        return json.dumps({'status':'success'})
    return render_template('no_login.html')

@app.route('/type2_delete',methods=['POST'])
@nocache
def type2_delete():
    pid = request.form['pid']
    id = request.cookies.get('key')
    if id in session:
        stop_deploy(pid)
        return json.dumps({'status':'success'})
    return render_template('no_login.html')


@app.route('/cms_start',methods=['POST'])
@nocache
def cms_start():
    pid = request.form['pid']
    id = request.cookies.get('key')
    if id in session:
        cms.start_cms(pid)
        return json.dumps({'status':'success'})
    return render_template('no_login.html')

@app.route('/cms_delete',methods=['POST'])
@nocache
def cms_delete():
    pid = request.form['pid']
    id = request.cookies.get('key')
    if id in session:
        cms.delete_cms(pid)
        return json.dumps({'status':'success'})
    return render_template('no_login.html')




@app.route('/cms_deploy',methods=['POST'])
@nocache
def cms_deploy():
    id = request.cookies.get('key')

    if id in session:
        data = {}
        data['mis'] = session[id]['mis']
        data['choice'] = request.form['choice']
        data['name'] = request.form['appn']
        data['db'] = request.form['db']
        data['pass'] = session[id]['password']
        print data['pass']
        '''choice 1 -> wordpress, 2 -> joomla , 3 -> drupal'''
        '''db choice 1 -> mysql , 2 -> sqllite'''
        print(data['choice'])
        if int(data["choice"]) == 1:
            print("wordpress")
            retString = cms.deploy_wordpress(data)
        elif int(data["choice"]) == 2:
            print("joomla")
            retString = cms.deploy_joomla(data)
        elif int(data["choice"]) == 3:
            if int(data["db"]) == 1:
                print("Drupal MySQL")
                retString = cms.deploy_drupal_mysql(data)
            elif int(data["db"]) == 2:
                print("Drupal SQLite")
                retString = cms.deploy_drupal_lite(data)

        return json.dumps({'status':retString['status']})

    return render_template('no_login.html')

'''lamp app - no DB'''
@app.route('/deployfile_zip',methods=['POST'])
@nocache
def deployfile_zip():
    files = request.files['zipup']
    data = {}
    id = request.cookies.get('key')
    data['name'] = request.form['name']
    mis = session[id]['mis']
    os.makedirs(basedir+'/static/uploads/'+mis+'/apps/'+data['name']+'/zip')
    os.makedirs(basedir+'/static/uploads/'+mis+'/apps/'+data['name']+'/sql')

    updir = os.path.join(basedir, 'static/uploads/'+mis+'/apps/'+data['name']+'/zip/')
    files.save(os.path.join(updir, data['name']+'.zip'))
    data['mis'] = mis
    data['type'] = request.form['opt']
    data['path'] = updir
    data['filename'] = data['name']+'.zip'
    data['sql'] = basedir+'/static/uploads/'+mis+'/apps/'+data['name']+'/sql'
    data['pass'] = session[id]['password']
    data['dbName'] = "myDB"
    data['dump'] = data['name']+'.sql'
    if request.form['dump'] == 'false':
        return json.dumps({'status':str(data)})
    else:
        if data["type"] == '1':
            returnString = run_lamp_app(data)
        elif data["type"] == '4':
            returnString = run_tomcat_app(data)
        return json.dumps({'status':str(request.form['dump'])})
    return json.dumps({'status':str(request.form['dump'])})


@app.route('/deployfile_dump',methods=['POST'])
@nocache
def deployfile_dump():
    files = request.files['dump']
    data = {}
    id = request.cookies.get('key')
    data['name'] = request.form['name']
    mis = session[id]['mis']
    updir = os.path.join(basedir, 'static/uploads/'+mis+'/apps/'+data['name']+'/sql/')
    files.save(os.path.join(updir, data['name']+'.sql'))
    data['type'] = request.form['opt']
    data['mis'] = mis
    data['path'] = basedir + '/static/uploads/'+mis+'/apps/'+data['name']+'/zip/'
    data['filename'] = data['name']+'.zip'
    data['sql'] = basedir+'/static/uploads/'+mis+'/apps/'+data['name']+'/sql'
    data['pass'] = session[id]['password']
    data['dbName'] = request.form['db_name']
    data['dump'] = data['name']+'.sql'
    print(data)
    if request.form['dump'] == 'true':
        print("test")
        if data["type"] == '2':
            returnString = run_db_app(data)
        return json.dumps({'status':str(data)})
    else:
        return json.dumps({'status':'sql'})


@app.route('/calcy')
@nocache
def calcy():
    id = request.cookies.get('key')
    if id in session:
        return render_template('calcy.html')
    return render_template('no_login.html')


@app.route('/check_share',methods=['POST'])
@nocache
def check_share():
    id = request.cookies.get('key')
    if id in session:
        _mis = request.form['mis']
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "select name from secure_login where MIS = '" + _mis +"'"
        cursor.execute(query)
        connection.commit()
        data = cursor.fetchone()
        if data is None:
            return json.dumps({'status':'na',})
        else:
            return json.dumps({'status':'available','name':data[0]})
    return render_template('error.html')

@app.route('/calcy_deploy',methods=['POST'])
@nocache
def calcy_deploy():
    id = request.cookies.get('key')
    if(request.form['class'] != ''):
        r = request.form['class']
        cl = r
    else:
        r = 'temp'
        cl = ''
    lang_ext_map = {'1':['.c','calcy_alp_gcc'],'2':['.java','calcy_alp_java'],'3':['.py','calcy_alp_py'],'4':['.cpp','calcy_alp_cplus']}
    if id in session:
        fo = open(basedir+'/static/uploads/'+session[id]['mis']+'/calcy/'+r+lang_ext_map[request.form['lang']][0], "w+")
        fo.write(request.form['code'])
        fo.close()
        pr = False
        if session[id][lang_ext_map[request.form['lang']][1]]:
            pr = True
            port =  session[id][lang_ext_map[request.form['lang']][1]]['op']

        else:
            port = port_manage.getPort(1)
            port = port[0]

        data = {'mis':session[id]['mis'],'lang':request.form['lang'],'type':lang_ext_map[request.form['lang']][1],'op':port,'dir':basedir+'/static/uploads/'+session[id]['mis']+'/calcy','f_name':r+lang_ext_map[request.form['lang']][0],'pip':request.form['pip'],'class':request.form['class'],'name':id+lang_ext_map[request.form['lang']][1],'pr':pr,'class':cl,'back':request.form['back']}
        if(data['pip'] != ''):
            data['pip'] = data['pip'].split(',')
        status = perform_calcy.perform_calc(data)


        if(status['succ'] == 1):
            session[id][lang_ext_map[request.form['lang']][1]] = data
            status['port'] = port
        return json.dumps({'status':status})
    return render_template('no_login.html')

@app.route('/gettable_data',methods=['POST'])
def gettable_data():
    id = request.cookies.get('key')
    if id in session:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "select * from app where MIS = '" + session[id]['mis'] + "'"
        cursor.execute(query)
        data = cursor.fetchall()
        if data is not None:
            return json.dumps(data)

@app.route('/get_calcy_data',methods=['POST'])
def get_calcy_data():
    id = request.cookies.get('key')
    if id in session:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "select * from calcy where mis = '" + session[id]['mis'] + "'"
        cursor.execute(query)
        data = cursor.fetchall()
        if data is not None:
            return json.dumps(data)

@app.route('/error')
@nocache
def error():
    return render_template('error.html')

@app.route('/get_num_app',methods=['POST'])
@nocache
def get_num_app():
    id = request.cookies.get('key')
    type = request.form['type']
    if id in session:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "select pid from app where MIS = '" + session[id]['mis'] + "' AND type = '"+type+"'"
        cursor.execute(query)
        data = cursor.fetchall()
        return json.dumps(data)

@app.route('/three_error')
@nocache
def three_error():
    id = request.cookies.get('key')
    if id in session:
        return render_template('three_error.html')
    return render_template('no_login.html')

@app.route('/getapp_data',methods=['POST'])
@nocache
def getapp_data():
    id = request.cookies.get('key')
    p = request.form['pid']
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "select * from app where mis = '" + session[id]['mis'] + "' and pid = '" + p + "'"
    cursor.execute(query)
    data = cursor.fetchone()
    return json.dumps({'name':data[2],'port':data[4],'status':data[5],'type':data[6]})

@app.route('/stop_single_c',methods=['POST'])
@nocache
def stop_single_c():
    id = request.cookies.get('key')
    if id in session:
        n = request.form['name']
        db_manage.db_update_status(n+'.'+session[id]['mis'],'stopped')
        cmd = 'docker stop '+n+'.'+session[id]['mis']
        subprocess.call(cmd,shell=True)
        return json.dumps({'status':'success'})
    return render_template('no_login.html')

@app.route('/start_single_c',methods=['POST'])
@nocache
def start_single_c():
    id = request.cookies.get('key')
    if id in session:
        n = request.form['name']
        db_manage.db_update_status(n+'.'+session[id]['mis'],'started')
        cmd = 'docker start '+n+'.'+session[id]['mis']
        subprocess.call(cmd,shell=True)
        return json.dumps({'status':'success'})
    return render_template('no_login.html')

@app.route('/del_single_c',methods=['POST'])
@nocache
def del_single_c():
    id = request.cookies.get('key')
    if id in session:
        n = request.form['name']
        updir = os.path.join(basedir, 'static/uploads/'+session[id]['mis']+'/apps/'+n)
        pid = request.form['pid']
        db_manage.db_delete_app(pid)
        cmd = 'docker rm -f '+n+'.'+session[id]['mis']
        subprocess.call(cmd,shell=True)
        subprocess.call('rm -rf '+updir,shell=True)

        return json.dumps({'status':'success'})
    return render_template('no_login.html')

'''@app.route('/start_deploy_app',methods=['POST'])
@nocache
def start_deploy_app():


@app.route('/stop_deploy_app',methods=['POST'])
@nocache
def stop_deploy_app():

@app.route('/del_deploy_app',methods=['POST'])
@nocache
def del_deploy_app():'''

@app.route('/drive_save')
@nocache
def drive_save():
    id = request.cookies.get('key')
    if id in session:
        return render_template('drive_store.html')
    return render_template('no_login.html')

@app.route('/store_overview')
@nocache
def store_overview():
    id = request.cookies.get('key')
    if id in session:
        return render_template('drive_download .html')
    return render_template('no_login.html')

@app.route('/edit')
@nocache
def edit():
    id = request.cookies.get('key')
    if id in session:
        return render_template('edit.html')
    return render_template('no_login.html')

@app.route('/get_edit_data',methods=['POST'])
@nocache
def get_edit_data():
    global myfile
    src = request.form['src']
    mis = request.form['mis']
    id = request.cookies.get('key')
    if id in session:
        if mis == session[id]['mis']:
            myfile = open(src,'r')
            data=myfile.read()
            myfile.close()
            return json.dumps({'data':data})
    return json.dumps({'data':'error'})

@app.route('/success_write')
@nocache
def success_write():
    id = request.cookies.get('key')
    if id in session:
        return render_template('success_write.html')
    return render_template('no_login.html')

@app.route('/set_edit_data',methods=['POST'])
@nocache
def set_edit_data():
    src = request.form['src']
    mis = request.form['mis']
    data = request.form['data']
    id = request.cookies.get('key')
    if id in session:
        if mis == session[id]['mis']:
            myfile = open(src,'w+')
            myfile.write(data)
            myfile.close()
            return json.dumps({'data':'success'})
    return json.dumps({'data':'error'})

@app.route('/view_txt')
@nocache
def view_txt():
    id = request.cookies.get('key')
    if id in session:
        return render_template('view_txt.html')
    return render_template('no_login.html')

@app.route('/download',methods=['GET','POST'])
@nocache
def download():
    id = request.cookies.get('key')
    if id in session:
        updir = request.args.get('folder')
        updir =  os.path.dirname(updir)

        src = request.args.get('src')
        return send_from_directory(updir,src,as_attachment=True)
    return render_template('no_login.html')



@app.route('/view_pdf')
@nocache
def view_pdf():
    id = request.cookies.get('key')
    src = request.args.get('src')
    if id in session:
        if src.split('/')[7] == session[id]['mis']:
            return render_template('view_pdf.html')
        return render_template('error.html')
    return render_template('no_login.html')

@app.route('/share_file')
def share_file():
    id = request.cookies.get('key')
    mis = request.args.get('mis')
    src = request.args.get('src')
    if id in session:
        if src.split('/')[7] == session[id]['mis']:
            if not os.path.isdir(basedir+'/static/uploads/'+mis+'/share/'+session[id]['mis']):
                os.makedirs(basedir+'/static/uploads/'+mis+'/share/'+session[id]['mis'])
            updir = os.path.join(basedir, 'static/uploads/'+mis+'/share/'+session[id]['mis'])

            subprocess.call(['ln',src,updir])
            return render_template('share.html')
        return render_template('error.html')
    return render_template('no_login.html')

@app.route('/unzip')
@nocache
def unzip():
    id = request.cookies.get('key')
    src = request.args.get('src')
    if id in session:
        if src.split('/')[7] == session[id]['mis']:
            dire =  os.path.dirname(src)
            subprocess.call(['unzip','-o','-j',src,'-d',dire])
            return render_template('drive_download .html')
        return render_template('error.html')
    return render_template('no_login.html')

@app.route('/view_video')
@nocache
def view_video():
    id = request.cookies.get('key')
    src = request.args.get('src')
    if id in session:
        if src.split('/')[7] == session[id]['mis']:
            return render_template('view_video.html')
        return render_template('error.html')
    return render_template('no_login.html')

@app.route('/view_audio')
@nocache
def view_audio():
    id = request.cookies.get('key')
    src = request.args.get('src')
    if id in session:
        if src.split('/')[7] == session[id]['mis']:
            return render_template('view_audio.html')
        return render_template('error.html')
    return render_template('no_login.html')

@app.route('/delete_store_file')
@nocache
def delete_store_file():
    id = request.cookies.get('key')
    src = request.args.get('src')
    if id in session:
        if src.split('/')[7] == session[id]['mis']:
            subprocess.call(['rm',src])
            return render_template('drive_download .html')
        return render_template('error.html')
    return render_template('no_login.html')

@app.route('/keep')
@nocache
def keep():
    id = request.cookies.get('key')
    src = request.args.get('src')
    if id in session:
        if src.split('/')[7] == session[id]['mis']:
            updir = os.path.join(basedir, 'static/uploads/'+session[id]['mis']+'/store/')
            subprocess.call(['mv',src,updir])
            updir = os.path.join(basedir, 'static/uploads/'+session[id]['mis']+'/share/')
            try:
                os.rmdir(updir+src.split('/')[9])
            except OSError as ex:
                print('not empty so not deleting')
            return render_template('drive_download .html')
        return render_template('error.html')
    return render_template('no_login.html')

@app.route('/delete_folder')
@nocache
def delete_folder():
    id = request.cookies.get('key')
    src = request.args.get('src')
    if id in session:
        if src.split('/')[7] == session[id]['mis']:
            subprocess.call(['rm','-rf',src])
            return render_template('drive_download .html')
        return render_template('error.html')
    return render_template('no_login.html')

@app.route('/folder')
@nocache
def folder():
    id = request.cookies.get('key')
    if id in session:
        return render_template('folder.html')

    return render_template('no_login.html')

@app.route('/folder_share')
@nocache
def folder_share():
    id = request.cookies.get('key')
    if id in session:
        return render_template('folder_share.html')

    return render_template('no_login.html')

@app.route('/get_dir',methods=['POST'])
@nocache
def get_dir():
    id = request.cookies.get('key')
    src = request.form['dir']
    if id in session:
        if src.split('/')[7] == session[id]['mis']:
            updir = src
            return json.dumps({'dir':getfile.getdir(updir),'file':getfile.getfile(updir)})

        return render_template('error.html')
    return render_template('no_login.html')

@app.route('/view_image')
@nocache
def view_image():
    id = request.cookies.get('key')
    src = request.args.get('src')
    if id in session:
        if src.split('/')[7] == session[id]['mis']:
            return render_template('view_image.html')
        return render_template('error.html')
    return render_template('no_login.html')





if __name__ == '__main__':
    context = ('host.cert', 'host.key')
    app.run(host='0.0.0.0',port=8080,threaded=True,debug=True,use_reloader=False,ssl_context=context)
