# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class TimeSheetReportWizard(models.TransientModel):
    _name = 'time.sheet.report.wizard'

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    employee_ids = fields.Many2one('hr.employee', string="Employee")

    def get_report(self):
        data = {
            'model':'time.sheet.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('hta_custom_report.time_sheet_report').with_context(landscape=True).report_action(self, data=data)

