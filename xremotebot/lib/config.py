import re

class ConfigError(Exception): pass
class ConfigSyntaxError(ConfigError): pass
class ConfigValueError(ConfigError): pass
class ConfigRequiredFieldError(ConfigError): pass

class Config(dict):
    '''
    Config file parser.
    '''
    _comment = re.compile(r'^\s*#.+$')
    _entry   = re.compile(r'^\s*(\w+)\s*=\s*"?(\w+)"?\s*(?:#.+)?$')
    def __init__(self, configfile):
        try:
            self._read_file(configfile)
            self._validate()
        except KeyError as e:
            raise ConfigRequiredFieldError(e)
        except ConfigError as e:
            # FIXME: loguear el error, capturar bien todo lo de configparser
            raise

    def _read_file(self, configfile):
        for line in configfile:
            if self._comment.match(line) is not None:
                continue
            entry = self._entry.match(line)

            if entry is None:
                raise ConfigSyntaxError('({})'.format(line))

            key, value = entry.groups()

            self[key] = value

    def convert(self, key, conversion=int):
        return conversion(self[key])

    def _validate(self):
        if len(self['secret']) < 40:
            raise ConfigValueError('"secret" should be a random string of'
                                   ' at least 40 chars, use `maintainance'
                                   '/random_secret` to generate a new one.')
        if 'mode' in self:
            if not self['mode'] in ('standalone', 'server'):
                raise ConfigValueError(
                    '"mode" should be either "standalone" or "server".')
        else:
            self['mode'] = 'standalone'





