from odoo import fields, models


class TrainingTask(models.Model):
    _name = "training.task"
    _description = "Training Task"
    _order = "id desc"

    name = fields.Char(string="Task", required=True)
    description = fields.Text(string="Description")
    rules = fields.Html(
        string="Hostel Rules",
        sanitize=True,
        default="""
            <p><strong>အဆောင်စည်းကမ်းများ</strong></p>
            <ul>
                <li>အခန်းကို သန့်ရှင်းစွာထားရမည်။</li>
                <li>ည ၁၀ နာရီမတိုင်မီ ပြန်ရောက်ရမည်။</li>
                <li>အဆောင်ပိုင်ပစ္စည်းများကို ထိန်းသိမ်းရမည်။</li>
            </ul>
        """,
    )
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
