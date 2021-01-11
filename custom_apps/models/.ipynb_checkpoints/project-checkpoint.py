# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


# class custom_apps(models.Model):
#     _name = 'custom_apps.custom_apps'
#     _description = 'custom_apps.custom_apps'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Project(models.Model):
    _inherit = "project.project"
    
    sale_order_ids = fields.One2many("sale.order", "project_id", string="Sale Orders")
    #purchase_order_lines = fields.One2many("purchase.order.line", "project_id", string="Purchase Orders")
    
    project_code_sequence_id = fields.Many2one(comodel_name='ir.sequence', string='Code Sequence Id', ondelete='cascade')
    project_code = fields.Char(string='Code Projet', required=True, readonly=True, copy=False, default= lambda self: _('New'))
    
    #Create method to compute project_code from id like P%year/0000 + id
    @api.model
    def create(self, vals):
        # Prevent double project creation
        if vals.get('project_code', _('New')) == _('New'):
            self = self.with_context(mail_create_nosubscribe=True)
            vals['project_code'] = self.env['ir.sequence'].next_by_code('project.code.sequence') or _('New')
            project = super(Project, self).create(vals)
            if not vals.get('subtask_project_id'):
                project.subtask_project_id = project.id
            if project.privacy_visibility == 'portal' and project.partner_id:
                project.message_subscribe(project.partner_id.ids)
        return project
    