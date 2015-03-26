# -*- coding: utf8 -*-
'''
Global messages supported by XRemoteBot
'''
from .entity import Entity
from .user import User
from .reservation import Reservation
# FIXME
# from .robot import Robot

from remotebot.configuration import robots
from remotebot.lib.message import value

class Global(Entity):
    def authentication_required(self, wshandler, msg_id):
        return value(True, msg_id=msg_id)

    def authenticate(self, wshandler, msg_id, api_key):
        wshandler.authenticated = False
        user = User.with_api_key(api_key)
        if user is not None:
            wshandler.set_current_user(user)

        return value(wshandler.authenticated, msg_id=msg_id)

    def get_robots(self, wshandler, msg_id):
        # FIXME: cotejar con reservas actuales, mostrar libres y reservados
        # por el usuario actual
        avail = {}
        for model, id_ in Reservation.available(all_robots=robots):
            avail[model] = id_
        return value(avail, msg_id=msg_id)

    def fetch_robot(self, wshandler, msg_id):
        robot = wshandler.current_user.reserve_any()
        return value({
            robot.robot_model: robot.robot_id,
            }, msg_id=msg_id)
