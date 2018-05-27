import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys
import os
import hashlib
import urllib.request
import uuid
import smtplib
import threading
import time
import struct

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from tornado.options import define, options
#options read options from the command line

# КОДЫ СТАТУСОВ
# status_noexist = 0 #задания не существует
status_inprocess = 1 #задание в работе
status_fincorrect = 2 #задание завершено удачно
status_finerror = 3 #задание завершено с ошибкой

define("port", default=8080, help="run on the given port", type=int)
#if user runs the program with the --help parameter,
#the program will print out all of the options in defined

class Process:
    status = 0;
    url = '1'
    mail = '1'
    md5 = '1'


dictionary = {} #dictionary
    #number of process : status, url, mail, md5

def getMD5sum(fileName):
    m = hashlib.md5()
    fd = open(fileName, 'rb')
    b = fd.read()
    m.update(b)
    fd.close()
    return m.hexdigest()


def send_mail(pro):

    n_url = pro.url
    n_mail = pro.mail
    n_md = pro.md5
    
    new_url = str(n_url)
    new_md = str(n_md)
    new_mail = str(n_mail)

    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    username = 'dariahighfly@gmail.com'
    password = '123DariaHighfly'
    sender = username 
    targets = new_mail
    
    my_text = ('Hi!\n' + 'Url: ' + new_url + '\n' +
            'MD5-hash ' + new_md + '\n')

    msg = MIMEText(my_text)
    msg['Subject'] = 'HELLO'
    msg['From'] = sender
    msg['To'] = targets


    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()


class GetHandler(tornado.web.RequestHandler):
    def get(self):

        global dictionary

        new_id = self.get_argument('id')
        id_str = str(new_id)

        res = dictionary.get(id_str)
        if res is not None:
            struc = dictionary[id_str]
            a = struc.status
            stat  = str(a)
            b = struc.url
            ur = str(b)
            c = struc.md5
            mmdd = str(c)

            if (stat == '2'):
                self.write('md5: ')
                self.write(mmdd)
                self.write('\n')
                self.write('status: done\n')
                #self.write(stat)
                self.write('url: ')
                self.write(ur)
                self.write('\n')
            elif (stat == '1'):
                self.write('status : running')
                self.write('\n')
            else:
                self.write('ERROR\n')
        else:
            self.write('NO FILE\n')


#class MakeCount(tornado.web.RequestHandler):
#    def MakeCount():

class PostHandler(tornado.web.RequestHandler):
    def post(self):

        global dictionary
        pro = Process()
        pro.status = 1
        my_id = uuid.uuid4()

        id_to_type = str(my_id)
        dictionary[id_to_type] = pro
        
        self.write('\n')

        mail = self.get_argument('email', '1')
        url = self.get_argument('url')
        filename = "1"

        pro.url = url
        pro.mail = mail

        urllib.request.urlretrieve(url, filename)
        md5_code = getMD5sum(filename)

        pro.md5 = md5_code

        dictionary[id_to_type] = pro
        change = dictionary[id_to_type]
        change.status = 2
        
        print({"id": str(my_id)}) # ID нужно,
        #чтобы можно было проверить работу GET

        if (mail != '1'):
            self.write({"id": str(my_id)})
            send_mail(pro)
            self.write('\n')
        else:
            self.write({"url": url})
            self.write('\n')
            self.write({"md5": md5_code})
            self.write('\n')

'''
class PostHandler(tornado.web.RequestHandler):
    def post(self):
        #id1 = uuid.uuid4()
        #self.write({"id": str(id1)})
        download_thread = threading.Thread(
                    target=MakeCount,
                    args=())
        download_thread.start()
'''

if __name__ == "__main__":

    while True:
        tornado.options.parse_command_line()
   
        app = tornado.web.Application(
            handlers=[
                (r"/submit", PostHandler),
                (r"/check",GetHandler)
            ]
        )

        # list of tuples
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
