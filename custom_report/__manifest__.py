# -*- coding: utf-8 -*-
{
    'name': "custom_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant','project',
                'hr_holidays',
               'hr_payroll',
               'account',
               'hr_payroll_account',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        #report
        'report/template_report_project_report.xml',
        'report/template_report_analytic_report.xml',
        'report/template_report_result_report.xml',
        'report/template_repor_paie_book_report.xml',
        
        #wizard
        'wizard/wizard_project_project_views.xml',
        'wizard/wizard_account_analytic_views.xml',
        'wizard/wizard_account_result_views.xml',
        'wizard/wizard_paie_book_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
