{
    'name': "Real Estate",
    'version': '19.0.1',
    'depends': ['base','web'],
    'author': "HMK",
    'category': 'Category',
    'description': """
    Real Estate Odoo Training  Test
    """,
    'assets': {
        'web.assets_backend': [
            'real_estate/static/src/css/property_status.css',
        ],
    },
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/real_estate_view.xml',
        'views/real_estate_properties_type_view.xml',
        'views/real_estate_properties_tag_view.xml',
        'views/real_estate_properties_offer_view.xml',
        'menus/real_estate_menus.xml',
    ],
}
