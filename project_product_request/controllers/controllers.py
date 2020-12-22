# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectProductRequest(http.Controller):
#     @http.route('/project_product_request/project_product_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_product_request/project_product_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_product_request.listing', {
#             'root': '/project_product_request/project_product_request',
#             'objects': http.request.env['project_product_request.project_product_request'].search([]),
#         })

#     @http.route('/project_product_request/project_product_request/objects/<model("project_product_request.project_product_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_product_request.object', {
#             'object': obj
#         })
