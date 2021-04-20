# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _


class AutoParkingTracking(models.Model):
    _name = 'auto.parking.tracking'
    _description = 'Auto Parking Tracking'
    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Many2one(
        'auto.parking',
        string='Auto number',
    )
    date_from = fields.Datetime(
        string='Parked from',
    )
    date_to = fields.Datetime(
        string='Parked to',
    )
    total_park_time = fields.Float(
        string='Total time parked',
    )
    

