# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)
    
    payment_mode = fields.Selection(selection_add=[("employee", "Employee (to justify)")])
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
    
    #Overide methode to add payment type employee to justify
    def _create_sheet_from_expenses(self):
        if any(expense.state != 'draft' or expense.sheet_id for expense in self):
            raise UserError(_("You cannot report twice the same line!"))
        if len(self.mapped('employee_id')) != 1:
            raise UserError(_("You cannot report expenses for different employees in the same report."))
        if any(not expense.product_id for expense in self):
            raise UserError(_("You can not create report without product."))

        todo = self.filtered(lambda x: x.payment_mode=='own_account') or self.filtered(lambda x: x.payment_mode=='company_account') or self.filtered(lambda x: x.payment_mode=='employee')
        sheet = self.env['hr.expense.sheet'].create({
            'company_id': self.company_id.id,
            'employee_id': self[0].employee_id.id,
            'name': todo[0].name if len(todo) == 1 else '',
            'expense_line_ids': [(6, 0, todo.ids)]
        })
        sheet._onchange_employee_id()
        return sheet
    
    
    def _prepare_move_values(self):
        """
        This function prepares move values related to an expense
        """
        self.ensure_one()
        journal = self.sheet_id.bank_journal_id if (self.payment_mode == 'company_account' or self.payment_mode == 'employee') else self.sheet_id.journal_id
        account_date = self.sheet_id.accounting_date or self.date
        move_values = {
            'journal_id': journal.id,
            'company_id': self.sheet_id.company_id.id,
            'date': account_date,
            'ref': self.sheet_id.name,
            # force the name to the default value, to avoid an eventual 'default_name' in the context
            # to set it to '' which cause no number to be given to the account.move when posted.
            'name': '/',
        }
        return move_values
    
    
    def _get_expense_account_destination(self):
        self.ensure_one()
        account_dest = self.env['account.account']
        if self.payment_mode == 'company_account' or self.payment_mode == 'employee':
            if not self.sheet_id.bank_journal_id.default_credit_account_id:
                raise UserError(_("No credit account found for the %s journal, please configure one.") % (self.sheet_id.bank_journal_id.name))
            account_dest = self.sheet_id.bank_journal_id.default_credit_account_id.id
        else:
            if not self.employee_id.sudo().address_home_id:
                raise UserError(_("No Home Address found for the employee %s, please configure one.") % (self.employee_id.name))
            partner = self.employee_id.sudo().address_home_id.with_context(force_company=self.company_id.id)
            account_dest = partner.property_account_payable_id.id or partner.parent_id.property_account_payable_id.id
        return account_dest
    