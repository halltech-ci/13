# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero


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
    
    journal_id = fields.Many2one('account.journal', string='Expense Journal', 
                    states={'done': [('readonly', True)], 'post': [('readonly', True)]},
                    check_company=True, help="The journal used when the expense is done.")
    
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
    
    def action_sheet_move_create(self):
        if any(sheet.state != 'approve' for sheet in self):
            raise UserError(_("You can only generate accounting entry for approved expense(s)."))

        if any(not sheet.journal_id for sheet in self):
            raise UserError(_("Expenses must have an expense journal specified to generate accounting entries."))

        expense_line_ids = self.mapped('expense_line_ids')\
            .filtered(lambda r: not float_is_zero(r.total_amount, precision_rounding=(r.currency_id or self.env.company.currency_id).rounding))
        res = expense_line_ids.action_move_create()

        if not self.accounting_date:
            self.accounting_date = self.account_move_id.date

        if (self.payment_mode == 'own_account' or self.payment_mode == 'employee') and expense_line_ids:
            self.write({'state': 'post'})
        else:
            self.write({'state': 'done'})
        self.activity_update()
        return res
    