# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class AccountAnalyticReportWizard(models.TransientModel):
    _name = 'paie.book.report.wizard'
    _description = "Wizard Paie Book"
    

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    #partner = fields.Many2one('hr.partner', string="Partner")
    id_employee = fields.Many2one('hr.employee', string="Employee")

    def get_report(self):
        data = {
            'model':'paie.book.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report.paie_book_report').with_context(landscape=True).report_action(self, data=data)

