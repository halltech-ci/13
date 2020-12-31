from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportTimeSheetReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.book_report_view'
    
    _description = 'Report Paie Book'
    
    def get_lines(self, employee, date_start,date_end):
        
        params = [date_start,date_end,tuple(employee)]
        query = """
            SELECT hpl.name AS x_hpl_name, SUM(hpl.total) AS x_hpl_total, hpl.employee_id AS x_employee
            FROM hr_payslip AS hp
            INNER JOIN hr_contract AS x_hc ON hp.contract_id = x_hc.id
            INNER JOIN hr_payslip_line AS hpl ON hpl.slip_id = hp.id
            WHERE
                (hp.date BETWEEN %s AND %s)
                AND (hpl.employee_id IN %s)
            GROUP BY x_hpl_name, x_employee
            """
        
        self.env.cr.execute(query,params)
        return self.env.cr.dictfetchall()
      

    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        
        
        
        if data['form']['id_employee']:
            employee = data['form']['id_employee'][0]
            lines_contrat = self.env['hr.contract'].search([('employee_id','=',employee)])
        else:
            lines_contrat = self.env['hr.contract'].search([])
        docs = []    
        for line in lines_contrat:
            if len(line.employee_id.slip_ids)>0:
                employee = line.employee_id.id
                employee_name = line.employee_id.name
                id_he = str(employee)
                get_lines = self.get_lines(id_he,date_start,date_end)
            
                docs.append({
                    'name':employee_name,
                    'get_lines':get_lines,
                })
            
        
        return {
            'doc_model': 'paie.book.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'get_lines':self.get_lines,
        }