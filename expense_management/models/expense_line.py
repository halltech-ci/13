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
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
        ]

class ExepnseLine(models.Model):
    _name = 'expense.line'
    _description = 'Custom expense line'
    
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id
    
    name = fields.Char('Description', required=True)
    request_state = fields.Selection(selection=REQUEST_STATE, related='request_id.state',string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    employee_id = fields.Many2one('hr.employee', string="Beneficiaire", required=True, default=_default_employee_id, check_company=True)
    request_id = fields.Many2one('expense.request', string='Expense Request')
    date = fields.Datetime(readonly=True, default=fields.Date.context_today, string="Date")
    amount = fields.Float("Montant", required=True, digits='Product Price')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, 
                                 default=lambda self: self.env.company
                                )
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange', related='request_id.requested_by')
    payment_mode = fields.Selection(selection=PAYMENT_MODE, string="Payment Mode", default='company')
    payed_by = fields.Selection(selection=PAYMENT_TYPE, string="Payer Par", default='cash')
    analytic_account = fields.Many2one('account.analytic.account', related='request_id.analytic_account', 
                                       string='Analytic Account')
    
    def unlink(self):
        for expense in self:
            if expense.request_state in ['done', 'approved']:
                raise UserError(_('You cannot delete a posted or approved expense.'))
        return super(ExpenseLine, self).unlink()

    def write(self, vals):
        for expense in self:
            if expense.request_state in ['done', 'approved']:
                raise UserError(_('You cannot delete a posted or approved expense.'))
        return super(ExpenseLine, self).write(vals)
    
