# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import string

class Emitten(models.Model):
    _name = "erups_emitten"

    id = fields.Many2one('erups_emitten', ondelete='cascade', required=True)
    name = fields.Char(string='Emitten', required=True)
    agenda_ids = fields.One2many('erups_agenda', 'erups_id')
    # kegiatan_ids = fields.One2many('erups', 'erups_id')

    total_kegiatan = fields.Integer('Jumlah Kegiatan', compute='_compute_total_kegiatan')
    total_agenda = fields.Integer('Jumlah Agenda', compute='_compute_total_agenda')

    # @api.depends('kegiatan_ids')
    # def _compute_total_kegiatan(self):
    #     for r in self:
    #         if r.agenda_ids:
    #             r.total_kegiatan = len(r.agenda_ids)
    #         else:
    #             r.total_kegiatan = 0

    @api.depends('agenda_ids')
    def _compute_total_agenda(self):
        for r in self:
            if r.agenda_ids:
                r.total_agenda = len(r.agenda_ids)
            else:
                r.total_agenda = 0

class Erups(models.Model):
    _name = 'erups'

    id_k = fields.Many2one('erups', ondelete='cascade', required=True)
    emitten_id = fields.Many2one('erups_emitten', ondelete='cascade', required=True)
    name = fields.Char(string='Kegiatan',required=True)
    kegiatan_num = fields.Integer(string='No Urut')
    event_date = fields.Date(string='Tanggal Event')
    location = fields.Text(string='Lokasi Event')
    agenda_ids = fields.One2many('erups_agenda', 'erups_id')
    description = fields.Text()
    status = fields.Selection([('open', 'Open'), ('close', 'Closed')], required=True, default="open")

    total_kegiatan = fields.Integer('Jumlah Kegiatan', compute='_compute_total_kegiatan')
    total_agenda = fields.Integer('Jumlah Agenda', compute='_compute_total_agenda')
    total_question = fields.Integer('Jumlah Pertanyaan', compute='_compute_total_question')
    total_question_valid = fields.Integer('Jumlah Pertanyaan Valid', compute='_compute_total_valid')
    total_question_relevan = fields.Integer('Jumlah Pertanyaan Relevan', compute='_compute_total_relevan')
    total_question_verified = fields.Integer('Jumlah Pertanyaan Dipilih', compute='_compute_total_verified')

    total_consultant_relevan = fields.Integer('Jumlah Pertanyaan Konsultan Relevan', compute='_compute_total_consultant_relevan')
    total_consultant_not_relevan = fields.Integer('Jumlah Pertanyaan Konsultan Not Relevan',
                                           compute='_compute_total_consultant_not_relevan')

    # total_question_relevan = fields.Integer('Jumlah Pertanyaan Valid dan Relevan', compute='_compute_total_relevan')
    # total_question_verified = fields.Integer('Jumlah Pertanyaan Dipilih', compute='_compute_total_verified')

    # complete_name = fields.Char("Agenda Full Name", compute='_compute_complete_name', store=True)
    num_name = fields.Char("Kegiatan Name", compute='_compute_num_name', store=True)

    relevan_question_ids = fields.One2many('erups_question', 'agenda_id', domain=[('status', 'in', ['consultant', 'speaker'])])
    speaker_question_ids = fields.One2many('erups_question', 'agenda_id', domain=[('status', 'in', ['speaker'])])

    active_agenda = fields.Integer(compute='_compute_active_agenda')

    agenda_num_text = fields.Char(compute='_compute_num_to_text')

    @api.depends('agenda_ids')
    def _compute_total_agenda(self):
        for r in self:
            if r.agenda_ids:
                r.total_agenda = len(r.agenda_ids)
            else:
                r.total_agenda = 0


    @api.depends('agenda_ids')
    def _compute_total_question(self):
        for r in self:
            if r.agenda_ids:
                for a in r.agenda_ids:
                    r.total_question += len(a.question_ids)
            else:
                r.total_question = 0

    @api.depends('agenda_ids')
    def _compute_total_valid(self):
        for r in self:
            r.total_question_valid = 0
            if r.agenda_ids:
                for a in r.agenda_ids:
                    if a.question_ids:
                        for q in a.question_ids:
                            if q.status not in ['shareholder', 'bae_reject']:
                                r.total_question_valid += 1

    @api.depends('agenda_ids')
    def _compute_total_relevan(self):
        for r in self:
            r.total_question_relevan = 0
            if r.agenda_ids:
                for a in r.agenda_ids:
                    if a.question_ids:
                        for q in a.question_ids:
                            if q.status in ['consultant', 'speaker']:
                                r.total_question_relevan += 1


    @api.depends('agenda_ids')
    def _compute_total_verified(self):
        for r in self:
            if r.agenda_ids:
                for a in r.agenda_ids:
                    r.total_question_verified = a.search_count([['question_ids.status', '=', 'speaker']])
            else:
                r.total_question_verified = 0


