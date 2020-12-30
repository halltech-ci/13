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
    project_code = fields.Many2one('project.project' ,related='sale_order.project_id', string="Project", readonly=True)
    purchase_type = fields.Selection(selection=[('project', 'Projet'), ('autres', 'Autres')], string="Request Type")
    has_manager = fields.Boolean(compute='_compute_has_manager')
    is_project_approver = fields.Boolean(compute='_compute_is_project_approver')
    is_expense = fields.Boolean('is_expense', default=False)
    
    def action_send_email(self):
        self.ensure_one()
        template_id = self.env.ref('purchase_request.email_template_purchase_request').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
    
    @api.model
    def create(self, vals):
        request = super(PurchaseRequest, self).create(vals)
        if vals.get("assigned_to"):
            partner_id = self._get_partner_id(request)
            request.message_subscribe(partner_ids=[partner_id])
            self.action_send_email()
        return request

    
class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"
    
    project = fields.Many2one(related="request_id.project_code", string="Project", readonly=True)
    product_code = fields.Char(related="product_id.default_code", sting="Code Article")