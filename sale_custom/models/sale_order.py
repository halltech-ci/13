# -*- coding: utf-8 -*-

from odoo import models, fields, api


_SALE_ORDER_DOMAINE = [('fm', 'FABRICATION MECANIQUE'),
                          ('cm', 'CONSTRUCTION METALLIQUE'),
                          ('gc', 'GENIE CIVILE'),
                          ('ct', 'CHAUDRONNERIE TUYAUTERIE'),
                          ('em', 'ELECTROMECANIQUE'),
                          ('bt', 'BATIMENT'),
                          ('ra', 'RECTIFICATION AUTOMOBILE'),
                          ('mi', 'MAINTENANCE INDUSTRIELLE'),
                          ('me', 'MAINTENANCE ELECTROMECANIQUE'),
                          ('mm', 'MAINTENANCE MECANIQUE'),
                          ('cu', 'CONSTRUCTION USINE'),
                          ('ep', 'ETUDES DE PROJET')
    ]

class SameOrder(models.Model):
    _inherit = "sale.order"
    
    project_id = fields.Many2one("project.project", "Project", ondelete= "cascade")
    project_code = fields.Char("Code Projet", related='project_id.key')
    description = fields.Text("Description : ")
    signed_user = fields.Many2one("res.users", string="Signed In User", readonly=True, default= lambda self: self.env.uid)
    sale_order_recipient = fields.Char("Destinataire")
    sale_order_type = fields.Selection(_SALE_ORDER_DOMAINE, string="Domaine", required=True, index=True, default='fm')
