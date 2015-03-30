"use strict";

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

function run_js(ev){
    var code = ev.data.getValue();
    var runner = $('#runner').remove();
    $('body').append('<script id="runner">' + code + '</script>');
}

$(document).ready(function(){
    var cookies = get_cookies();
    // Show errors
    var error = $('#error_placeholder');
    if (error.length > 0 && cookies['error'] !== undefined){
        error.attr('class', error.attr('class').replace('hidden', ''));
        error.text(cookies['error']);
    }

    // Display correct login/logout link
    var login = $('#login');
    var logout = $('#logout');
    var signin = $('#signin');

    if (cookies.username !== undefined) {
        login.remove();
        signin.remove();
        logout.text('Salir (' + cookies.unsafe_name + ')');
    }
    else{
        logout.remove();
    }
});
