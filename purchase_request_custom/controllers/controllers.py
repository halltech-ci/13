# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseRequestCustom(http.Controller):
#     @http.route('/purchase_request_custom/purchase_request_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_request_custom/purchase_request_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_request_custom.listing', {
#             'root': '/purchase_request_custom/purchase_request_custom',
#             'objects': http.request.env['purchase_request_custom.purchase_request_custom'].search([]),
#         })

#     @http.route('/purchase_request_custom/purchase_request_custom/objects/<model("purchase_request_custom.purchase_request_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_request_custom.object', {
#             'object': obj
#         })
