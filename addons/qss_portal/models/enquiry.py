from odoo import api, fields, models


class QssEnquiry(models.Model):
    _name = 'qss.enquiry'
    _description = 'QSS Client Enquiry'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Enquiry Reference', required=True, copy=False, default='New', tracking=True)
    client_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True)
    description = fields.Text(string='Requirements')
    state = fields.Selection([
        ('new', 'New'),
        ('quoted', 'Quoted'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled')
    ], default='new', tracking=True)
    quotation_id = fields.One2many('qss.quotation', 'enquiry_id', string='Quotations')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qss.enquiry') or 'New'
        return super().create(vals_list)


