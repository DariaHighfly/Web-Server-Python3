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

'''
def send_mail(pro):
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    username = 'dariahighfly@gmail.com'
    password = '123DariaHighfly'
    sender = username 
    targets =['filitovme@gmail.com']
    #targets = []
    
    new_url = str(url)
    new_md = str(md5_code)
    my_text = 'Url: ' + new_url + '\n' + 'MD5-hash ' + new_md + '\n'
    msg = MIMEText(my_text)
    msg['Subject'] = 'Servers answer'
    msg['From'] = sender
    msg['To'] = ', '.join(targets)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()

'''

class GetHandler(tornado.web.RequestHandler):
    def get(self):

        global dictionary
        new = Process()
        new.status = 1
        new_id = self.get_argument('id')

        dictionary = dict(new_id = new)

        dictionary[new_id] = new
        res = dictionary.get(new_id)
        if res is not None:
            a = dictionary[new_id]
            b = str(a.status)
            self.write(b)

            if (b == '2'):
                c = str(a.md5)
                d = str(a.url)
                self.write({"md5": c,
                            "status": b,
                            "url": d})
                self.write('\n')
            elif (b == '1'):
                self.write({"status": "running"})
                self.write('\n')
            else:
                self.write('ERROR\n')
        else:
            self.write('NO FILE\n')

            #new_pro = Process()
            #dictionary = dict(new_id = new_pro)
            #me = dictionary[new_id]
            #ne = str(me.status)
            #if ne == 0:
            #    self.write('WE DID IT!!!!!!!!!!!\n')




#class MakeCount(tornado.web.RequestHandler):
#    def MakeCount():

class PostHandler(tornado.web.RequestHandler):
    def post(self):

        global dictionary
        pro = Process()
        pro.status = 1
        my_id = uuid.uuid4()

        dictionary = dict(my_id = pro)
    

        mail = self.get_argument('email', '1')
        url = self.get_argument('url')
        filename = "1"

        pro.url = url
        pro.mail = mail

        urllib.request.urlretrieve(url, filename)
        md5_code = getMD5sum(filename)

        pro.md5 = md5_code

        dictionary[my_id] = pro
        
        resu = dictionary.get(my_id)
        if resu is not None:
            self.write('PIPIPIP')
        #me = dictionary[my_id]
        #ne =str(me.status)
        #self.write(ne)

        if (mail != '1'):
            self.write({"id": str(my_id)})
            #send_mail(pro)
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
        #http_server = tornado.httpserver.HTTPServer(app)
        #http_server.listen(options.port)
   
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
