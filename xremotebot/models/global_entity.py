# -*- coding: utf8 -*-
'''
Global messages supported by XRemoteBot
'''
import random

from .entity import Entity
from .user import User
from .reservation import Reservation

from xremotebot.configuration import robots, public_server
from xremotebot.lib.exceptions import NoFreeRobots, UnavailableRobot, ReservationNotFound


class Global(Entity):
    def authentication_required(self, wshandler):
        return public_server

    def authenticate(self, wshandler, api_key):
        if public_server:
            wshandler.authenticated = False
            user = User.with_api_key(api_key)
            if user is not None:
                wshandler.set_current_user(user)
            return wshandler.authenticated
        else:
            return True

    def get_robots(self, wshandler):
        avail = []
        for model, id_ in Reservation.available(all_robots=robots):
            avail.append({
                'robot_model': model,
                'robot_id': id_,
            })
        return avail

    def fetch_robot(self, wshandler):
        """
        Returns a newly reserved robot if available, a previously reserved
        robot if not or raises an exception if there are no available and
        no reserved robots for this user.
        """
        nofreerobots = NoFreeRobots('There are no free robots, '
                                    'wait a moment and try again')
        if not public_server:
            try:
                model = random.choice(robots.keys())
                id_ = random.choice(robots[model])
                return {'robot_model': model, 'robot_id': id_}
            except IndexError:
                raise nofreerobots

        robot = Reservation.reserve_any(wshandler.current_user)
        if robot is not None:
            return {
                'robot_model': robot.robot_model,
                'robot_id': robot.robot_id,
            }
        elif len(wshandler.current_user.reservations) > 0:
            previous = wshandler.current_user.reservations[0]
            return {
                'robot_model': previous.robot_model,
                'robot_id': previous.robot_id,
            }

        raise nofreerobots

    def reserve(self, wshandler, model, id_,time):
        reservation = Reservation.reserve(
            robot_id=id_,
            robot_model=model,
            time=time
        )
        if reservation is None:
            raise UnavailableRobot('Unavailable robot {}:{}'.format(model, id_))

        return {'robot_model': reservation.robot_model, 'robot_id': reservation.robot_id, 'time': time, 'reservation_id':reservation.id}


    def release(self,wshandler,reservation_id):
        Reservation.release(reservation_id)
        return {'reservation_id': reservation_id}
