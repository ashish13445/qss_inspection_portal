from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    project_number_id = fields.Many2one('qss.project.number', string='Project Unique Number')
