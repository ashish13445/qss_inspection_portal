from odoo import api, fields, models


class QssQuotation(models.Model):
    _name = 'qss.quotation'
    _description = 'QSS Quotation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Quotation Number', required=True, copy=False, default='New', tracking=True)
    enquiry_id = fields.Many2one('qss.enquiry', string='Enquiry', required=True, ondelete='cascade', tracking=True)
    client_id = fields.Many2one(related='enquiry_id.client_id', store=True, readonly=True)
    amount_total = fields.Monetary(string='Total Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancelled'),
    ], default='draft', tracking=True)
    approved_work_order = fields.Binary(string='Client Work Order')
    approved_work_order_filename = fields.Char()

    project_number_id = fields.Many2one('qss.project.number', string='Project Unique Number', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qss.quotation') or 'New'
        return super().create(vals_list)
    

    def action_create_invoice(self):
        """Create a customer invoice from approved quotation/work order"""
        self.ensure_one()  # make sure only one record is processed

        invoice_vals = {
            'move_type': 'out_invoice',  # customer invoice
            'partner_id': self.client_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_origin': self.name,
            'project_number_id': self.project_number_id.id,  # custom field
            
        }
        
        invoice = self.env['account.move'].create(invoice_vals)

        # Optional: Notify operations team
        # invoice.message_post(
        #     body=f"Invoice {invoice.name} created for Project {self.project_number_id.name}",
        #     subtype='mail.mt_comment'
        # )

        # Open the newly created invoice form
        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }



