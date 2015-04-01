'use strict';


function Server(address, api_key){
    var that = this;
    this.address = address;
    this.api_key = api_key;
    this.authenticated = false;
    this.onConnectFunction = function(){};
    this.next_avail_msg_id = 0;
    this.last_response_msg_id = -1;
    this.pending_msgs = {};
    this.pending_count = 0;
    this.delayed = [];

    this.send_ws_msg = function(msg){
        var msg_id = that.next_avail_msg_id++;
        var promise;
        msg['msg_id'] = msg_id;
        msg = JSON.stringify(msg);

        that.delayed.push(msg);

        promise = new Promise(function(resolve, reject){
            that.pending_msgs[msg_id] = {resolve: resolve, reject: reject};
        });

        rblog(msg);
        if (that.last_response_msg_id + 1 == msg_id){
            that.ws.send(that.delayed.shift());
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
            if (required){
                rblog('autenticación requerida');
                return that.authenticate(that.api_key);
            }
            else{
                that.onConnectFunction.apply();
                rblog('no se requiere autenticación');
            }
        }).then(function(authenticated){
            if (authenticated){
                rblog('autenticado');
                that.authenticated = true;
                that.onConnectFunction.apply();
            }
            else{
                rblog('no autenticado');
                that.authenticated = false;
            }
        }).catch(function(msg){
            alert('Conectándose con el servidor: ' + msg);
        });

        rblog('conectado');
    };
    this.ws.onmessage = function(msg){
        // FIXME
        msg = JSON.parse(msg.data);
        rblog(msg);
        if (msg['msg_id'] !== undefined){
            var executor = that.pending_msgs[msg['msg_id']];
            delete that.pending_msgs[msg['msg_id']];
            that.last_response_msg_id = msg['msg_id']
            if (msg.response === 'value'){
                executor.resolve(msg.value);
            }
            else{
                executor.reject(msg.message);
            }
        }
        else{
            println(msg);
        }
        if (that.delayed.length > 0){
            that.ws.send(that.delayed.shift());
        }
    };
    this.ws.onclose = function(e){
        rblog('desconectado');
        that.delayed = [];
        that.pending_msgs = {};
        that.pending_count = 0;
    };
    this.ws.onerror = function(e){
        println('error ' + e.data);
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

Server.prototype.reserve = function(model, id){
    var promise = this.send_ws_msg(
        {entity: 'global', method: 'reserve', args: [model, id]}
    );
    return promise;
};

function Robot(server, robot_obj){
    var that = this;
    // FIXME
    rblog('Creating local instance of robot');
    if (robot_obj === undefined){
        rblog('robot_obj is undefined');
    }
    rblog(robot_obj);

    this.server = server;
    this.robot_id = robot_obj.robot_id;
    this.robot_model = robot_obj.robot_model;
}

Robot.prototype._send = function(){ // message, *args
    var message = arguments[0];
    var i, args = [({'robot_model': this.robot_model, 'robot_id': this.robot_id})];
    var first, second;
    var that = this;
    for (i = 1; i < arguments.length; i++){
        args.push(arguments[i]);
    }
    return this.server.send_ws_msg({
        entity: 'robot',
        method: message,
        args: args,
    });
};



Robot.prototype.forward = function(speed, time){
    return this._send('forward', speed, time);
};

Robot.prototype.backward = function(speed, time){
    return this._send('backward', speed, time);
};

Robot.prototype.turnLeft = function(speed, time){
    return this._send('turnLeft', speed, time);
};

Robot.prototype.turnRight = function(speed, time){
    return this._send('turnLeft', speed, time);
};

Robot.prototype.getObstacle = function(){
    return this._send('getObstacle');
};

Robot.prototype.getLine = function(){
    return this._send('getLine');
};

Robot.prototype.ping = function(){
    return this._send('ping');
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
    // console.focus();
}

// FIXME
function rblog(text){ println(text); }
// function rblog(){}
