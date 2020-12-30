# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectMoveRequest(http.Controller):
#     @http.route('/project_move_request/project_move_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_move_request/project_move_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_move_request.listing', {
#             'root': '/project_move_request/project_move_request',
#             'objects': http.request.env['project_move_request.project_move_request'].search([]),
#         })

#     @http.route('/project_move_request/project_move_request/objects/<model("project_move_request.project_move_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_move_request.object', {
#             'object': obj
#         })
