from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportEtatTvaReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.tva_report_view'
    
    _description = 'Report Etat Tva'
    
    def get_lines(self, partner_id, date_start,date_end):
        
        params = [tuple(partner_id),date_start,date_end]
        query = """
                SELECT rp.name AS partner, am.ref AS refence, am.date AS x_date, SUM(am.amount_total) AS total, SUM(am.amount_tax) AS tax
                FROM account_move AS am
                INNER JOIN res_partner AS rp ON rp.id = am.partner_id
                WHERE
                    (am.type LIKE '%invoice%')
                    AND
                    (am.partner_id = """+partner_id+""")
                    AND
                    (am.date BETWEEN '%s' AND '%s')

                GROUP BY partner,refence,x_date
        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
      

    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        
        docs = []
        if data['form']['partner']:
            partner = data['form']['partner'][0]
            lines = self.env['res.partner'].search([('id','=',partner)])
        else:
            lines = self.env['res.partner'].search([])
        for line in lines:
            partner_id = line.id
            id_rp = str(partner_id)
            
            get_lines = self.get_lines(id_rp,date_start,date_end)
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines,
            })
            
        
        return {
            'doc_model': 'etat.tva.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'get_lines':self.get_lines,
        }