
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


import logging
_logger = logging.getLogger(__name__)


class AutoParking(models.Model):
    _inherit = 'auto.parking'
    _description = 'Auto Parking Duration'
    _rec_name = 'name'
    _order = 'name ASC'

    # rodo rysi atgal i auto tracking ir sitas dabar bus pasiemas auto parking modelyje nes mes ji inheritinom
    tracking_ids = fields.One2many(
        'auto.parking.tracking', 'name',  # sitos duomenu bazes susietos per name integeri
        string='Tracking lines',
    )
    park_note = fields.Text(
        string='Note',
        store=True,
    )
    # feature_ids = fields.Many2many(
    #     'auto.parking.brand.features',
    #     string='Features',
    # )
    park_email = fields.Char(
        string="Email",
        default="opaipa@gmaill.com",
        readonly=True,
    )
    park_phone = fields.Char(
        string="Phone",
        default="+3706655645",
        readonly=True,
    )



    # ovverdininam funkcija

    def start_parking(self):
        # su super mes ivygdom funkcija originaliame modelyje
        res = super(AutoParking, self).start_parking()

        values = {
            'name': self.id,
            'date_from': datetime.now(),
        }
        # per env pasiekiame kita modeli ir jame isaugome irasa istorijos rinkimui
        self.env['auto.parking.tracking'].create(values)

        return res

    def end_parking(self):
        res = super(AutoParking, self).end_parking()
        # randame irasa kuri atnaujinsime
        auto_parking_tracking = self.env['auto.parking.tracking'].search([('name', '=', self.id)], limit=1, order="create_date DESC")

        auto_parking_tracking.write({
            'date_to': datetime.now(),
            'total_park_time': self.calculate_parking(auto_parking_tracking.date_from, datetime.now())
        })
        return res
