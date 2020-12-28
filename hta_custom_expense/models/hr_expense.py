# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)
    
    payment_mode = fields.Selection(selection_add=[('employee', 'To justify')])
    is_rfq = fields.Boolean(string='Demande Achat', default=False,)
    employee_id = fields.Many2one(string='Destinataire')
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange',
                    default=_get_default_requested_by)
    journal_id = fields.Many2one('account.journal', string="Journal")
    purchase_request = fields.Many2one('purchase.request', string="N° de D.A")