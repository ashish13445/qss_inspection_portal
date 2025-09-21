from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class QssInspectionCall(models.Model):
    _name = 'qss.inspection.call'
    _description = 'QSS Inspection Call'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Fields
    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        default='New',
        tracking=True
    )
    project_number_id = fields.Many2one(
        'qss.project.number',
        string='Project Unique Number',
        required=True
    )
    client_id = fields.Many2one(
        related='project_number_id.client_id',
        store=True,
        readonly=True
    )
    manufacturer_name = fields.Char(required=True)
    manufacturer_address = fields.Text()
    manufacturer_contact = fields.Char()
    client_contact = fields.Char()
    special_instructions = fields.Text()
    po_copy = fields.Binary(string='Client->Manufacturer PO')
    drawings = fields.Binary(string='Applicable Drawings/Specs')
    data_sheet = fields.Binary(string='Data Sheet/QAP')

    # Status
    state = fields.Selection([
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], default='new', tracking=True)

    # Engineer assignment
    assigned_engineer_id = fields.Many2one(
        'res.users',
        string='Assigned Engineer',
        tracking=True
    )

    # Visit reports
    visit_report_id = fields.One2many(
        'qss.visit.report',
        'inspection_call_id',
        string='Visit Reports'
    )

    # -------- OVERRIDES --------
    @api.onchange('assigned_engineer_id')
    def _onchange_assigned_engineer_id(self):
        try:
            group = self.env.ref('qss_portal.group_qss_inspection_engineer', raise_if_not_found=False)
            if not group:
                _logger.warning("QSS Inspection Engineer group not found.")
                return {}
            
            _logger.info("Filtering assigned_engineer_id using group_id: %s", group.id)
            return {'domain': {'assigned_engineer_id': [('groups_id', 'in', [group.id])]}}
        
        except Exception as e:
            _logger.exception("Error in _onchange_assigned_engineer_id: %s", e)
            return {}


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qss.inspection.call') or 'New'
        return super().create(vals_list)

    # -------- ACTIONS --------
    def action_assign_engineer(self):
        self.ensure_one()
        if self.assigned_engineer_id:
            self.state = 'assigned'
            visit_report = self.env['qss.visit.report'].create({
                'inspection_call_id': self.id,
                'engineer_id': self.assigned_engineer_id.id,
            })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Visit Report Created',
                'res_model': 'qss.visit.report',
                'res_id': visit_report.id,
                'view_mode': 'form',
                'target': 'current',
            }
        return False
