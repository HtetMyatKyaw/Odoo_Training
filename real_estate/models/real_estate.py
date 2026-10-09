from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class RealEstate(models.Model):
    _name = 'real.estate'
    _description = 'RealEstate'


    name = fields.Char(required=True)
    property_reference = fields.Char(
        string='Properties ID',
        readonly=True,
        copy=False,
        index=True,
    )
    status = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        default='new',
        required=True,
        readonly=True,
        copy=False,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Salesman',
        default=lambda self: self.env.user,
        domain=[('share', '=', False)],
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False,
    )
    offer_ids = fields.One2many(
        'real.estate.properties.offer',
        'property_id',
        string='Offers',
    )
    tag_ids = fields.Many2many(
        'real.estate.properties.tag',
        string='Tags',
    )
    property_type_id = fields.Many2one(
        'real.estate.properties.type',
        string='Property Type',
        domain=[('name', '!=', False)],
        copy=False,
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    total_area = fields.Float( compute='_compute_total_area')
    best_offer = fields.Float(compute='_compute_best_offer')

    _expected_price_positive = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be greater than zero.',
    )

    _property_reference_unique = models.Constraint(
        'UNIQUE(property_reference)',
        'Properties ID must be unique.',
    )

    @api.model_create_multi
    def create(self, vals_list):
        creation_date = fields.Date.context_today(self)
        for vals in vals_list:
            serial = self.env['ir.sequence'].next_by_code('real.estate.property')
            if not serial:
                raise UserError(self.env._('The Properties ID sequence is not configured.'))
            vals['property_reference'] = f'{creation_date:%d%m%Y}-{serial}'
        return super().create(vals_list)

    @api.constrains('expected_price', 'selling_price', 'status')
    def _check_expected_price_accept(self):
        for record in self:
            if (
                record.status in ('offer_accepted', 'sold')
                and record.selling_price < record.expected_price * 0.9
            ):
                raise ValidationError(self.env._(
                    'Selling price must be at least 90% of the expected price.'
                ))

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError(self.env._(
                    'Expected price must be greater than zero.'
                ))

    def action_sold(self):
        if any(record.status == 'cancel' for record in self):
            raise UserError(self.env._('A cancelled property cannot be marked as sold.'))
        if any(record.status != 'offer_accepted' for record in self):
            raise UserError(self.env._('Accept an offer before marking the property as sold.'))
        self.write({'status': 'sold'})
        return True

    def action_cancel(self):
        if any(record.status == 'sold' for record in self):
            raise UserError(self.env._('A sold property cannot be cancelled.'))
        self.write({'status': 'cancel'})
        return True

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation = False

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area


    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        """Compute the highest offer price for the property."""
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0.0)
