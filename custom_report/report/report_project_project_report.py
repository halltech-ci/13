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
    
    def get_lines(self, project_id, date_start,date_end):
        
        query = '''
                    SELECT x_so.project_id AS x_project_id, x_so.amount_total AS x_amount_total, SUM(x_po.amount_total) AS x_po_amount_total, x_so.amount_total - SUM(x_po.amount_total) as x_marge
                    FROM  project_project AS x_pp
                    INNER JOIN sale_order AS x_so ON x_pp.id = x_so.project_id
                    INNER JOIN purchase_order AS x_po ON x_so.id = x_po.sale_order_id
                    WHERE (x_pp.date_start >= %s and x_pp.date_start <= %s)
                          AND
                          (x_pp.id IN %s)

                    GROUP BY x_project_id,  x_amount_total

                    '''
        params = [date_start,date_end,tuple(project_id) ]
        self.env.cr.execute(query,params)
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
        
        id_project = []
        docs = []
        if data['form']['project']:
            project = data['form']['project'][0]
            lines = self.env['project.project'].search([('id','=',project)])
        else:
            lines = self.env['project.project'].search([])
        for line in lines:
            id_project.append(line.analytic_account_id.id)
            start_date = datetime.strptime(date_start, DATE_FORMAT)
            end_date = datetime.strptime(date_end, DATE_FORMAT)
            get_lines = self.get_lines(id_project,start_date.strftime(DATE_FORMAT),end_date.strftime(DATE_FORMAT))
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