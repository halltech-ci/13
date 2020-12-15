# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectStockRequest(http.Controller):
#     @http.route('/project_stock_request/project_stock_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_stock_request/project_stock_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_stock_request.listing', {
#             'root': '/project_stock_request/project_stock_request',
#             'objects': http.request.env['project_stock_request.project_stock_request'].search([]),
#         })

#     @http.route('/project_stock_request/project_stock_request/objects/<model("project_stock_request.project_stock_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_stock_request.object', {
#             'object': obj
#         })
