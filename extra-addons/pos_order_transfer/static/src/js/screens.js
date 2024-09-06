odoo.define('pos_order_transfer.screens', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var _t = core._t;

    var SelectCashierPopupWidget = screens.ConfirmPopupWidget.extend({
        template: 'SelectCashierPopup',
        show: function(options){
            options = options || {};
            this._super(options);

            this.list = options.list || [];
            this.renderElement();

            this.$('.item').click(function(){
                var cashier_id = $(this).data('id');
                var cashier = _.find(self.list, function(item){ return item.id === cashier_id; });
                options.confirm.call(self, cashier);
            });
        },
    });
    gui.define_popup({name:'SelectCashierPopup', widget: SelectCashierPopupWidget});
});
