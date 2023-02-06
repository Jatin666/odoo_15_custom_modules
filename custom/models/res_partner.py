from odoo import api, models


class ColleaguePartner(models.Model):
    _inherit = "res.partner"

    def _get_channels_as_member(self):
        channels = super(ColleaguePartner, self)._get_channels_as_member()
        allowed_partners_ids = channels.env.user.colleague_user_ids.mapped("partner_id") - channels.env.user.partner_id
        non_colleagues = channels.with_context(prefetch_fields=False, active_test=False).filtered_domain(
            [("channel_type", "=", "chat"), ("channel_partner_ids", "not in", allowed_partners_ids.ids)])
        return channels - non_colleagues

    @api.model
    def im_search(self, name, limit=20):
        res = super(ColleaguePartner, self).im_search(name, limit)
        if res and not self.env.user._is_system():
            colleague_ids = self.env.user.colleague_user_ids.ids
            res = [vals for vals in res if vals.get("user_id") in colleague_ids]
        return res
