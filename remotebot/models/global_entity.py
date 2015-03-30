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
from remotebot.lib.exceptions import NoFreeRobots


class Global(Entity):
    def authentication_required(self, wshandler):
        return True

    def authenticate(self, wshandler, api_key):
        wshandler.authenticated = False
        user = User.with_api_key(api_key)
        if user is not None:
            wshandler.set_current_user(user)

        return wshandler.authenticated

    def get_robots(self, wshandler):
        # FIXME: cotejar con reservas actuales, mostrar libres y reservados
        # por el usuario actual
        avail = {}
        for model, id_ in Reservation.available(all_robots=robots):
            avail[model] = id_
        return avail

    def fetch_robot(self, wshandler):
        """
        Returns a newly reserved robot if available, a previously reserved
        robot if not or raises an exception if there are no available and
        no reserved robots for this user.
        """
        robot = Reservation.reserve_any(wshandler.current_user)
        if robot is not None:
            return {robot.robot_model: robot.robot_id}
        elif len(wshandler.current_user.reservations) > 0:
            previous = wshandler.current_user.reservations[0]
            return {previous.robot_model: previous.robot_id}

        raise NoFreeRobots('There are no free robots, '
                           'wait a moment and try again')

    def reserve(self, wshandler, robot):
        reservation = Reservation.reserve(
            robot_id=robot['id'],
            robot_model=robot['model']
        )
        return reservation
