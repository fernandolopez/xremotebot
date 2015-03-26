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

import json
import traceback


class ServerException(Exception):
    def __init__(self, originalException):
        Exception.__init__(self, originalException)
        self.originalName = repr(originalException)
        self.stackTrace = traceback.format_exc()

    def dumpJSON(self):
        return json.dumps({
            'type': 'exception',
            'name': self.originalName,
            'stacktrace': self.stackTrace
            })
