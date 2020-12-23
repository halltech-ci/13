from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportTimeSheetReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.account_result_report_view'
    
    _description = 'Report Account Result'
    
    def get_lines(self, analytic_id, date_start,date_end):
        
        query = '''
                    (SELECT  SUM(x_aml.balance) AS x_balance_vente
                     FROM account_move_line AS x_aml
                     INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                     INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                     INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id
                     WHERE
                        ( x_aa.code IN ('701100','701200','701300','701400'))
                        AND
                        ( x_aml.date BETWEEN '''+str(date_start)+''' and '''+str(date_end)+''' )
                        AND
                        ( x_aml.analytic_account_id = '''+str(analytic_id)+''' ) 
                   
                     )
                    UNION ALL
                     (SELECT  SUM(x_aml.balance) AS x_balance_achat
                      FROM account_move_line AS x_aml
                      INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                      INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                      INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id
                      WHERE
                        ( x_aa.code LIKE '601%' 
                         OR x_aa.code LIKE '601%'
                         OR x_aa.code LIKE '603%'
                         OR x_aa.code LIKE '604%') 
            
                        AND
                        ( x_aml.date BETWEEN '''+str(date_start)+''' and '''+str(date_end)+''' )
                        AND
                        ( x_aml.analytic_account_id = '''+str(analytic_id)+''' ) 
 
                      )
                    UNION ALL
                     (SELECT  SUM(x_aml.balance) AS x_balance_vente_product_frab
                      FROM account_move_line AS x_aml
                      INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                      INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                      INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id
                      WHERE
                        ( x_aa.code LIKE '7061%') 
                        AND
                        ( x_aml.date BETWEEN '''+str(date_start)+''' and '''+str(date_end)+''' )
                        AND
                        ( x_aml.analytic_account_id = '''+str(analytic_id)+''' ) 
 
                      )
                    UNION ALL
                     (SELECT  SUM(x_aml.balance) AS x_balance_travaux_service
                      FROM account_move_line AS x_aml
                      INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                      INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                      INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id
                      WHERE
                        ( x_aa.code LIKE '7062%' 
                         OR x_aa.code LIKE '7063%'
                         OR x_aa.code LIKE '7064%'
                         OR x_aa.code LIKE '7071%'
                         OR x_aa.code LIKE '7072%'
                         OR x_aa.code LIKE '7073%'
                         OR x_aa.code LIKE '7074%'
                         OR x_aa.code LIKE '7075%'
                         OR x_aa.code LIKE '7076%'
                         OR x_aa.code LIKE '7077%') 
                        AND
                        ( x_aml.date BETWEEN '''+str(date_start)+''' and '''+str(date_end)+''' )
                        AND
                        ( x_aml.analytic_account_id = '''+str(analytic_id)+''' ) 
 
                      )
                    UNION ALL
                     (SELECT  SUM(x_aml.balance) AS x_balance_product_accesoire
                      FROM account_move_line AS x_aml
                      INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                      INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                      INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id
                      WHERE
                        ( x_aa.code LIKE '7078%') 
                        AND
                        ( x_aml.date BETWEEN '''+str(date_start)+''' and '''+str(date_end)+''' )
                        AND
                        ( x_aml.analytic_account_id = '''+str(analytic_id)+''' ) 
 
                      )
                    UNION ALL
                     (SELECT SUM(x_aml.balance) AS x_balance_product_stok
                      FROM account_move_line AS x_aml
                      INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                      INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                      INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id
                      WHERE
                        ( x_aa.code LIKE '601%' 
                         OR x_aa.code LIKE '601%'
                         OR x_aa.code LIKE '603%'
                         OR x_aa.code LIKE '604%') 
                        AND
                        ( x_aml.date BETWEEN '''+str(date_start)+''' and '''+str(date_end)+''' )
                        AND
                        ( x_aml.analytic_account_id = '''+str(analytic_id)+''' ) 
 
                      )
                    UNION ALL
                     (SELECT  SUM(x_aml.balance) AS x_balance_product_immobilise
                      FROM account_move_line AS x_aml
                      INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                      INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                      INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id
                      WHERE
                        ( x_aa.code LIKE '601%' 
                         OR x_aa.code LIKE '601%'
                         OR x_aa.code LIKE '603%'
                         OR x_aa.code LIKE '604%') 
                        AND
                        ( x_aml.date BETWEEN '''+str(date_start)+''' and '''+str(date_end)+''' )
                        AND
                        ( x_aml.analytic_account_id = '''+str(analytic_id)+''' ) 
 
                      )
                    UNION ALL
                     (SELECT  SUM(x_aml.balance) AS x_balance_subvent_exp
                      FROM account_move_line AS x_aml
                      INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                      INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                      INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id
                      WHERE
                        ( x_aa.code LIKE '601%' 
                         OR x_aa.code LIKE '601%'
                         OR x_aa.code LIKE '603%'
                         OR x_aa.code LIKE '604%') 
                        AND
                        ( x_aml.date BETWEEN '''+str(date_start)+''' and '''+str(date_end)+''' )
                        AND
                        ( x_aml.analytic_account_id = '''+str(analytic_id)+''' ) 
 
                      )
                    UNION ALL
                     (SELECT  SUM(x_aml.balance) AS x_balance_autre_product
                      FROM account_move_line AS x_aml
                      INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                      INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                      INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id
                      WHERE
                        ( x_aa.code LIKE '601%' 
                         OR x_aa.code LIKE '601%'
                         OR x_aa.code LIKE '603%'
                         OR x_aa.code LIKE '604%') 
                         
                        AND
                        ( x_aml.date BETWEEN '''+str(date_start)+''' and '''+str(date_end)+''' )
                        AND
                        ( x_aml.analytic_account_id = '''+str(analytic_id)+''' ) 
 
                      )
                    UNION ALL
                     (SELECT  SUM(x_aml.balance) AS x_balance_transfert_charge_expl
                      FROM account_move_line AS x_aml
                      INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                      INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                      INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id
                      WHERE
                        ( x_aa.code LIKE '601%' 
                         OR x_aa.code LIKE '601%'
                         OR x_aa.code LIKE '603%'
                         OR x_aa.code LIKE '604%') 
                        AND
                        ( x_aml.date BETWEEN '''+str(date_start)+''' and '''+str(date_end)+''' )
                        AND
                        ( x_aml.analytic_account_id = '''+str(analytic_id)+''' ) 
 
                      )

                    '''
        
        self.env.cr.execute(query)
        self.env.cr.dictfetchall()
      
    
    #Here obj represent payslip object
    '''def get_project_lines(self,data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        docs = []
        if data['form']['project']:
            project = data['form']['project'][0]
            lines = self.env['project.project'].search([('id','=',project)])
        else:
            lines = self.env['project.project'].search([])
        for line in lines:
            get_lines = self.get_lines(line.analytic_account_id,date_start,date_end)
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines
            })
        return docs
        '''
    
    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        docs = []
        if data['form']['project']:
            project = data['form']['project'][0]
            lines = self.env['project.project'].search([('id','=',project)])
        else:
            lines = self.env['project.project'].search([])
        for line in lines:
            get_lines = self.get_lines(line.analytic_account_id.id,start_date.strftime(DATE_FORMAT),end_date.strftime(DATE_FORMAT))
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines,
            })
            
        
        return {
            'doc_model': 'account.analytic.line',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'get_lines':self.get_lines,
        }