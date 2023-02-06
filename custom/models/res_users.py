from odoo import api, fields, models


class ColleagueUser(models.Model):
    _inherit = "res.users"

    project_task_ids = fields.Many2many("project.task", relation="project_task_user_rel",
                                        column1="user_id", column2="task_id")
    colleague_user_ids = fields.Many2many("res.users", relation="res_users_colleagues_rel",
                                          column1="user_id", column2="coll_user_id",
                                          string="Colleagues", compute="_compute_colleagues", store=True)

    @api.depends("project_task_ids", "project_task_ids.project_id",
                 "project_task_ids.project_id.task_ids", "project_task_ids.project_id.task_ids.user_ids")
    def _compute_colleagues(self):
        # Prefetch fields.
        self.mapped("project_task_ids.project_id.task_ids")._read(["user_ids"])
        for user in self:
            user.colleague_user_ids = user.project_task_ids.mapped("project_id.task_ids.user_ids") + user

