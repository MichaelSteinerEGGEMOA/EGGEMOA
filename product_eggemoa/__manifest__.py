{
    "name": "Product Eggemoa",
    "summary": """
        This module purpose is to allow handling unit of a different category on the invoice proccess.
    """,
    "category": "",
    "version": "12.0.1.0.0",
    "author": "Odoo PS",
    "website": "http://www.odoo.com",
    "license": "OEEL-1",
    "depends": ["account", "product", "stock_account",],
    "data": [
        "views/product_template.xml",
        "views/product_product.xml",
        "views/account_invoice.xml",
    ],
    # Only used to link to the analysis / Ps-tech store
    "task_id": [2480583],
}