class Agenda(models.Model):
    _name = 'erups_agenda'
    # _rec_name = 'complete_name'

    name = fields.Char(string='Nama Agenda', required=True)
    agenda_num = fields.Integer(string='No Urut')
    description = fields.Text()
    erups_id = fields.Many2one('erups', ondelete='cascade', required=True)
    status = fields.Selection([('open', 'Open'), ('close', 'Closed'), ('done', 'Done')], required=True, default="open")

    question_ids = fields.One2many('erups_question', 'agenda_id')
    total_question = fields.Integer('Jumlah Pertanyaan', compute='_compute_total_question')
    total_question_valid = fields.Integer('Jumlah Pertanyaan Valid', compute='_compute_total_valid')
    total_question_not_valid = fields.Integer('Jumlah Pertanyaan Tidak Valid', compute='_compute_total_not_valid')

    # total_notaris_relevan = fields.Integer('Jumlah Pertanyaan Notaris Relevan', compute='_compute_total_notaris_relevan')
    # total_notaris_not_relevan = fields.Integer('Jumlah Pertanyaan Notaris Not Relevan',
    #                                        compute='_compute_total_notaris_not_relevan')

    total_consultant_relevan = fields.Integer('Jumlah Pertanyaan Konsultan Relevan', compute='_compute_total_consultant_relevan')
    total_consultant_not_relevan = fields.Integer('Jumlah Pertanyaan Konsultan Not Relevan',
                                           compute='_compute_total_consultant_not_relevan')

    total_question_relevan = fields.Integer('Jumlah Pertanyaan Valid dan Relevan', compute='_compute_total_relevan')
    total_question_verified = fields.Integer('Jumlah Pertanyaan Dipilih', compute='_compute_total_verified')

    complete_name = fields.Char("Agenda Full Name", compute='_compute_complete_name', store=True)
    num_name = fields.Char("Agenda Name", compute='_compute_num_name', store=True)

    relevan_question_ids = fields.One2many('erups_question', 'agenda_id', domain=[('status', 'in', ['consultant', 'speaker'])])
    speaker_question_ids = fields.One2many('erups_question', 'agenda_id', domain=[('status', 'in', ['speaker'])])

    active_agenda = fields.Integer(compute='_compute_active_agenda')

    agenda_num_text = fields.Char(compute='_compute_num_to_text')

    @api.depends('agenda_num')
    def _compute_active_agenda(self):
        ErupsAgenda = self.env['erups_agenda'].sudo().search([('status', 'not in', ['done'])], order='agenda_num', limit=1)
        first_agenda_open = ErupsAgenda.agenda_num

        for r in self:
            r.active_agenda = first_agenda_open

    @api.depends('agenda_num')
    def _compute_num_to_text(self):
        for r in self:
            if r.agenda_num == 1:
                r.agenda_num_text = "Pertama"
            if r.agenda_num == 2:
                r.agenda_num_text = "Kedua"
            if r.agenda_num == 3:
                r.agenda_num_text = "Ketiga"
            if r.agenda_num == 4:
                r.agenda_num_text = "Keempat"
            if r.agenda_num == 5:
                r.agenda_num_text = "Kelima"
            if r.agenda_num == 6:
                r.agenda_num_text = "Keenam"



    @api.depends('question_ids')
    def _compute_total_question(self):
        for r in self:
            if r.question_ids:
                r.total_question = len(r.question_ids)
            else:
                r.total_question = 0

    @api.depends('question_ids')
    def _compute_total_valid(self):
        for r in self:
            r.total_question_valid = 0
            if r.question_ids:
                for q in r.question_ids:
                    if q.status not in ['shareholder', 'bae_reject']:
                        r.total_question_valid += 1
            else:
                r.total_question_valid = 0

    @api.depends('question_ids')
    def _compute_total_not_valid(self):
        for r in self:
            r.total_question_not_valid = 0
            if r.question_ids:
                for q in r.question_ids:
                    if q.status in ['bae_reject', 'shareholder']:
                        r.total_question_not_valid += 1

    @api.depends('question_ids')
    def _compute_total_notaris_relevan(self):
        for r in self:
            r.total_notaris_relevan = 0
            if r.question_ids:
                for q in r.question_ids:
                    if q.status == 'notaris':
                        r.total_notaris_relevan += 1

    @api.depends('question_ids')
    def _compute_total_notaris_not_relevan(self):
        for r in self:
            r.total_notaris_not_relevan = 0
            if r.question_ids:
                for q in r.question_ids:
                    if q.status == 'notaris_reject':
                        r.total_notaris_not_relevan += 1

    @api.depends('question_ids')
    def _compute_total_consultant_relevan(self):
        for r in self:
            r.total_consultant_relevan = 0
            if r.question_ids:
                for q in r.question_ids:
                    if q.status in ['consultant', 'speaker']:
                        r.total_consultant_relevan += 1

    @api.depends('question_ids')
    def _compute_total_consultant_not_relevan(self):
        for r in self:
            r.total_consultant_not_relevan = 0
            if r.question_ids:
                for q in r.question_ids:
                    if q.status in ['consultant_reject', 'bae']:
                        r.total_consultant_not_relevan += 1

    @api.depends('question_ids')
    def _compute_total_relevan(self):
        for r in self:
            r.total_question_relevan = 0
            if r.question_ids:
                for q in r.question_ids:
                    if q.status in ['consultant', 'speaker']:
                        r.total_question_relevan += 1
            else:
                r.total_question_relevan = 0


    @api.depends('question_ids')
    def _compute_total_verified(self):
        for r in self:
            if r.question_ids:
                for q in r.question_ids:
                    if q.status == 'speaker':
                        r.total_question_verified += 1
            else:
                r.total_question_verified = 0


    @api.depends('name', 'agenda_num')
    def _compute_complete_name(self):
        for r in self:
            if r.agenda_num:
                r.complete_name = 'Agenda %s - %s' % (r.agenda_num, r.name)
            else:
                r.complete_name = r.name

    @api.depends('name', 'agenda_num')
    def _compute_num_name(self):
        for r in self:
            if r.agenda_num:
                r.num_name = 'Agenda %s' % (r.agenda_num)
            else:
                r.num_name = r.name

    # @api.onchange('status')
    # def _onchange_status(self):
    #     print('merdeka', self)
    #     if self.status == 'open':
    #         agenda_open = self.env['erups_agenda'].sudo().search([('status', '=', 'open')])
    #         agenda_open.sudo().write({'status': 'close'})
    #
    #         self.sudo().write({'status': 'open'})

    def open_agenda(self):
        agenda_open = self.env['erups_agenda'].sudo().search([('status', '=', 'open')])
        agenda_open.sudo().write({'status': 'close'})

        for r in self:
            r.sudo().write({'status': 'open'})

        return True

    def close_agenda(self):
        for r in self:
            r.sudo().write({'status': 'close'})

        return True

    def done_agenda(self):
        for r in self:
            r.sudo().write({'status': 'done'})

        return True

