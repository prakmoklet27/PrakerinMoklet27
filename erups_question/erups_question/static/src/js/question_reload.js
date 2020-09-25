odoo.define('question.reload', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var widget_registry = require('web.widget_registry');

    var QuestionReload = Widget.extend({
        selector: '.o_erups_question',
        template: 'SwitchCompanyMenu',

        _pollCount: 0,

        start: function() {
            console.log("pet store home page loaded");
        },

        init: function() {
            console.log('hello world');
            this.poll();
            return this._super.apply(this, arguments);
        },

        startPolling: function () {
            var timeout = 3000;
            //
            if(this._pollCount >= 10 && this._pollCount < 20) {
                timeout = 10000;
            }
            else if(this._pollCount >= 20) {
                timeout = 30000;
            }
            //
            setTimeout(this.poll.bind(this), timeout);
            this._pollCount ++;
        },
        poll: function () {
            var self = this;
            console.log('reload');
//            window.location.reload();
            self.startPolling();
        },
    });

    console.log('merdeka cak!');
})