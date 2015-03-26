# -*- encoding: utf-8 -*-
#  remotebot, Python web server for remote interaction with duinobot API.
#  Copyright (C) 2012  Fernando E. M. López <flopez AT linti.unlp.edu.ar>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from duinobot import *
# from libraries.mock_robot import *
try:
    from serial.serialutil import SerialException
except ImportError:
    class SerialException(Exception):
        pass

import json
from errors import ServerException

__robot = {}
__board = {}


def robot_execute(message):
    boardid = message['board']['device']
    robotid = (boardid, message['id'])
    if message['command'] == '__init__':
        if boardid in __board and robotid not in __robot:
            __robot[robotid] = Robot(__board[boardid], message['id'])
    else:
        return getattr(__robot[robotid], message['command'])(*message['args'])
    return None


def board_execute(message):
    device = message['board']['device'].strip()
    if message['command'] == '__init__':
        if device not in __board:
            __board[device] = Board(device)
    else:
        return getattr(__board[device], message['command'])(*message['args'])
    return None


def module_execute(message):
    # print message
    if message['command'] == 'boards':
        return boards(*message['args'])
    elif message['command'] == 'joysticks':
        return joysticks(*message['args'])
    return None


__handler = {
    'robot': robot_execute,
    'board': board_execute,
    'module': module_execute
}


def execute(form):
    returnList = []
    print(form)
    try:
        command = '\n'.join(form["commands"])
        cmdList = json.loads(command)
        for cmdObject in cmdList:
            if 'args' not in cmdObject:
                cmdObject['args'] = ()
            returnList.append(__handler[cmdObject["target"]](cmdObject))
    except (TypeError, ValueError, KeyError, SerialException, NameError) as e:
        raise ServerException(e)

    return json.dumps({
        'type': 'returnvalues',
        'values': returnList
        })

    def free():
        for each in __board.values():
            each.exit()