class Shareholders(models.Model):
    _name = "erups_shareholders"

    name = fields.Char(string='Shareholders', required=True)
    alamat = fields.Char(string='Alamat', required=True)
    saham = fields.Char(string='Jumlah Saham', required=True)

class Question(models.Model):
    _name = 'erups_question'

    registration_number = fields.Char(required=True)
    name = fields.Char(string='Nama Pemegang Saham', required=True)
    authority_holder = fields.Char(string='Nama Pemegang Kuasa')
    share_count = fields.Float(string='Jumlah Saham')
    agenda_id = fields.Many2one('erups_agenda', ondelete='cascade', required=True)
    question = fields.Text(string='Pertanyaan')
    email = fields.Char()

    status = fields.Selection([('shareholder', 'Open'), ('bae', 'Verified by BAE'), ('bae_reject', 'Not Valid'),
                               ('notaris', 'Verified by Notaris'), ('notaris_reject', 'Not Relevan by Notaris'),
                               ('consultant', 'Verified by Consultant'), ('consultant_reject', 'Not Relevan by Consultant'),
                               ('speaker', 'Selected by Speaker'), ('speaker_reject', 'Not Selected')],
                            required=True, default="shareholder")

    erups = fields.Char(related='agenda_id.erups_id.name')
    agenda_full_name = fields.Char(related='agenda_id.complete_name')
    agenda_num_name = fields.Char(related='agenda_id.num_name')

    # _sql_constraints = [
    #     ('name_uniq', 'unique (registration_number, agenda_id)', 'Pemegang Saham hanya bisa mengajukan Satu Pertanyaan per Agenda')
    # ]

    def bae_confirm(self):
        for r in self:
            if r.status not in ['shareholder']:
                continue

            r.sudo().write({'status': 'bae'})

        return True

    def bae_reject(self):
        for r in self:
            if r.status not in ['shareholder']:
                continue

            r.sudo().write({'status': 'bae_reject'})

        return True

    def notaris_confirm(self):
        for r in self:
            if r.status not in ['bae']:
                continue

            r.sudo().write({'status': 'notaris'})

        return True

    def notaris_reject(self):
        for r in self:
            if r.status not in ['bae']:
                continue

            r.sudo().write({'status': 'notaris_reject'})

        return True

    def consultant_confirm(self):
        for r in self:
            if r.status not in ['bae']:
                continue

            r.sudo().write({'status': 'consultant'})

        return True

    def consultant_reject(self):
        for r in self:
            if r.status not in ['bae']:
                continue

            r.sudo().write({'status': 'consultant_reject'})

        return True

    def speaker_confirm(self):
        for r in self:
            if r.status not in ['consultant']:
                continue

            r.sudo().write({'status': 'speaker'})

        return True

    def speaker_reject(self):
        for r in self:
            if r.status not in ['speaker']:
                continue

            r.sudo().write({'status': 'consultant'})

        return True

