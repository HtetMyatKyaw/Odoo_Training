from odoo import fields, models


class TrainingTask(models.Model):
    _name = "training.task"
    _description = "Training Task"
    _order = "id desc"

    name = fields.Char(string="Task", required=True)
    description = fields.Text(string="Description")
    deadline = fields.Date(string="Deadline")

    user_id = fields.Many2one(
        "res.users", string="Assigned To", default=lambda self: self.env.user
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancel"),
        ],
        default="draft",
    )

    def action_start(self):
        for record in self:
            record.state = "in_progress"

    def action_done(self):
        for record in self:
            record.state = "done"
