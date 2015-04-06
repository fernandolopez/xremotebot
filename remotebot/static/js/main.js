"use strict";

var _tips = [
    'Todos los métodos de los robots usan Promises, aprendé a usar la función then en la documentación',
    'Para repetir acciones con el robot es preferible usar setInterval en lugar de while o for, aprendé por qué en la documentación',
    'Usá setTimeout y setInterval en lugar de window.setTimeout y window.setInterval. Aprendé por qué en la documentación',

];

function get_cookies(){
    var obj = {};
    var key, value, kv;
    document.cookie.split(';').forEach(function(each){
        kv = each.split('=');
        if (kv.length >= 2){  // In safe cookies = is allowed in the value
            key = kv[0].trim();
            value = decodeURIComponent(kv[1].trim()).replace(/\+/g, ' ');
            obj[key] = value;
        }
    });
    return obj;
}

// Wrap setInterval and setTimeout to cleanup when running a new script
var _timeouts = [];
var _intervals = [];
var code_wrapper = '\n\
(function(){\n\
    function setInterval(func, time){\n\
        var interval = window.setInterval(func, time);\n\
        _intervals.push(interval);\n\
        return interval;\n\
    }\n\
    function setTimeout(func, time){\n\
        var timeout = window.setTimeout(func, time);\n\
        _timeouts.push(timeout);\n\
        return timeout;\n\
    }\n\
';
var code_wrapper_end = '\n})();'

function run_js(ev){
    var code = ev.data.getValue();
    var runner = $('#runner').remove();

    _timeouts.forEach(function(tout){
        clearTimeout(tout);
    });
    _intervals.forEach(function(inter){
        clearInterval(inter);
    });

    $('body').append('<script id="runner">' +
                     code_wrapper +
                     code +
                     code_wrapper_end +
                     '</script>');
}

$(document).ready(function(){
    var cookies = get_cookies();
    // Show errors
    var error = $('#error_placeholder');
    if (error.length > 0 && cookies['error'] !== undefined){
        error.attr('class', error.attr('class').replace('hidden', ''));
        error.text(cookies['error']);
    }

    if (cookies['form_next_redirect'] !== undefined){
        $('#form_next_redirect').text(cookies['form_next_redirect']);
    }

    // Display correct login/logout link
    if (cookies.username !== undefined && cookies.username !== null) {
        $('#login').remove();
        $('#signin').remove();
        $('#user_dropdown_title').html(
            escape(cookies.unsafe_name) + ' <span class="caret"></span>');
    }
    else{
        $('#user_dropdown').remove();
    }

    // Show tips
    var _tip_index = 1;
    $('#tips').text(_tips[0]);
    setInterval(function(){
        $('#tips').text(_tips[_tip_index]);
        _tip_index = (_tip_index + 1) % _tips.length;
    }, 10000);

});
