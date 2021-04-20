# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                   #
###############################################################################

from odoo import SUPERUSER_ID, api

def migrate(cr, version):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        bad_rule = env['ir.model.access'].search([('name', '=', 'auto parking'), ('group_id', '=', False)])
        bad_rule.unlink()