class Evoting(models.Model):
    _name = "erups_evoting"

    agenda_id = fields.Many2one('erups_agenda', ondelete='cascade', required=True)
    pilihan_suara = fields.Selection([('setuju','1'),
                                ('tidak_setuju','2'),('abstain','3')
                                ],string='Pilihan Suara', required=True) 
                                

class Registrasi(models.Model):
    _name = "erups_registrasi"

    emitten_id = fields.Many2one('erups_emitten', ondelete='cascade', required=True)
    erups_id = fields.Many2one('erups', ondelete='cascade', required=True)
    
    tipe_registrasi = fields.Selection([('perorangan','1'),
                                ('individu','2')],
                                string='Tipe Registrasi', required=True)
    no_sid = fields.Char(string='NO.SID',required=True)
    no_ktp = fields.Char(string='NO.KTP', required=True)
    name = fields.Char(string='Nama Pemegang Saham', required=True)
    alamat = fields.Char(string='Alamat', required=True)
    jumlah_saham = fields.Char(string='Jumlah Saham', required=True)
    no_mobile = fields.Char(string='NO.Mobile', required=True)
    email = fields.Char(string='Email', required=True)
    kehadiran = fields.Selection([('0',''),('langsung','1'),
                                ('online','2'),('perwakilan','3')],
                                string='Kehadiran', required=True)
    penerima_kuasa = fields.Char()
    noktp = fields.Char()
    nomobel = fields.Char()
    myfile = fields.Char()
    nomor_registrasi = fields.Char() 
    password = fields.Char()
    # role = fields.Selection([('user','User'),('admin','Admin')],string='Role', required=True)

