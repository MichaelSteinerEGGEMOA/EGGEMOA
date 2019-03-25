# -*- coding: utf-8 -*-
{
    'name':        "l10n_it_edi_custo_CW",

    'summary':
                   """
                   Fix quantiy with CW-QTY on SO""",

    'description': """
        Fix quantiy with CW-QTY on SO
    """,

    'author':      "Odoo",
    'website':     "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':    '',
    'version':     '0.1',

    # any module necessary for this one to work correctly
    'depends':     ['base', 'l10n_it_edi'],

    # always loaded
    'data':        [
        "views/invoice_it_template_inherit.xml",

    ],
    # only loaded in demonstration mode
    'demo':        [],
}
