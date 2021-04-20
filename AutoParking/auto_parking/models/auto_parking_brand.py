# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                   #
###############################################################################

from odoo import api, fields, models, _  # alphabetically ordered


class AutoParkingManufacturers(models.Model):
    _name = 'auto.parking.brand'
    _description = 'Auto Parking Brand'

    name = fields.Char(
        string='Brand',
    )
    model_ids = fields.One2many('auto.parking.model','brand_id',
        string='Model',
    )
    # feature_ids = fields.Many2many(
    #     'auto.parking.features',
    #     string='Features',
    # )
    
