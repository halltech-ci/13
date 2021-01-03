# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    expense_cost = fields.Monetary('Expense Cost', currency_field='currency_id',
    	groups="hr.group_hr_user", compute="_compute_expense_cost")
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    expense_account = fields.Many2one('account.account', string="Expense Account")
    salary_account = fields.Many2one('account.account', string="Salary Account")
    
    def _compute_expense_cost(self):
        for record in self:
            expenses = self.env['hr.expense.sheet'].search([('employee_id', '=', record.id), ('payment_mode', '=', 'company_account')])
            cost = 0.0
            if expenses:
                for expense in expenses:
                    cost += expense.amount_residual
            record.expense_cost = cost
            
