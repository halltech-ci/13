# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ExpenseRequest(models.Model):
    _name = 'expense.request'
    _description = 'Custom expense request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id
    
    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)
    
    name = fields.Char('Description', required=True)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('to_approve', 'To Approve'),
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, states={'draft': [('readonly', False)]}, default=_default_employee_id, check_company=True)
    line_ids = fields.One2many('expense.line', 'request_id', string='Expense Line')
    intermediary = fields.Many2one('hr.employee', string="Intermediaire")
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange',
                    default=_get_default_requested_by)
    date = fields.Datetime(readonly=True, default=fields.Datetime.now, string="Date")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.company.currency_id)
    total_amount = fields.Monetary('Total Amount', currency_field='currency_id', compute='_compute_amount', store=True)
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account')
    project_id = fields.Many2one('project.project', string='Projet')
    to_approve_allowed = fields.Boolean(compute="_compute_to_approve_allowed")
    journal = fields.Many2one('account.journal', string='Journal', required=True, 
                              default=lambda self:self.env['account.journal'].search([('type', '=', 'cash')])
                             )
    
    @api.depends("state")
    def _compute_to_approve_allowed(self):
        for rec in self:
            rec.to_approve_allowed = rec.state == "submit" 
    
    @api.onchange('company_id')
    def _onchange_expense_company_id(self):
        self.employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid), ('company_id', '=', self.company_id.id)])
    
    @api.depends('line_ids.amount')
    def _compute_amount(self):
        for request in self:
            request.total_amount = sum(request.line_ids.mapped('amount'))
    
    def prepare_move_values(self):
        """
        This function prepares move values related to an expense line
        """
        self.ensure_one()
        journal = self.journal
        account_date = self.date
        move_values = {
            'journal_id': journal.id,
            'company_id': self.company_id.id,
            'date': account_date,
            'ref': self.name,
            # force the name to the default value, to avoid an eventual 'default_name' in the context
            # to set it to '' which cause no number to be given to the account.move when posted.
            'name': '/',
        }
        return move_values
    
   
    def action_move_create(self):
        '''
        main function that is called when trying to create the accounting entries related to an expense
        '''
        move_obj = self.env['account.move']
        payment_obj = self.env['account.payment']
        for expense in self:
            company_currency = expense.company_id.currency_id
            different_currency = expense.currency_id != company_currency
     
    
    
    def action_submit(self):
        for line in self.line_ids:
            line.action_submit()
        self.state = "submit"
        return True
    
    def button_to_approve(self):
        self.to_approve_allowed_check()
        for line in self.line_ids:
            line.action_to_approve()
        return self.write({"state": "to_approve"})
    
    def button_approve(self):
        #self.to_approve_allowed_check()
        for line in self.line_ids:
            line.action_approve()
        return self.write({"state": "approve"})
    
    def to_approve_allowed_check(self):
        for rec in self:
            if not rec.to_approve_allowed:
                raise UserError(
                    _(
                        "You can't request an approval for a expense request "
                        "which is empty. (%s)"
                    )
                    % rec.name
                )
    
    @api.model
    def create(self, vals):
        request = super(ExpenseRequest, self).create(vals)
        return request
    
    def write(self, vals):
        res = super(ExpenseRequest, self).write(vals)
        return res
    
    '''def activity_update(self):
        for expense_report in self.filtered(lambda hol: hol.state == 'submit'):
            self.activity_schedule(
                'hr_expense.mail_act_expense_approval',
                user_id=expense_report.sudo()._get_responsible_for_approval().id or self.env.user.id)
        self.filtered(lambda hol: hol.state == 'approve').activity_feedback(['hr_expense.mail_act_expense_approval'])
        self.filtered(lambda hol: hol.state == 'cancel').activity_unlink(['hr_expense.mail_act_expense_approval'])
    '''
    