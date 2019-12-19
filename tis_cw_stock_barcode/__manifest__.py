# -*- coding: utf-8 -*-
# Copyright (C) 2019-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).
{
    'name': 'CatchWeight- Barcode',
    'version': '12.0.2.0.2',
    'sequence': 1,
    'category': 'Inventory',
    'summary': 'Catchw8 - Catch Weight Management Stock Barcode',
    'description': """
""",
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'website': 'http://www.catchweighterp.com/',
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': [
        'tis_catch_weight', 
	'stock_barcode'
    ],
    'data': [
        'views/stock_move_line_views.xml',
        'views/stock_barcode_templates.xml',
    ],
    'qweb': [
        "static/src/xml/qweb_templates.xml",
    ],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True
}
