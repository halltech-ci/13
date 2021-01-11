# -*- coding: utf-8 -*-

from odoo import models, fields, api

PAYMENT_MODE = [('justify', 'Employee (To justify)'),
                ('company', 'Company (Not justify)'),
                ('reimburse', 'Employee (To Reimburse)'),
               ]

PAYMENT_TYPE = [('cash', 'Espece'),
                ('trasfert', 'Mobile'),
                ('check', 'Cheque'),
               ]

REQUEST_STATE = [('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('to_approve', 'To Approve'),
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
        ]

class ExpenseLine(models.Model):
    _name = 'expense.line'
    _description = 'Custom expense line'
    
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id
    
    name = fields.Char('Description', required=True)
    request_state = fields.Selection(selection=REQUEST_STATE, string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    employee_id = fields.Many2one('hr.employee', string="Beneficiaire", required=True, default=_default_employee_id, check_company=True)
    request_id = fields.Many2one('expense.request', string='Expense Request')
    date = fields.Datetime(readonly=True, related='request_id.date', string="Date")
    amount = fields.Float("Montant", required=True, digits='Product Price')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, 
                                 default=lambda self: self.env.company
                                )
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange', related='request_id.requested_by')
    payment_mode = fields.Selection(selection=PAYMENT_MODE, string="Payment Mode", default='company')
    payed_by = fields.Selection(selection=PAYMENT_TYPE, string="Payer Par", default='cash')
    analytic_account = fields.Many2one('account.analytic.account', related='request_id.analytic_account', 
                                       string='Analytic Account')
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, 
                                  default=lambda self: self.env.company.currency_id
                                 )
    accounting_date = fields.Date(string='Accounting Date')
    account_src = fields.Many2one('account.account', string='Debit Account')
    account_dst = fields.Many2one('account.account', string='Credit Account')
    
    def action_submit(self):
        self._action_submit()

    def _action_submit(self):
        self.request_state = "submit"
        
    def action_to_approve(self):
        self.request_state = "to_approve"
    
    def action_approve(self):
        self.request_state = "approve"       
    
    def unlink(self):
        for expense in self:
            if expense.request_state in ['done', 'approved']:
                raise UserError(_('You cannot delete a posted or approved expense.'))
        return super(ExpenseLine, self).unlink()

    def write(self, vals):
        for expense in self:
            if expense.request_state in ['done', 'approved']:
                raise UserError(_('You cannot modify a posted or approved expense.'))
        return super(ExpenseLine, self).write(vals)
    
