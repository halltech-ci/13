from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportTimeSheetReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.analytic_report_view'
    
    _description = 'Report Account Analytic'
    
    def get_lines(self, analytic_id, date_start,date_end):
        
        query = """
                SELECT x_aml.analytic_account_id AS x_analytic_account_id, SUM(x_aml.debit) AS x_debit, SUM(x_aml.credit) AS x_credit
                FROM account_move_line AS x_aml
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id

                WHERE 
                    (( x_aa.code LIKE '6%'
                                OR x_aa.code LIKE '81%'
                                OR x_aa.code LIKE '83%'
                                OR x_aa.code LIKE '85%'
                                OR x_aa.code LIKE '87%'
                                OR x_aa.code LIKE '89%'

                            ) OR ( x_aa.code LIKE '7%'
                                OR x_aa.code LIKE '82%'
                                OR x_aa.code LIKE '84%'
                                OR x_aa.code LIKE '86%'
                                OR x_aa.code LIKE '88%'


                            ))
                            AND
                            x_aml.analytic_account_id = """+ analytic_id+"""
                            AND
                            (x_aml.date BETWEEN '%s' AND '%s')
                GROUP BY x_analytic_account_id
        """ %(date_start,date_end)

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
            'doc_model': 'account.analytic.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'get_lines':self.get_lines,
        }