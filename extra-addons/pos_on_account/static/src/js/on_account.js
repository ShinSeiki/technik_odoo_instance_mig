odoo.define('pos_on_account.on_account',function(require){
"use strict";

    var gui = require('point_of_sale.gui');
    var chrome = require('point_of_sale.chrome');
    var core = require('web.core');
    var models = require('point_of_sale.models');
    var pos_screens = require('point_of_sale.screens');
    var PopupWidget = require('point_of_sale.popups');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var _t = core._t;
    var _super_posmodel = models.PosModel.prototype;
    var PosBaseWidget = require('point_of_sale.BaseWidget');

    _super_posmodel.models.splice(10, 0, {
        model: 'sale.order',
        fields: ['id', 'name', 'state', 'partner_id', 'date_order', 'order_line', 'amount_total', 'amount_tax'],
        domain: function(self){ return [['create_from_pos', '=', true]]},
        loaded: function (self, sale_orders) {
            var orders = [];
            for (var i in sale_orders){
                orders[sale_orders[i].id] = sale_orders[i];
            }
            self.sale_orders = orders;
            self.order = [];
            for (var i in sale_orders){
                self.order[i] = sale_orders[i];
            }
        },
    });

    var PaymentScreenWidget = pos_screens.PaymentScreenWidget.include({
        renderElement: function() {
            var self = this;
            this._super();
            this.$('.js_onAccount').click(function(){
                self.click_onAccount();
            });
        },
        click_onAccount: function() {
            var self = this;
            var sale_order = {};
            var order = this.pos.get_order();
            var order_lines = order.get_orderlines();
            var flag_negative = false;
            for (var line in order_lines){
                if (order_lines[line].quantity < 0){
                    flag_negative = true;
                }
            }
            if(flag_negative == true){
                this.gui.show_popup('alert',{
                    'title': _t('Alert: Invalid Order'),
                    'body': _t('Negative Quantity is Not Allowed'),
                });
            }
            else if(order_lines.length == 0 || this.pos.get_order().get_total_with_tax() <=0){
                self.gui.show_popup('confirm',{
                    'title': _t('Please Add Some Order Lines'),
                    'body': _t('You need to add Ordre Lines before you can create order.'),
                    confirm: function(){
                        self.gui.show_screen('products');
                    },
                });
            }
            else if(!order.get_client()){
                self.gui.show_popup('confirm',{
                    'title': _t('Please select the Customer'),
                    'body': _t('You need to select the customer before you can create order on account.'),
                    confirm: function(){
                        self.gui.show_screen('clientlist');
                    },
                });
            }
            else{
                sale_order.order_line = [];
                for (var line in order_lines){
                    if (order_lines[line].quantity>0)
                    {
                        var sale_order_line = [0,false,{product_id:null,product_uom_qty:0}];
                        sale_order_line[2].product_id = order_lines[line].product.id;
                        sale_order_line[2].product_uom_qty = order_lines[line].quantity;
                        sale_order.order_line.push(sale_order_line);
                    }
                }
                sale_order.partner_id = this.pos.get_client().id;
                sale_order.create_from_pos = true;
                rpc.query({
                    model: 'sale.order',
                    method: 'create_order_from_ui',
                    args: [sale_order]
                }).then(function(order_ref){
                    self.pos.delete_current_order();
                    self.gui.show_popup('pos_so_ref',{
                        'body': _t('Sale Order Ref : ')+ order_ref[0] ,
                        'lineData': order_ref[1]
                    });
                });
            }
        }
    });

    var SaleRefPopupWidget = PopupWidget.extend({
        template: 'SaleRefPopupWidget',
        show: function (options) {
            this._super(options);
            this.render_list(options);
            this.pos.load_server_data();
        },
        render_list: function(options){
            var rows = ''
            for(var i = 0; i < options.lineData.length; i++){
                var product = this.pos.db.get_product_by_id(options.lineData[i][2]['product_id']);
                rows += "<tr><td width='60%'>" + product.display_name + "</td><td>" + options.lineData[i][2]['product_uom_qty'] + "</td></tr>";
            }
            this.$('.order-line-data').append($(rows));
        }
    });

    gui.define_popup({name:'pos_so_ref', widget: SaleRefPopupWidget});

    var OnAccountOrderButton = pos_screens.ActionButtonWidget.extend({
        template: 'OnAccountOrderButton',
        button_click: function(){
            if (this.pos.get_order().get_orderlines().length === 0){
                this.gui.show_screen('OnAccountOrdersWidget');
            }
            else{
                this.gui.show_popup('error',{
                    title :_t('Process Only one operation at a time'),
                    body  :_t('Process the current order first'),
                });
            }
        }
    });

    pos_screens.define_action_button({
        'name': 'on_account order',
        'widget': OnAccountOrderButton,
        'condition': function(){
            return this.pos;
        },
    });

    var OnAccountOrdersWidget = pos_screens.ScreenWidget.extend({
        template: 'OnAccountOrdersWidget',

        init: function(parent, options){
            this._super(parent, options);
            this.search_string = "";
        },
        show: function(){
            var self = this;
            this._super();

            this.$('.back').click(function(){
                self.gui.back();
            });
            var sale_orders = this.pos.sale_orders;
            this.render_list(sale_orders);

            var search_timeout = null;

            if(this.pos.config.iface_vkeyboard && this.chrome.widget.keyboard){
                this.chrome.widget.keyboard.connect(this.$('.searchbox input'));
            }

            this.$('.searchbox input').on('keyup',function(event){
                clearTimeout(search_timeout);
                var query = this.value;
                search_timeout = setTimeout(function(){
                    self.perform_search(query,event.which === 13);
                },70);
            });

            this.$('.searchbox .search-clear').click(function(){
                self.clear_search();
            });
        },
        perform_search: function(query, associate_result){
            var new_orders;
            if(query){
                new_orders = this.search_order(query);
                this.render_list(new_orders);
            }else{
                var orders = this.pos.sale_orders;
                this.render_list(orders);
            }
        },
        search_order: function(query){
            var self = this;
            try {
                query = query.replace(/[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g,'.');
                query = query.replace(' ','.+');
                var re = RegExp("([0-9]+):.*?"+query,"gi");
            }catch(e){
                return [];
            }
            var results = [];
            for(var i = 0; i < self.pos.sale_orders.length; i++){
                var r = re.exec(this.search_string);
                if(r){
                    var id = Number(r[1]);
                    results.push(this.get_order_by_id(id));
                }else{
                    break;
                }
            }
            var uniqueresults = [];
            $.each(results, function(i, el){
                if($.inArray(el, uniqueresults) === -1) uniqueresults.push(el);
            });
            return uniqueresults;
        },
        get_order_by_id: function (id) {
            return this.pos.sale_orders[id];
        },
        clear_search: function(){
            var orders = this.pos.sale_orders;
            this.render_list(orders);
            this.$('.searchbox input')[0].value = '';
            this.$('.searchbox input').focus();
        },
        render_list: function(orders){
            var self = this;
            for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
                if (orders[i]) {
                    var order = orders[i];
                    self.search_string += i + ':' + order.partner_id[1] + '\n';
                }
            }
            this.$('.on-account-order-lines').delegate('.on-account-button','click',function(event){
                var order_id = $(this).data('id');
                self.gui.show_popup('OrderAddOnAccountWidget',{
                    ref: order_id
                });
            });
            var contents = this.$el[0].querySelector('.on-account-order-lines');
            if (contents){
                contents.innerHTML = "";
                for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
                    if (orders[i]) {
                        var order = orders[i];
                        var orderline_html = QWeb.render('OnAccountOrderLines', {widget: this, order: order});
                        var orderline = document.createElement('tbody');
                        orderline.innerHTML = orderline_html;
                        orderline = orderline.childNodes[1];
                        contents.appendChild(orderline);
                    }
                }
            }
        },
    });

    gui.define_screen({name:'OnAccountOrdersWidget', widget: OnAccountOrdersWidget});

    var OrderAddOnAccountWidget = PosBaseWidget.extend({
        template: 'OrderAddOnAccountWidget',

        init: function(parent, options){
            this._super(parent, options);
            this.pos_reference = "";
        },
        show: function (options) {
            var self = this;
            this._super(options);
            var sale_orders = this.pos.sale_orders;
            this.render_list(options);

        },
        close: function(){
            if (this.pos.barcode_reader) {
                this.pos.barcode_reader.restore_callbacks();
            }
        },
        events: {
            'click .button.cancel':  'click_cancel',
            'click .button.confirm': 'click_confirm',
        },
        render_list:function(options){
            var order_new = null;
            $("#order-table-body").empty();
            var lines = [];
            this.pos_reference = options.ref;
            rpc.query({
                model: 'sale.order',
                method: 'get_sale_order_lines',
                args: [options.ref],
            }).then(function(result){
                $("#order-table-body").empty();
                lines = result[0];
                for(var j=0;j < lines.length; j++){
                    var product_line = lines[j];
                    var rows = "";
                    var id = product_line.product_id;
                    var price_unit = product_line.price_unit;
                    var name =product_line.product;
                    var qty = product_line.qty;
                    rows += "<tr><td>" + id + "</td><td>" + price_unit +" </td><td>" + name + "</td><td>" + qty + "</td></tr>";
                    $(rows).appendTo("#order-list tbody");
                    var rows = document.getElementById('order-list').rows;
                    for (var row = 0; row < rows.length; row++) {
                        var cols = rows[row].cells;
                        cols[0].style.display = 'none';
                        cols[1].style.display = 'none';
                    }
                }
                var table = document.getElementById('order-list');
                var tr = table.getElementsByTagName("tr");
                for (var i = 1; i < tr.length; i++) {
                  var td = document.createElement('td');
                  var input = document.createElement('input');
                  input.setAttribute("type", "text");
                  input.setAttribute("value", 0);
                  input.setAttribute("id", "text"+i);
                  td.appendChild(input);
                  tr[i].appendChild(td);
                }
            });
        },
         click_confirm: function(){
            var self = this;
            var myTable = document.getElementById('order-list').tBodies[0];
            var c = 1
            for (var r=0, n = myTable.rows.length; r < n; r++) {
                var row = myTable.rows[r];
                var on_account_qty = document.getElementById("text"+c).value;
                var product = this.pos.db.get_product_by_id(row.cells[0].innerHTML);
                if (!product) {
                    return;
                }
                if (on_account_qty > 0){
                    this.pos.get_order().add_product(product, {
                        price: row.cells[1].innerHTML,
                        quantity: (on_account_qty),
                    });
                    var sale_orders = self.pos.sale_orders;
                    var sale_order = [];
                    for(var o = 0, len = Math.min(sale_orders.length,1000); o < len; o++) {
                        if (sale_orders[o] && sale_orders[o].id == self.pos_reference) {
                            sale_order = sale_orders[o];
                        }
                    }
                    this.pos.get_order().set_client(self.pos.db.get_partner_by_id(sale_order.partner_id[0]));
                }
                c = c+1
            }
            this.gui.close_popup();
            self.gui.show_screen('products');
        },
        click_cancel: function(){
            this.gui.close_popup();
        }
    });

    gui.define_popup({name:'OrderAddOnAccountWidget', widget: OrderAddOnAccountWidget});

    return {
        PaymentScreenWidget: PaymentScreenWidget,
        OnAccountOrdersWidget: OnAccountOrdersWidget
    }

});
