from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportBalanceReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.balance_report_view'
    
    _description = 'Report Balance Analytique'
    
    def get_lines(self, analytic_id, date_start,date_end):
        
        params = [tuple(analytic_id),date_start,date_end]
        query = """
                SELECT pp.key AS code_project, pp.name AS name_project, x_aan.code AS code_analytic, SUM(x_aml.debit) AS x_debit, SUM(x_aml.credit) AS x_credit, (SUM(x_aml.debit)-SUM(x_aml.credit)) AS solde_debit, (SUM(x_aml.credit)-SUM(x_aml.debit)) AS solde_credit

                FROM account_move_line AS x_aml
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                INNER JOIN project_project AS pp ON pp.analytic_account_id = x_aan.id

                WHERE 
                    ( x_aa.code LIKE '6%') OR ( x_aa.code LIKE '7%')
                    AND
                    (x_aml.analytic_account_id = """+ analytic_id+""")
                    AND
                    (x_aml.date BETWEEN '%s' AND '%s')
                GROUP BY code_project,name_project,code_analytic
        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
      

    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        
        docs = []
        if data['form']['analytic']:
            analytic_id = data['form']['analytic'][0]
            lines = self.env['account.analytic.account'].search([('id','=',analytic_id)])
        else:
            lines = self.env['account.analytic.account'].search([])
        for line in lines:
            analytic = line.id
            id_aan = str(analytic)
            
            get_lines = self.get_lines(id_aan,date_start,date_end)
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines,
            })
            
        
        return {
            'doc_model': 'balance.analytic.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'get_lines':self.get_lines,
        }