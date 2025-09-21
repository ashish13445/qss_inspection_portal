{
    'name': 'QSS Portal',
    'version': '17.0.1.0.0',
    'summary': 'Workflow for enquiries, quotations, inspections, billing',
    'author': 'Your Company',
    'license': 'LGPL-3',
    'website': 'https://example.com',
    'depends': ['base', 'mail','account'],
    'data': [
        'security/qss_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu.xml',
        'views/enquiry_views.xml',
        'report/report_qss_quotation.xml',
        'views/quotation_views.xml',
        'views/project_number_views.xml',
        'views/inspection_call_views.xml',
        'views/visit_report_views.xml',
        'views/payment_views.xml',
    ],
    'application': True,
}


