# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Italy - E-invoicing',
    'version': '0.3',
    'depends': ['l10n_it'],
    'author': 'Odoo',
    'description': """
E-invoice implementation for customer invoice
    """,
    'category': 'Localization',
    'website': 'http://www.odoo.com/',
    'data': [
        'security/ir.model.access.csv',
        'data/invoice_it_template.xml',
        'data/l10n_it_chart_data.xml',
        'views/l10n_it_view.xml',
        ],
    'demo': [
        'data/account_invoice_demo.xml',
    ],
}