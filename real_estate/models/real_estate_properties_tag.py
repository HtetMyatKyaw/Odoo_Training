from odoo import fields, models


class RealEstatePropertiesTag(models.Model):
    _name = 'real.estate.properties.tag'
    _description = 'Property Tag'

    name = fields.Char(required=True)
    color = fields.Integer(string='Color', default=0)
