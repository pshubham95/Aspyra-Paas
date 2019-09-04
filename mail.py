__author__ = 'pshubham'
import smtplib,email
def sendmail(email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("coepaspyra@gmail.com", "ssm12345")

    msg = '''Hi,

                Thank you for registering.

                Regards
                Team Aspyra. '''


    server.sendmail("coepaspyra@gmail.com", email, msg)
    server.quit()

def forgot(email,password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("coepaspyra@gmail.com", "ssm12345")

    msg = '''Hi,

                Your temporary password is: '''+password+''' .
                Use the temporary password to log into the account
                Regards
                Team Aspyra. '''


    server.sendmail("coepaspyra@gmail.com", email, msg)
    server.quit()

