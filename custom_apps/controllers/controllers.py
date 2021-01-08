# -*- coding: utf-8 -*-
# from odoo import http


# class CustomApps(http.Controller):
#     @http.route('/custom_apps/custom_apps/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_apps/custom_apps/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_apps.listing', {
#             'root': '/custom_apps/custom_apps',
#             'objects': http.request.env['custom_apps.custom_apps'].search([]),
#         })

#     @http.route('/custom_apps/custom_apps/objects/<model("custom_apps.custom_apps"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_apps.object', {
#             'object': obj
#         })
