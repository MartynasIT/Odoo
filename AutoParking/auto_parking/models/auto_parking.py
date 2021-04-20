# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                   #
###############################################################################

from odoo import api, fields, models, exceptions, _  # alphabetically ordered
from datetime import date, datetime
import re

import logging
_logger = logging.getLogger(__name__)


class AutoParking(models.Model):
    _name = 'auto.parking'
    _description = 'Auto Parking'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Auto number',
        required=True,
        default=lambda self: _('HHH000'),
        copy=False
    )
    brand_id = fields.Many2one(
        'auto.parking.brand',
        string='Brand',
        ondelete='cascade',
        required=True,
    )
    date_from = fields.Date(
        string='Valid from',
        default=fields.Date.context_today,
    )
    date_to = fields.Date(
        string='Valid to',
    )
    model_id = fields.Many2one(
        'auto.parking.model',
        string='Model',
        ondelete='cascade',
        required=True,
    )
    size = fields.Selection(
        string='Engine size',
        selection=[
            ('small', '<=1L'),
            ('medium', '>= 2L'),
            ('big', '>= 5L'),
        ],
        select=True,
    )
    brands_at_garage = fields.Integer(
        string='Already at garage',
        compute='_brand_count'
    )
    car_active = fields.Boolean(
        string='Active',
        default=True,
        store=True,
    )
    park_start = fields.Datetime(
        string='Start Park',
    )
    park_end = fields.Datetime(
        string='End park',
    )
    park_time = fields.Float(
        string='Park Time',
    )
    park_rating = fields.Selection(
        [('1', 'First'),
         ('2', 'Second'),
         ('3', 'Third'),
         ('4', 'Fourth'),
         ('5', 'Fifth'),
         ],
        select=True,
    )
    image = fields.Binary(
        string="Image"
    )
    state = fields.Selection([
        ('unset', 'Unset'),
        ('parked', 'Parked'),
        ('finished', 'Finished parking'),
    ], default='unset'
    )
    park_driver = fields.Many2one(
        'res.partner',
        string='Driver',
        ondelete='cascade',
    )
    # feature_ids = fields.Many2many(
    #     'auto.parking.features',
    #     string='Features',
    # )

    # kai naudojamas compute

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            if not re.match(r"^[A-Z]{3}[0-9]{3}$", rec.name):
                raise exceptions.ValidationError(
                    'Car\'s number should start with 3 \
                    capital letters and end with 3 numbers')
                    

    @ api.depends('brand_id')
    def _brand_count(self):
        for record in self:
            record.brands_at_garage = len(self.search(
                [('brand_id', '=', record.brand_id.id)]))
        # self.brands_at_garage = len(self.search([('brand_id', '=', self.brand_id.id)])) works too

    # kai belekur reiksmes pasikecia ir mes norim reaguoti
    @ api.onchange('car_active')
    def _set_end_date(self):
        if not self.car_active:
            self.date_to = fields.Date.today()

    def start_parking(self):
        self.park_start = datetime.now()
        self.write({'state': 'parked'})
        return True

    def end_parking(self):
        self.park_end = datetime.now()
        self.park_time = self.calculate_parking(self.park_start, self.park_end)
        self.write({'state': 'finished'})
        return True

    def calculate_parking(self, park_start, park_end):
        return float((park_end - park_start).total_seconds()) / 3600

    # 1. Kai vartotas iveda automobili, reikia galimybes priskirti automobilio modeli.
    # 2. Reikia nurodyti automobilio kubatura.

    # 1. Kai ivedamas automobilis vartotojas privalo pasirinkti model
    # 2. kai vartotojas iveda automobilio marke reikia, kad model butu pasirenkamas is tos markes modeliu.

    # 1. kai vartotojas iveda automobilio numeri ir marke reikia parodyti kelintas tos markes automobilis bus registruotas aiskteleje
    # 2. vartotjas turi galimybe pazymeti automobili kaip neaktyvu
    # 3. kai automobilis pazymetas neaktvyiu tai jo valid to data yra siandiena

    # 1. vartotojas nori mygtuko paspaudimu fiksuoti automobilio isvykima ir trukme
