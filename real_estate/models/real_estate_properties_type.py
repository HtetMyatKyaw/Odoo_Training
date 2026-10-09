from odoo import fields, models


class RealEstatePropertiesType(models.Model):
    _name = 'real.estate.properties.type'
    _description = 'Property Type'

    name = fields.Char(string='Type')
    property_ids = fields.One2many(
        'real.estate',
        'property_type_id',
        string='Properties',
    )

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.',
    )
