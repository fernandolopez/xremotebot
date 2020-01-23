'''Index of the site returns a list of reserved robots'''
import tornado.web
from .base_handler import BaseHandler
from xremotebot.models.reservation import Reservation
import xremotebot.configuration as conf
from datetime import datetime, timedelta


class IndexHandler(BaseHandler):

    def get(self):
        now = datetime.now()
        until = now
        robots = {}
        for model, ids in conf.robots.items():
            robots[model] = []
            for id_ in ids:
                # Reservation.reserved_by_any_user() doesn't work correctly
                # reservations = Reservation.reserved_by_any_user(
                #    model,
                #    id_,
                #    now,
                #    until
                #)
                # FIXME:
                reservations = []
                if len(reservations) > 0:
                    late = max(map(lambda r: r.date_to, reservations))
                    robots[model].append((id_, late))
                else:
                    robots[model].append((id_, None))
        self.render('index.html', robots=robots)
