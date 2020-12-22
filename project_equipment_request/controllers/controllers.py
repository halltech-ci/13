# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectEquipmentRequest(http.Controller):
#     @http.route('/project_equipment_request/project_equipment_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_equipment_request/project_equipment_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_equipment_request.listing', {
#             'root': '/project_equipment_request/project_equipment_request',
#             'objects': http.request.env['project_equipment_request.project_equipment_request'].search([]),
#         })

#     @http.route('/project_equipment_request/project_equipment_request/objects/<model("project_equipment_request.project_equipment_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_equipment_request.object', {
#             'object': obj
#         })
