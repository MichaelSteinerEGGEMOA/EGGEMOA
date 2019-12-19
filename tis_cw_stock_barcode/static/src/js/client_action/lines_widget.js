odoo.define('tis_cw_stock_barcode.LinesWidget', function (require) {
'use strict';

var core = require('web.core');
var Widget = require('web.Widget');
var LinesWidget = require('stock_barcode.LinesWidget');

var QWeb = core.qweb;
LinesWidget.include({

    incrementProduct: function(id_or_virtual_id, qty, model, doNotClearLineHighlight) {
        this._super.apply(this, arguments);
        var $line = this.$("[data-id='" + id_or_virtual_id + "']");
        if (model === 'stock.picking'){
            var incrementcwClass = '.cw-qty-done';
        }
        var cwqtyDone = parseInt($line.find(incrementcwClass).text(), 10);
        $line.find(incrementcwClass).text(cwqtyDone + qty);
    },
});

return LinesWidget;

});
