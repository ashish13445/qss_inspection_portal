from odoo import api, fields, models


class QssVisitReport(models.Model):
    _name = 'qss.visit.report'
    _description = 'QSS Visit Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Visit Report Number', required=True, copy=False, default='New', tracking=True)
    inspection_call_id = fields.Many2one('qss.inspection.call', string='Inspection Call', required=True, ondelete='cascade')
    engineer_id = fields.Many2one('res.users', string='Inspection Engineer')
    report_file = fields.Binary(string='Report Document')
    report_filename = fields.Char()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('review', 'Under Review'),
        ('approved', 'PM Approved'),
        ('final', 'Finalized')
    ], default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qss.visit.report') or 'New'
        return super().create(vals_list)

    def action_submit_report(self):
        """Submit report for review"""
        self.ensure_one()
        if self.report_file:
            self.state = 'submitted'
            # Notify engineering coordination team
            self.message_post(
                body=f"Visit Report {self.name} has been submitted for review by {self.engineer_id.name}",
                message_type='notification'
            )
        return True

    def action_mark_reviewed(self):
        """Mark report as reviewed by coordinator"""
        self.ensure_one()
        self.state = 'review'
        return True

    def action_approve(self):
        """Approve report by project manager"""
        self.ensure_one()
        self.state = 'approved'
        return True

    def action_finalize(self):
        """Finalize report for client submission"""
        self.ensure_one()
        self.state = 'final'
        # Notify operations team
        self.message_post(
            body=f"Visit Report {self.name} has been finalized and ready for client submission",
            message_type='notification'
        )
        return True


