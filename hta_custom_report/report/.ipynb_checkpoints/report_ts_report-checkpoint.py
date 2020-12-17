from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportTimeSheetReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_custom_report.time_sheet_report_view'
    
    _description = 'Report Time Sheet'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        

        AAL = self.env['account.analytic.line']
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        delta = timedelta(days=1)

        docs = []

        if data['form']['employee_ids']:
            employee_ids = data['form']['employee_ids'][0]
            timesheets = AAL.search([
                        ('date', '>=', start_date.strftime(DATETIME_FORMAT)),
                        ('employee_id', '=', employee_ids)
                        ])
        else:
            timesheets = AAL.search([
                        ('date', '>=', start_date.strftime(DATETIME_FORMAT)),
                    ])
        
        for timesheet in timesheets:
            
            
            date = timesheet.date
            employee = timesheet.employee_id.name
            name = timesheet.name
            project = timesheet.project_id.name
            task = timesheet.task_id.name
            duration = timesheet.unit_amount
            amount = timesheet.amount
            
            docs.append ({
                'date': date,
                'name': name,
                'employee': employee,
                'project': project,
                'task': task,
                'duration': duration,
                'amount': amount
            })

        return {
            'doc_model': 'account.analytic.line',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }