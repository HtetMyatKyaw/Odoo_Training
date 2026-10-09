from odoo import fields, models, api
from odoo.exceptions import UserError


class RealEstatePropertiesOffer(models.Model):
    _name = 'real.estate.properties.offer'
    _description = 'Offer'

    name = fields.Char()
    price = fields.Float()
    validity = fields.Integer(string='Validity (Days)')
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', copy=False)
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True,
    )
    property_id = fields.Many2one(
        'real.estate',
        string='Property',
        required=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        new_properties = offers.mapped('property_id').filtered(
            lambda property_record: property_record.status == 'new'
        )
        new_properties.write({'status': 'offer_received'})
        return offers

    def action_accept(self):
        self.ensure_one()
        property_record = self.property_id
        if property_record.status in ('offer_accepted', 'sold', 'cancel'):
            raise UserError(self.env._(
                'You cannot accept another offer for an accepted, sold or cancelled property.'
            ))
        property_record.write({
            'selling_price': self.price,
            'buyer_id': self.partner_id.id,
            'status': 'offer_accepted',
        })
        self.write({'status': 'accepted'})
        return True

    def action_refuse(self):
        self.write({'status': 'refused'})
        return True

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            creation_date = (
                fields.Date.to_date(record.create_date)
                if record.create_date
                else fields.Date.today()
            )
            record.date_deadline = fields.Date.add(
                creation_date, days=record.validity,
            )

    @api.onchange('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                creation_date = (
                    fields.Date.to_date(record.create_date)
                    if record.create_date
                    else fields.Date.today()
                )
                record.validity = (record.date_deadline - creation_date).days
