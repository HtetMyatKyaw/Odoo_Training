from odoo import fields, models


class QuickTaskWizard(models.TransientModel):
    _name = "training.task.quick.wizard"
    _description = "Quick Task Wizard"

    name = fields.Char(string="Task", required=True)
    description = fields.Text(string="Description")

    def action_create_task(self):
        self.ensure_one()
        task = self.env["training.task"].create({
            "name": self.name,
            "description": self.description,
        })
        return {
            "type": "ir.actions.act_window",
            "name": "Task",
            "res_model": "training.task",
            "view_mode": "form",
            "res_id": task.id,
            "target": "current",
        }
