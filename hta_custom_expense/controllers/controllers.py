# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomExpense(http.Controller):
#     @http.route('/hta_custom_expense/hta_custom_expense/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_expense/hta_custom_expense/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_expense.listing', {
#             'root': '/hta_custom_expense/hta_custom_expense',
#             'objects': http.request.env['hta_custom_expense.hta_custom_expense'].search([]),
#         })

#     @http.route('/hta_custom_expense/hta_custom_expense/objects/<model("hta_custom_expense.hta_custom_expense"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_expense.object', {
#             'object': obj
#         })
