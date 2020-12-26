from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportTimeSheetReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.time_sheet_report_view'
    
    _description = 'Report Time Sheet'
    
        def get_marcha(self, objs):
        res = []
        ids = []
        for item in objs:
            if item.appears_on_payslip is True and not item.salary_rule_id.parent_rule_id:
                ids.append(item.id)
        if ids:
            res = self.env['hr.payslip.line'].browse(ids)
        return res

    def get_total_by_rule_category(self, obj, code):
        category_total = 0
        category_id = self.env['hr.salary.rule.category'].search([('code', '=', code)], limit=1).id
        if category_id:
            line_ids = self.env['hr.payslip.line'].search([('slip_id', '=', obj.id), ('category_id', 'child_of', category_id)])
            for line in line_ids:
                category_total += line.total
        return category_total
    
    #Here obj represent payslip object
    def parse_payslip_lines(self, obj):
        code_dict = {}
        p_lines = self.env['hr.payslip'].search([('id', '=', obj.id)]).line_ids
        code_dict = {}
        for line in p_lines:
            code = line.code
            name = line.name
            val = line.amount
            dico = {code:[name, val],}#example: TH:['Taux Horaire', 177.33]
            code_dict.update(dico)
        return code_dict
        
    def get_employer_line(self, obj, parent_line):
        return self.env['hr.payslip.line'].search([('slip_id', '=', obj.id), ('salary_rule_id.parent_rule_id.id', '=', parent_line.salary_rule_id.id)], limit=1)

    
    @api.model
    def _get_report_values(self, docids, data=None):

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