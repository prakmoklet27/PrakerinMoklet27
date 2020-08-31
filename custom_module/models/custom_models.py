from odoo import models,fields

class CustomModel(models.Model):
    _name = 'custom.model'

    name = fields.Char(string='Name')