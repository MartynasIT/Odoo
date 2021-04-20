# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                   #
###############################################################################

from odoo import api, fields, models, _  # alphabetically ordered


class AutoParkingManufacturers(models.Model):
    _name = 'auto.parking.model'
    _description = 'Auto Parking Models'

    name = fields.Char(
        string='Model',
    )
    brand_id = fields.Many2one('auto.parking.brand',
        string='Brand',
        ondelete='cascade',
    )
    # feature_ids = fields.Many2many(
    #     'auto.parking.features',
    #     string='Features',
    # )

