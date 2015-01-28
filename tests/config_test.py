#!/usr/bin/env python3
import unittest
from remotebot.lib import config
import io

class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.cfgstr = io.StringIO(
            'secret = "{}"\n'.format('x' * 40)
        )

    def appendcfg(self, lines):
        self.cfgstr.seek(0, 2)
        self.cfgstr.write(lines)
        self.cfgstr.seek(0)

    def test_secret_is_required(self):
        with self.assertRaises(config.ConfigRequiredFieldError):
            cfg = config.Config(io.StringIO())

    def test_invalid_short_secret_should_raise_exception(self):
        with self.assertRaises(config.ConfigValueError):
            cfg = config.Config(
                io.StringIO('secret = "CHANGE_ME"'))

    def test_long_secret_should_be_ok(self):
        cfg = config.Config(
                io.StringIO('secret = "{}"'.format('x' * 40)))

    def test_mode_should_be_valid(self):
        self.appendcfg('mode = foobar\n')
        with self.assertRaises(config.ConfigValueError):
            cfg = config.Config(self.cfgstr)

    def test_mode_defaults_to_standalone(self):
        cfg = config.Config(self.cfgstr)
        self.assertEqual('standalone', cfg['mode'])

    def test_comments_are_ignored(self):
        self.appendcfg('#Comment\n# Best style\n## Still valid\n \t  # Blanks')

if __name__ == '__main__':
    unittest.main()
