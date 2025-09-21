from odoo import api, fields, models

class QssInvoice(models.Model):
    _name = 'qss.invoice'
    _description = 'QSS Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Invoice Number', required=True, copy=False, default='New', tracking=True)
    quotation_id = fields.Many2one('qss.quotation', string='Quotation', required=True, ondelete='cascade', tracking=True)
    client_id = fields.Many2one(related='quotation_id.client_id', store=True, readonly=True)
    project_number_id = fields.Many2one(related='quotation_id.project_number_id', store=True, readonly=True)
    amount_total = fields.Monetary(string='Total Amount', currency_field='currency_id', related='quotation_id.amount_total', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('posted', 'Posted'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], default='draft', tracking=True)
    invoice_file = fields.Binary(string='Invoice Document')
    invoice_filename = fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qss.invoice') or 'New'
        return super().create(vals_list)
