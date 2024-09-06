odoo.define('pos_order_transfer.pos_order_transfer', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var _t = core._t;

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var self = this;
            models.load_fields('pos.config', ['pos_type']);
            _super_posmodel.initialize.apply(this, arguments);
        },
    });

    var PaymentScreenWidget = screens.PaymentScreenWidget;
    screens.PaymentScreenWidget.include({
        renderElement: function() {
            var self = this;
            this._super();
            if (this.pos.config.pos_type === 'order_only') {
                this.$('.next').text(_t('Enviar Pedido a Caja'));
            }
        },
        validateOrder: function(force_validation) {
            if (this.pos.config.pos_type === 'order_only') {
                this.transferOrder();
            } else {
                this._super(force_validation);
            }
        },
        transferOrder: function() {
            var self = this;
            this.pos.db.get_available_cashiers().then(function(cashiers) {
                if (cashiers.length === 1) {
                    self.sendOrderToCashier(cashiers[0]);
                } else if (cashiers.length > 1) {
                    self.showPopup('SelectCashierPopup', {
                        title: _t('Seleccionar Caja'),
                        list: cashiers,
                        confirm: function(cashier) {
                            self.sendOrderToCashier(cashier);
                        },
                    });
                } else {
                    self.showPopup('ErrorPopup', {
                        title: _t('Error'),
                        body: _t('No hay cajas disponibles para transferir el pedido.'),
                    });
                }
            });
        },
        sendOrderToCashier: function(cashier) {
            var order = this.pos.get_order();
            var order_data = order.export_as_JSON();
            this.pos.db.save_transferred_order(order_data, cashier.id).then(function() {
                order.destroy();
            });
        },
    });
});
