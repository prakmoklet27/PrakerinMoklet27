from odoo import models,fields

class Course(models.Model):
    _name = 'frankynew.course'
    _description = 'Data course'

    name = fields.Char(
        string='Course Name',
        required=True,
        help="Fill course name..."
    )

    description = fields.Text(
        string='Description',
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )