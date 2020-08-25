# -*- coding: utf-8 -*-
# from odoo import http


# class ModuleBaru(http.Controller):
#     @http.route('/module_baru/module_baru/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/module_baru/module_baru/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('module_baru.listing', {
#             'root': '/module_baru/module_baru',
#             'objects': http.request.env['module_baru.module_baru'].search([]),
#         })

#     @http.route('/module_baru/module_baru/objects/<model("module_baru.module_baru"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('module_baru.object', {
#             'object': obj
#         })
