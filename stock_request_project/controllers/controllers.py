# -*- coding: utf-8 -*-
# from odoo import http


# class StockRequestProject(http.Controller):
#     @http.route('/stock_request_project/stock_request_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_request_project/stock_request_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_request_project.listing', {
#             'root': '/stock_request_project/stock_request_project',
#             'objects': http.request.env['stock_request_project.stock_request_project'].search([]),
#         })

#     @http.route('/stock_request_project/stock_request_project/objects/<model("stock_request_project.stock_request_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_request_project.object', {
#             'object': obj
#         })
