'use strict';

var next_avail_msg_id = 0;
var pending_msgs = {};

function send_ws_msg(ws, msg){
    var msg_id = next_avail_msg_id++;
    var promise;
    promise = new Promise(function(resolve, reject){
        pending_msgs[msg_id] = {resolve: resolve, reject: reject};
    });
    msg['msg_id'] = msg_id;
    ws.send(JSON.stringify(msg));
    return promise;
}

function Server(address, api_key){
    var that = this;
    this.address = address;
    this.api_key = api_key;
    this.authenticated = false;
    this.authentication_required = function(){
        var promise = send_ws_msg(that.ws,
                {entity: 'global', method: 'authentication_required'});
        return promise;
    };
    this.authenticate = function(api_key){
        var promise = send_ws_msg(that.ws,
                {entity: 'global', method: 'authenticate', args: [api_key,]});
        return promise;
    }
    this.ws = new WebSocket(address);
    this.ws.onopen = function(e){
        that.authentication_required().then(function(required){
            if (required.value){
                alert('autenticación requerida');
                return that.authenticate(that.api_key);
            }
            else{
                alert('no se requiere autenticación');
            }
        }).then(function(authenticated){
            if (authenticated.value){
                alert('autenticado');
                that.authenticated = true;
            }
            else{
                alert('no autenticado');
                that.authenticated = false;
            }
        });

        alert('conectado');
    };
    this.ws.onmessage = function(msg){
        // FIXME
        msg = JSON.parse(msg.data);
        console.log(msg);
        if (msg['msg_id'] !== undefined){
            var executor = pending_msgs[msg['msg_id']];
            delete pending_msgs[msg['msg_id']];
            executor.resolve(msg);
        }
        else{
            console.log(msg);
        }
    };
    this.ws.onclose = function(e){
        alert('desconectado');
    };
    this.ws.onerror = function(e){
        alert('error ' + e.data);
    };
}


//Server.prototype.fetch_robot = function
Server.prototype.get_robots = function(){}

//Server.prototype.reserve = function

function Robot(id, server){
    var that = this;
    this.server = server;
    server.reserve(id);
    this.id = id;
}

Robot.prototype._send = function(){ // message, *args
    var message = arguments[0];
    var i, args = [];
    for (i = 1; i < arguments.length; i++){
        args.push(arguments[i]);
    }
    this.server.ws.send(JSON.stringify({
        entity: 'robot',
        message: message,
        args: args,
    }));
};

Robot.prototype.forward = function(speed, time){
    this._send('forward', speed, time);
};

Robot.prototype.backward = function(speed, time){
    this._send('backward', speed, time);
};

Robot.prototype.turnLeft = function(speed, time){
    this._send('turnLeft', speed, time);
};

Robot.prototype.turnRight = function(speed, time){
    this._send('turnRight', speed, time);
};

