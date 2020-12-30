# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomHr(http.Controller):
#     @http.route('/hta_custom_hr/hta_custom_hr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_hr/hta_custom_hr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_hr.listing', {
#             'root': '/hta_custom_hr/hta_custom_hr',
#             'objects': http.request.env['hta_custom_hr.hta_custom_hr'].search([]),
#         })

#     @http.route('/hta_custom_hr/hta_custom_hr/objects/<model("hta_custom_hr.hta_custom_hr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_hr.object', {
#             'object': obj
#         })
