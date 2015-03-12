'use strict';


function Server(address, api_key){
    var that = this;
    this.ws = new WebSocket(address);
    this.ws.onopen = function(e){
        that.ws.send(JSON.stringify({entity: 'global', method: 'hello'}));
        alert('conectado');
    };
    this.ws.onmessage = function(e){
        alert(e.data);
    };
    this.ws.onclose = function(e){
        alert('desconectado');
    };
    this.ws.onerror = function(e){
        alert('error ' + e.data);
    };
    function hello(){
        that.ws.send(json.dumps({entity: 'global', method: 'hello'}));
    }
}

//Server.prototype.fetch_robot = function

function Constructor() {
    // Miembros privados
    var that = this;
    var x = 20;

    // Miembro público
    this.y = x;

    function metodo_privado() {
        return that;
    }

    this.metodo_privilegiado = function () {
        return that.x;
    };
}

Constructor.prototype.metodo_publico = function () {
    return this.y;
};

function Child() { }
Child.prototype = new Constructor();
Child.prototype.constructor = Child;
