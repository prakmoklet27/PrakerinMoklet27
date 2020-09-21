# -*- coding: utf-8 -*-
{
    'name': "Tanya Jawab RUPS",
    'summary': "Tanya Jawab RUPS",
    'author': "Sigma, Lutfi Nailufar Nurdin",
    'website': "http://sigma.co.id",
    'category': 'RUPS',
    'version': '13.0.1.0.0',

    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/views.xml',
        'views/templates.xml',
        'security/menu.xml',
    ],
    'application': True,
    'installable': True,
    'auto-install': True,
}
