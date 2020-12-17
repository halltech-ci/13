# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class hta_custom_hr(models.Model):
#     _name = 'hta_custom_hr.hta_custom_hr'
#     _description = 'hta_custom_hr.hta_custom_hr'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class HrContract(models.Model):
    _inherit = "hr.contract"
    
    #hourly_rate = fields.Monetary(string="Taux Horaire", compute="_compute_employee_hourly_rate")
    prime_transport = fields.Monetary(string="Prime de Transport")
    indemnite_transport = fields.Monetary(string="Indemnité de Transport")
    prime_communication = fields.Monetary(string="Communication")
    sursalaire = fields.Monetary(string="Sursalaire")
    prime_logement = fields.Monetary(string="Logement")
    prime_responsabilite = fields.Monetary(string="Responsabilité")
    prime_rendement = fields.Monetary(string="Prime de rendement")
    prime_salissure = fields.Monetary(string="Salissure")
    #prime_anciennete = fields.Monetary(string="Ancienneté", compute='_compute_anciennete')
    gratification = fields.Monetary(string="Gratification")
    autres_avantages = fields.Monetary(string="Autres Avantages")
    conges_payes = fields.Monetary(string="Congés Payés")
    salaire_brut = fields.Monetary(string="Salary Cost")
    avs = fields.Monetary(string="Avances et  Acomptes perçus")
    partner_id = fields.Many2one('res.partner', string="Partner")
   