from odoo import api, fields, models


class QssPayment(models.Model):
    _name = 'qss.payment'
    _description = 'QSS Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Payment Reference', required=True, copy=False, default='New', tracking=True)
    project_number_id = fields.Many2one('qss.project.number', string='Project Unique Number', required=True)
    invoice_reference = fields.Char(string='Invoice Reference')
    amount = fields.Monetary(string='Amount', currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
    utr_number = fields.Char(string='NEFT/UTR Number', tracking=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid')
    ], default='pending', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qss.payment') or 'New'
        return super().create(vals_list)


