# -*- coding: utf-8 -*-
# from odoo import http


# class ExpenseApps(http.Controller):
#     @http.route('/expense_apps/expense_apps/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expense_apps/expense_apps/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('expense_apps.listing', {
#             'root': '/expense_apps/expense_apps',
#             'objects': http.request.env['expense_apps.expense_apps'].search([]),
#         })

#     @http.route('/expense_apps/expense_apps/objects/<model("expense_apps.expense_apps"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expense_apps.object', {
#             'object': obj
#         })
