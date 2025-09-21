from odoo import api, fields, models


class QssProjectNumber(models.Model):
    _name = 'qss.project.number'
    _description = 'QSS Project Unique Number'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Unique Number', required=True, copy=False, default='New', tracking=True)
    client_id = fields.Many2one('res.partner', string='Client', required=True)
    project_name = fields.Char(string='Project Name', required=True)
    quotation_id = fields.Many2one('qss.quotation', string='Quotation', ondelete='set null')
    state = fields.Selection([
        ('new', 'New'),
        ('active', 'Active'),
        ('closed', 'Closed')
    ], default='new', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qss.project.number') or 'New'
        return super().create(vals_list)


