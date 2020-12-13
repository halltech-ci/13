# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"
    
    @api.depends('requested_by')
    def _compute_has_manager(self):
        for rec in self:
            if rec.requested_by:
                employee = self.env['hr.employee'].search([('work_email', '=', rec.requested_by.email)], limit = 1)
                if (employee.department_id) and (employee.department_id.manager_id):
                    rec.has_manager = True
                else:
                    rec.has_manager = False
    
    def _compute_is_project_approver(self):
        for rec in self:
            if self._compute_has_manager():
                if (self.env['hr.employee'].search([('project_apporver', '=', True)])).exists():
                    rec.is_project_apporver = True
                else:
                    rec.is_project_approver = False
    sale_order = fields.Many2one('sale.order', string='Sale Order')
    project_code = fields.Char(related='sale_order.project_code', string="Project", readonly=True)
    purchase_type = fields.Selection(selection=[('project', 'Projet'), ('autres', 'Autres')], string="Request Type")
    has_manager = fields.Boolean(compute='_compute_has_manager')
    is_project_approver = fields.Boolean(compute='_compute_is_project_approver')