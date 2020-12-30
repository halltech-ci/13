# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class LivrePaieReportWizard(models.TransientModel):
    _name = 'livre.paie.report.wizard'
    _description = "Wizard Livre Paie"

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    #partner = fields.Many2one('hr.partner', string="Partner")
    employee = fields.Many2one('hr.employee', string="Employee")

    def get_report(self):
        data = {
            'model':'livre.paie.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report.livre_paie_report').with_context(landscape=True).report_action(self, data=data)

