# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)
    
    payment_mode = fields.Selection([
        ("own_account", "Employee (to reimburse)"),
        ("company_account", "Employee (to justify)")
    ])
    is_rfq = fields.Boolean(string='Demande Achat', default=False,)
    employee_id = fields.Many2one(string='Beneficiaire')
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange',
                    default=_get_default_requested_by)
    journal_id = fields.Many2one('account.journal', string="Journal", 
                                 default=lambda self: self.env['account.journal'].search([('type', '=', 'cash')], limit=1)
                                )
    purchase_request = fields.Many2one('purchase.request', string="N° de D.A")
    
    @api.onchange('purchase_request')
    def _onchange_purchase_request(self):
        if self.purchase_request:
            self.analytic_account_id = self.purchase_request.project_code.analytic_account_id.id 