# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'
    
    amount_advance = fields.Monetary(string="Advanced Amount", 
                                     compute="_compute_advance_amount"
                                    )
    justify_amount = fields.Monetary(string="Justified Amount")
    amount_residual = fields.Monetary(string="Residual Amount", 
                                      compute="_compute_residual_amount", 
                                      readonly=True
                                     )
    assigned_to = fields.Many2one('hr.employee', string="Destinataire")
    employee_id = fields.Many2one("hr.employee", string="Beneficiaire")
    
    '''journal_id = fields.Many2one('account.journal', string='Expense Journal', states={'done': [('readonly', True)], 'post': [('readonly', True)]}, check_company=True, domain="[('type', '=', 'purchase'), ('company_id', '=', company_id)]",
        default=_default_journal_id, help="The journal used when the expense is done.")
    bank_journal_id = fields.Many2one('account.journal', string='Bank Journal', states={'done': [('readonly', True)], 'post': [('readonly', True)]}, check_company=True, domain="[('type', 'in', ['cash', 'bank']), ('company_id', '=', company_id)]",
        default=_default_bank_journal_id, help="The payment method used when the expense is paid by the company.")
    '''#journal_id = fields.Many2one('account.journal')
    
    @api.depends('expense_line_ids')
    def _compute_advance_amount(self):
        sum_amount = 0.0
        for sheet in self:
            lines = self.expense_line_ids.filtered(lambda e:e.payment_mode == 'company_account')
            if lines:
                for line in lines:
                    amount = line.total_amount
                    sum_amount += amount 
            self.amount_advance = sum_amount
    
    @api.depends('amount_advance', 'total_amount')
    def _compute_residual_amount(self):
        for sheet in self:
            self.amount_residual = self.total_amount - self.justify_amount
    
    @api.onchange('justify_amount')
    def onchange_justify_amount(self):
        self.amount_residual = self.total_amount - self.justify_amount
    
    