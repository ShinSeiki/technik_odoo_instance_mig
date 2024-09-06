odoo.define('custom_background.BackgroundManager', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');

    var BackgroundManager = core.Class.extend({
        init: function () {
            this.updateBackground();
        },

        updateBackground: function () {
            var self = this;
            ajax.rpc('/web/dataset/call_kw/res.config.settings/get_values', {
                model: 'res.config.settings',
                method: 'get_values',
                args: [],
                kwargs: {},
            }).then(function (result) {
                if (result.background_image) {
                    $('body').css({
                        'background-image': 'url(data:image/png;base64,' + result.background_image + ')',
                        'background-repeat': 'no-repeat',
                        'background-attachment': 'fixed',
                        'background-size': 'cover'
                    });
                }
            });
        }
    });

    core.bus.on('web_client_ready', null, function () {
        new BackgroundManager();
    });

    return BackgroundManager;
});
