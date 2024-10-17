FROM dockersit1/sit_ce:13.0-tnk.3

USER root

RUN apt-get update
RUN apt-get install -y xmlstarlet

RUN xmlstarlet ed -L -u "/odoo/data/record/field[@name='active']/@eval" -v "False" /usr/lib/python3/dist-packages/odoo/addons/mail_notification/views/ir_cron.xml

#RUN apt-get install -y gettext

#COPY tmpl.conf /etc/odoo
#COPY entrypoint.sh /
#RUN chmod +x /entrypoint.sh
#RUN ls -l /

#USER odoo

#ENTRYPOINT [ "/entrypoint.sh" ]
#CMD ["odoo"]
