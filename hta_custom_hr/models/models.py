# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hta_custom_hr(models.Model):
#     _name = 'hta_custom_hr.hta_custom_hr'
#     _description = 'hta_custom_hr.hta_custom_hr'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
