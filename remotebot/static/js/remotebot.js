'use strict';


function Server(address, api_key){
    var that = this;
    this.address = address;
    this.api_key = api_key;
    this.authenticated = false;
    this.onConnectFunction = function(){};
    this.next_avail_msg_id = 0;
    this.pending_msgs = {};
    this.pending_count = 0;
    this.delayed = [];

    this.send_ws_msg = function(msg){
        var msg_id = that.next_avail_msg_id++;
        var promise;
        promise = new Promise(function(resolve, reject){
            that.pending_count++;
            that.pending_msgs[msg_id] = {resolve: resolve, reject: reject};
        });
        msg['msg_id'] = msg_id;
        if (that.pending_count <= 1){
            that.ws.send(JSON.stringify(msg));
        }
        else{
            that.delayed.push(JSON.stringify(msg));
        }
        return promise;
    }

    this.authentication_required = function(){
        var promise = that.send_ws_msg(
                {entity: 'global', method: 'authentication_required'});
        return promise;
    };
    this.authenticate = function(api_key){
        var promise = that.send_ws_msg(
                {entity: 'global', method: 'authenticate', args: [api_key,]});
        return promise;
    };
    this.onConnect = function(f){
        this.onConnectFunction = f;
    };
    this.ws = new WebSocket(address);
    this.ws.onopen = function(e){
        that.authentication_required().then(function(required){
            if (required.value){
                rblog('autenticación requerida');
                return that.authenticate(that.api_key);
            }
            else{
                that.onConnectFunction.apply();
                rblog('no se requiere autenticación');
            }
        }).then(function(authenticated){
            if (authenticated.value){
                rblog('autenticado');
                that.authenticated = true;
                that.onConnectFunction.apply();
            }
            else{
                rblog('no autenticado');
                that.authenticated = false;
            }
        });

        rblog('conectado');
    };
    this.ws.onmessage = function(msg){
        // FIXME
        msg = JSON.parse(msg.data);
        rblog(msg);
        that.pending_count--;
        if (msg['msg_id'] !== undefined){
            var executor = that.pending_msgs[msg['msg_id']];
            delete that.pending_msgs[msg['msg_id']];
            executor.resolve(msg);
        }
        else{
            rblog(msg);
        }
        if (that.delayed.length > 0){
            that.ws.send(that.delayed.pop());
        }
    };
    this.ws.onclose = function(e){
        rblog('desconectado');
        that.delayed = [];
        that.pending_msgs = {};
        that.pending_count = 0;
    };
    this.ws.onerror = function(e){
        rblog('error ' + e.data);
    };
}


Server.prototype.get_robots = function(){
    var promise = this.send_ws_msg(
        {entity: 'global', method: 'get_robots'}
    );
    return promise;
}

Server.prototype.fetch_robot = function(){
    var promise = this.send_ws_msg(
        {entity: 'global', method: 'fetch_robot'}
    );
    return promise;
}

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

function println(text){
    var console = $('#console');
    if (typeof text !== 'object'){
        text = String(text);
    }
    else{
        text = JSON.stringify(text);
    }
    console.append(text, '&#10;');
    console.scrollTop(console[0].scrollHeight);
    console.focus();
}

// FIXME
function rblog(text){ println(text); }
// function rblog(){}
