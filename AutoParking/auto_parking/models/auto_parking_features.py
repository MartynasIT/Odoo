from odoo import models, fields, api, _


class AutoParkingFeatures(models.Model):
    _name = 'auto.parking.features'

    name=fields.Char(
        string='Feature',
    )
    model_ids = fields.Many2many(
        'auto.parking.model',
        string='Model',
    )
