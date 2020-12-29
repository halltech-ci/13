from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportLivrePaieReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.livre_paie_report_view'
    
    _description = 'Report Paie Book '
    
    def get_lines(self, employee, date_start,date_end):
        
        query = """
            SELECT  he.id AS x_employee_id, hpl.name AS x_hpl_name, hpl.total AS x_hpl_total
            FROM  hr_contract AS x_hc
            INNER JOIN hr_employee AS he ON he.id = x_hc.employee_id
            INNER JOIN hr_payslip AS hp ON hp.contract_id = x_hc.id
            INNER JOIN  hr_payslip_line AS hpl ON hpl.contract_id = x_hc.id
            WHERE
                he.id = """+ employee+"""
                AND
                (hp.date BETWEEN '%s' AND '%s')

            GROUP BY x_employee_id, x_hpl_name, x_hpl_total

            """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
      

    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        
        docs = []
        if data['form']['employee']:
            employee = data['form']['employee'][0]
            lines = self.env['hr.payslip'].search([('employee_id','=',employee)])
        else:
            lines = self.env['hr.payslip'].search([('employee_id','!=',False)])
        for line in lines:
            employee_id = line.employee_id.id
            id_he = str(employee_id)
            
            get_lines = self.get_lines(id_he,date_start,date_end)
            
            
            docs.append({
                'name': employee_id,
                'get_lines':get_lines,
            })
            
        
        return {
            'doc_model': 'livre.paie.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'get_lines':self.get_lines,
        }