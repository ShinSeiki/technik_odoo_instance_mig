# -*- coding: utf-8 -*-
# from odoo import http


# class MailNotification(http.Controller):
#     @http.route('/mail_notification/mail_notification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mail_notification/mail_notification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mail_notification.listing', {
#             'root': '/mail_notification/mail_notification',
#             'objects': http.request.env['mail_notification.mail_notification'].search([]),
#         })

#     @http.route('/mail_notification/mail_notification/objects/<model("mail_notification.mail_notification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mail_notification.object', {
#             'object': obj
#         })
