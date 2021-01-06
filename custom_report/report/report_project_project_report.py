from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportTimeSheetReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.project_report_view'
    
    _description = 'Report Account Result'
    
    def get_lines(self, analytic_id, date_start,date_end):
        
        params = [tuple(analytic_id),date_start,date_end]
        query = """
                SELECT pp.name AS project, SUM(aml.debit) AS debit, SUM(aml.credit) AS credit, (SUM(aml.debit)-SUM(aml.credit)) AS marge
                FROM account_move_line AS aml
                INNER JOIN account_analytic_account AS aan ON aan.id = aml.analytic_account_id
                INNER JOIN project_project AS pp ON pp.analytic_account_id = aml.analytic_account_id
                INNER JOIN account_move AS am ON am.id = aml.move_id
                WHERE
                    (aml.analytic_account_id IN %s)
                    AND
                    (aml.date BETWEEN %s AND %s)

                GROUP BY project
        """

        self.env.cr.execute(query,params)
        return self.env.cr.dictfetchall()
      

    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        
        docs = []
        if data['form']['project']:
            project = data['form']['project'][0]
            lines = self.env['project.project'].search([('id','=',project)])
        else:
            lines = self.env['project.project'].search([])
        for line in lines:
            account = line.analytic_account_id.id
            id_aan = str(account)
            
            get_lines = self.get_lines(id_aan,date_start,date_end)
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines,
            })
            
        
        return {
            'doc_model': 'project.project.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'get_lines':self.get_lines,
        }