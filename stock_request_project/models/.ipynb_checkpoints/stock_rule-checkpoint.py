# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class stock_request_project(models.Model):
#     _name = 'stock_request_project.stock_request_project'
#     _description = 'stock_request_project.stock_request_project'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
