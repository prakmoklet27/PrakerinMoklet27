# -*- coding: utf-8 -*-
import json
from odoo import http, _,exceptions 
from odoo.http import request
import time
import locale
import random
import smtplib
import string
# import bcrypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pusher import Pusher

# configure pusher object
pusher = Pusher(
app_id='1019595',
key='ec0971857e980f699709',
secret='d4a647edb00e85d10eed',
cluster='ap1',
ssl=True)

class Erups(http.Controller):

    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8'   )
    
    def __init__(self):
        self._model_erups = "erups"
        self._model_erups_agenda = "erups_agenda"
        self._model_erups_question = "erups_question"
        self._model_erups_registrasi = "erups_registrasi"
        self._model_erups_evoting = "erups_evoting"
        
    # @http.route('/message',type='http', auth='public', methods=['GET'])
    # def message(self, **params):
    #     #data = request.form
    #     pusher.trigger(u'message', u'send', {
    #         u'name': 'viki',
    #         u'message': 'hallo'
    #     })
    #     return "message sent"
        
    # @http.route('''/home''',type='http', auth='public', website=True)
    # def home(self, **params):
    #     url = ' '
    #     return http.request.redirect(url)

    @http.route('''/''',type='http', auth='public', website=True)
    def home(self, **params):
        url = '/formpertanyaan'
        return http.request.redirect(url)
        
    # @http.route('''/admin''',type='http', auth='public', website=True)
    # def admin(self, **params):
    #     url = '/web/login'
    #     return http.request.redirect(url)

    @http.route('''/register''',type='http', auth='public', website=True)
    def register(self, **params):
        return request.render("erups_question.register", {})

    @http.route('''/login''',type='http',auth='public', website=True)
    def login(self, **params):
        return request.render("erups_question.login", {})

    @http.route('''/resetpassword''',type='http',auth='public', website=True)
    def resetpassword(self, **params):
        return request.render("erups_question.resetpassword", {})
    
    @http.route('''/user''',type='http',auth='public', website=True)
    def user(self, **params):
        return request.render("erups_question.user", {})

    @http.route('''/pemegangsaham''',type='http',auth='public', website=True)
    def pemegangsaham(self, **params):
        return request.render("erups_question.pemegangsaham", {})

    @http.route('''/thanks''',type='http', auth='public', website=True)
    def thanks(self, **params):
        return request.render("erups_question.thanks", {})

    @http.route('''/thanks_langsung''',type='http', auth='public', website=True)
    def thanks_langsung(self, **params):
        return request.render("erups_question.thanks_langsung", {})

    @http.route('''/thanks_online''',type='http', auth='public', website=True)
    def thanks_online(self, **params):
        return request.render("erups_question.thanks_online", {})

    @http.route('''/pertanyaan''',type='http', auth='public', website=True)
    def admin(self, **params):
        url = '/formpertanyaan'
        return http.request.redirect(url)

    @http.route(['''/formpertanyaan''', '''/formpertanyaan/<int:erups_id>'''], auth='public', website=True)
    def index(self, erups_id=None, **params):
        
        sql2 = "SELECT * FROM erups_question eq LEFT JOIN erups_agenda ea ON ea.id = eq.agenda_id WHERE ea.status = 'open';"
        request.env[self._model_erups_question].sudo()._cr.execute(sql2)
        questioncheck = request.cr.fetchall()
        
        sql3 = "SELECT * FROM erups_agenda WHERE status = 'open';"
        request.env[self._model_erups_question].sudo()._cr.execute(sql3)
        agendacheck = request.cr.fetchall()
        
        if erups_id == None:
            erups = http.request.env[self._model_erups].sudo().search([])
            values = {
                "erups": erups,
                "message": len(agendacheck),
            }
            print(erups)
            return http.request.render('erups_question.erups', values)
        else:
            sql1 = "SELECT * FROM erups WHERE id = '%s';" % (erups_id)
            request.env[self._model_erups_question].sudo()._cr.execute(sql1)
            res = request.cr.fetchall()
            if len(res) > 0:
                erups = http.request.env[self._model_erups].sudo().search(
                    [('id', '=', erups_id)])
                agenda = http.request.env[self._model_erups_agenda].sudo().search(
                    [('erups_id', '=', erups_id),('status', '=', 'open')],order='id asc')
                
                if erups.status == 'close':
                    url = '/formpertanyaan/'
                    return http.request.redirect(url)
                else:
                    values = {
                        "erups": erups,
                        "agenda": agenda,
                        "message": len(questioncheck),
                    }
                    print(erups)
                    return http.request.render('erups_question.form_question', values)
            else:
                values = {
                    "message":  'Kegiatan tidak ditemukan',
                }
                return http.request.render('erups_question.pagenotfound',values)

    @http.route(['/formpertanyaan/save'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def rups_save(self, **post):

        rups_id = post['rups_id']
        
        data = {
            "registration_number": post['registration_number'],
            "email": post['email'],
            "name": post['name'],
            "authority_holder": post['authority_holder'],
            "share_count": post['share_count'],
            "agenda_id": post['agenda_id'],
            # "agenda_id": '2',
            "question": post['question'],
        }
        
        # filter_ar = [
        #     ('registration_number', '=', post['registration_number']),
        #     ('agenda_id', '=', post['agenda_id']),
        # ]
        # records = request.env[self._model_erups_question].sudo().search_count(filter_ar)
        sql1 = "SELECT * FROM erups_question WHERE registration_number = '%s' AND agenda_id = '%s';" % (data['registration_number'],data['agenda_id'])
        request.env[self._model_erups_question].sudo()._cr.execute(sql1)
        res_one = request.cr.fetchall()
         #json.dumps(res_one)
        sql2 = "SELECT * FROM erups_question WHERE agenda_id = '%s';" % (data['agenda_id'])
        request.env[self._model_erups_question].sudo()._cr.execute(sql2)
        questioncheck = request.cr.fetchall()
        
        sql3 = "SELECT * FROM erups_agenda WHERE id = '%s' AND status = '%s' ;" % (data['agenda_id'],'open')
        request.env[self._model_erups_question].sudo()._cr.execute(sql3)
        agendacheck = request.cr.fetchall()
        
        if len(questioncheck) >= 10:
            values = {
                "message":  'Jumlah Penanya sudah mencapai batas sebanyak 10 (sepuluh) Penanya per sesi',
            }
            return http.request.render('erups_question.messagepage',values)
        else:
            # if len(res_one) > 0:
            #     values = {
            #         "message":  'Pemegang Saham hanya bisa mengajukan Satu Pertanyaan per Agenda',
            #     }
            #     return http.request.render('erups_question.warningpage',values)
            #     # raise exceptions.ValidationError(
            #     #     "Pemegang Saham hanya bisa mengajukan Satu Pertanyaan per Agenda"
            #     # )
            # else:
            if len(agendacheck) > 0:
                rec_save = request.env[self._model_erups_question].sudo().create(data)
                if rec_save:
                    #return http.request.render('erups_question.terimakasih')
                    url = '/thankyou'
                    return http.request.redirect(url)
                else:
                    values = {
                        "message":  'Maaf, Gagal Menyimpan Data'
                    }
                    return http.request.render('erups_question.warningpage',values)
            else:
                values = {
                    "message":  'Agenda telah ditutup / Agenda telah selesai',
                }
                return http.request.render('erups_question.messagepage',values)

    @http.route(['''/evoting''', '''/evoting/<int:evoting_id>'''], auth='public', website=True)
    def index2(self, evoting_id=None, **params):
        
        sql2 = "SELECT * FROM erups_evoting eq LEFT JOIN erups_agenda ea ON ea.id = eq.agenda_id WHERE ea.status = 'open';"
        request.env[self._model_erups_evoting].sudo()._cr.execute(sql2)
        questioncheck = request.cr.fetchall()
        
        sql3 = "SELECT * FROM erups_agenda WHERE status = 'open';"
        request.env[self._model_erups_evoting].sudo()._cr.execute(sql3)
        agendacheck = request.cr.fetchall()
        
        if evoting_id == None:
            evoting = http.request.env[self._model_erups].sudo().search([])
            values = {
                "evoting": evoting,
                "message": len(agendacheck),
            }
            print(evoting)
            return http.request.render('erups_question.evoting', values)
        else:
            sql1 = "SELECT * FROM erups WHERE id = '%s';" % (evoting_id)
            request.env[self._model_erups_evoting].sudo()._cr.execute(sql1)
            res = request.cr.fetchall()
            if len(res) > 0:
                evoting = http.request.env[self._model_erups].sudo().search(
                    [('id', '=', evoting_id)])
                agenda = http.request.env[self._model_erups_agenda].sudo().search(
                    [('erups_id', '=', evoting_id),('status', '=', 'open')],order='id asc')
                
                if evoting.status == 'close':
                    url = '/evoting/'
                    return http.request.redirect(url)
                else:
                    values = {
                        "evoting": evoting,
                        "agenda": agenda,
                        "message": len(questioncheck),
                    }
                    print(evoting)
                    return http.request.render('erups_question.formevoting', values)
            else:
                values = {
                    "message":  'Kegiatan tidak ditemukan',
                }
                return http.request.render('erups_evoting.pagenotfound',values)

    @http.route('/thankyou', auth='public', methods=['GET'], website=True)
    def thankyou(self, **params):

        sql2 = "SELECT * FROM erups_question eq LEFT JOIN erups_agenda ea ON ea.id = eq.agenda_id WHERE ea.status = 'open';"
        request.env[self._model_erups_question].sudo()._cr.execute(sql2)
        questioncheck = request.cr.fetchall()
        
        #data = request.form
        pusher.trigger(u'message', u'send', {
            u'name': 'viki',
            u'message': len(questioncheck)
        })
        
        values = {
            'base_url': 'terimakasih telah mengisi pertanyaan',
        }
        return http.request.render('erups_question.terimakasih', values)

    @http.route('''/login_check''',type='http',auth='public',mothods=['POST'], website=True)
    def login_check(self, **post):

        data = {
            "email" : post['email'],
            "password" : post['password']
        }

        hashed = bcrypt.hashpw(post['password'].encode('utf-8'), bcrypt.gensalt())

        sql5 = "SELECT * FROM erups_registrasi WHERE email = '%s' ;"  % (data['email'])
        request.env[self._model_erups_registrasi].sudo()._cr.execute(sql5)
        user = request.cr.fetchall()
        
        if len(user) > 0 :
            if bcrypt.checkpw(post['password'].encode('utf-8'), hashed):
                url = '/formpertanyaan'
                return http.request.redirect(url)
            else:
                values = {
                    "message" : 'Password salah'
                }
                return request.render("erups_question.messagepage", values)
        else:
            values = {
                    "message" : 'Anda belum mendaftar'
                }
            return request.render("erups_question.messagepage", values)

    @http.route('''/reset_password''',type='http', auth='public',mothods=['POST','GET'], website=True)
    def reset_password(self, **post):

        passs=[]
        for i in range(3):
            alpha=random.choice(string.ascii_letters)
            numbers=random.choice(string.digits)
            passs.append(alpha)
            passs.append(numbers)

        v=("").join(str(x)for x in passs)

        sender_email = "prakmoklet27@gmail.com"
        password = "moklet12345"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = post['email']
        msg['Subject'] = "E-RUPS"
        # message = "Terima kasih telah melakukan registrasi.\nPassword : "+z

        body = "Password akun Anda telah diubah\n\nBerikut Password baru akun yang dapat Anda gunakan pada acara : \nRAPAT UMUM PEMEGANG SAHAM TAHUNAN BUKU 2020 PT TELEKOMUNIKASI INDONESIA TBK \n\nPassword : "+v+"\n\nSekian, Terima kasih"
        msg.attach(MIMEText(body, 'plain'))
        

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()

        hashed = bcrypt.hashpw(v.encode('utf-8'), bcrypt.gensalt())

        data = {
            "email" : post['email'],
            "password" : v
        }

        sql7 = "SELECT * FROM erups_registrasi WHERE email = '%s' ;"  % (data['email'])
        request.env[self._model_erups_registrasi].sudo()._cr.execute(sql7)
        user = request.cr.fetchall()

        if len(data) > 0 :
            sql6 = "UPDATE erups_registrasi SET password = '%s' WHERE email = '%s' ;" % (data['password'], data['email'])
            request.env[self._model_erups_registrasi].sudo()._cr.execute(sql6)
            if sql6 :
                server.sendmail(sender_email, post['email'], text)
                url = '/login'
                return http.request.redirect(url)
            else :
                values = {
                        "message":  'Maaf, Gagal Menyimpan Data'
                    }
                return http.request.render('erups_question.warningpage',values)
        else : 
            values = {
                        "message":  'Email tidak tersedia, harap registrasi terlebih dahulu'
                    }
            return http.request.render('erups_question.warningpage',values)

    @http.route('''/register/save''',type='http', auth='public',mothods=['POST'], website=True)
    def reg_save(self, **post):

        noreg=[]
        for i in range(5):
            numbers=random.choice(string.digits)    
            noreg.append(numbers)

        y="".join(str(x)for x in noreg)

        passs=[]
        for i in range(3):
            alpha=random.choice(string.ascii_letters)
            numbers=random.choice(string.digits)
            passs.append(alpha)
            passs.append(numbers)

        z="".join(str(x)for x in passs)

        data = {
            "no_sid" : post['no_sid'],
            "name" : post['name'],
            "email" : post['email'],
            "kehadiran" : post['kehadiran'],
            "pemegang_saham" : post['pemegang_saham'],
            "nomor_registrasi" : y,
            "password" : z
        }

        sender_email = "prakmoklet27@gmail.com"
        password = "moklet12345"
        msg = MIMEMultipart()
        msg1 = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = post['email']
        msg['Subject'] = "E-RUPS"
        msg1['From'] = sender_email
        msg1['To'] = post['email']
        msg1['Subject'] = "E-RUPS."
        # message = "Terima kasih telah melakukan registrasi.\nPassword : "+z

        body = "Halo "+post['name']+", \n\nTerima kasih telah melakukan pendaftaran dan menginformasikan kehadiran Anda\n\nBerikut Nomor Registrasi dan Password akun yang dapat Anda gunakan pada acara : \nRAPAT UMUM PEMEGANG SAHAM TAHUNAN BUKU 2020 PT TELEKOMUNIKASI INDONESIA TBK \n\nNomor registrasi : "+y+"\nPassword : "+z+"\n\nSekian, Terima kasih"
        body1 = "Halo "+post['name']+", \n\nTerima kasih telah melakukan pendaftaran dan menginformasikan kehadiran Anda\n\nBerikut Password akun yang dapat Anda gunakan untuk login pada acara : \nRAPAT UMUM PEMEGANG SAHAM TAHUNAN BUKU 2020 PT TELEKOMUNIKASI INDONESIA TBK \n\nPassword : " + z +"\n\nSekian, Terima kasih"
        msg.attach(MIMEText(body, 'plain'))
        msg1.attach(MIMEText(body1, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        text1 = msg1.as_string()

        sql7 = "SELECT * FROM erups_registrasi WHERE email = '%s' ;"  % (data['email'])
        request.env[self._model_erups_registrasi].sudo()._cr.execute(sql7)
        user = request.cr.fetchall()

        if len(user) > 0:
            values = {
                'message' : 'Anda sudah mendaftar menggunakan email ini'
            }
            return request.render("erups_question.messagepage", values)
        else :
            if post['kehadiran'] == '0':
                values = {
                    'message' : 'Pilih Kehadiran Anda'
                }
                return request.render("erups_question.messagepage", values)
            else:
                # if post['pilihan_suara'] == '0':
                #     values = {
                #     'message' : 'Pilih Suara Anda'
                #     }
                #     return request.render("erups_question.register", values)
                # else:
                    if post['kehadiran'] == 'langsung':
                        values = {
                            'message' : y
                        }
                        request.env['erups_registrasi'].sudo().create(data)
                        server.sendmail(sender_email, post['email'], text)
                        return request.render("erups_question.thanks_langsung", values)
                    else:
                        if post['kehadiran'] == 'online':
                            request.env['erups_registrasi'].sudo().create(data)
                            server.sendmail(sender_email, post['email'], text1)
                            url='/thanks_online'
                            return http.request.redirect(url)
                        else:
                            request.env['erups_registrasi'].sudo().create(data)
                            url='/Evoting'
                            return http.request.redirect(url)
                            

    # @http.route('''/thanks''',type='http', auth='public', website=True)
    # def thanks(self,erups_id=None,**params):
    #     return request.render("erups_question.thanks", {})

    @http.route('/viki', auth='public', methods=['GET'], website=True)
    def viki(self, **params):

        data = {
            # "rups_id": post['rups_id'],
            "registration_number": '123',
            "email": 'viki@email.com',
            "name": 'viki',
            "authority_holder": 'awds',
            "share_count": '10',
            "agenda_id": '2',
            # "agenda_id": '2',
            "question": '??',
        }
        
        sql = "SELECT * FROM erups_question WHERE registration_number = '%s' AND agenda_id = '%s';" % (data['registration_number'],data['agenda_id'])
        request.env[self._model_erups_question].sudo()._cr.execute(sql)
        res_one = request.cr.fetchall()
        #fetchone() will return the first element found as dictionary
        
        total_len = request.env[self._model_erups_question].browse([('registration_number', '=', '123'),('agenda_id', '=', '2')])
        
        filter_ar = [
            ['registration_number', '=', '123'],
            ['agenda_id', '=', '2']
        ]
        records = request.env[self._model_erups_question]
        records = records.sudo().search_count(filter_ar)
        
        #json.dumps(total_len)
        # if records > 0:
        #     values = {
        #         "message":  'Pemegang Saham hanya bisa mengajukan Satu Pertanyaan per Agenda',
        #     }
        #     return http.request.render('erups_question.erups',values)
        # else:
        #     res = request.env[self._model_erups_question].sudo().create(data)
        return http.Response(
            json.dumps(time.strftime("%a, %d %b %Y %H:%M:%S")),
            status=200,
            mimetype='application/json'
        )
            # if res:
            #     return http.request.render('erups_question.terimakasih')
            # else:
            #     values = {
            #         "message":  'Maaf, Gagal Menyimpan Data'
            #     }
            #     return http.request.render('erups_question.erups',values)

# class Erups_form_question(http.Controller):

#     def __init__(self):
#         self._model_erups = "erups"
#         self._model_erups_agenda = "erups_agenda"

#     @http.route('/formpertanyaan/<int:erups_id>', auth='public', website=True)
#     def index(self, erups_id=None, **params):

#         erups = http.request.env[self._model_erups].sudo().search(
#             [('id', '=', erups_id)])
#         agenda = http.request.env[self._model_erups_agenda].sudo().search(
#             [('erups_id', '=', erups_id)])
#         values = {
#             "erups": erups,
#             "agenda": agenda,
#         }
#         print(erups)
#         return http.request.render('erups_question.form_question', values)

#     @http.route('/erups_question/erups_question/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('erups_question.listing', {
#             'root': '/erups_question/erups_question',
#             'objects': http.request.env['erups_question.erups_question'].search([]),
#         })

#     @http.route('/erups_question/erups_question/objects/<model("erups_question.erups_question"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('erups_question.object', {
#             'object': obj
#         })

