# Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class BossManageError(Exception):
    pass

class SSHError(BossManageError):
    pass

class SSHTunnelError(SSHError):
    # DP ???: BossManageError or SSHError
    pass

class RemoteCommandError(BossManageError):
    def __init__(self, cmd, returncode):
        self.cmd = cmd
        self.returncode = returncode

        message = "Remote Command '{}' returned '{}'".format(cmd, returncode)

        super(RemoteCommandError, self).__init__(message)

class StatusCheckError(BossManageError):
    def __init__(self, message, target=None):
        self.target = target

        super(StatusCheckError, self).__init__(message)

# DP ???: Subclass BossManageError
# Taken from boss-tools.git/bossutils/keycloak.py
class KeyCloakError(Exception):
    def __init__(self, status, data):
        super(KeyCloakError, self).__init__(data)
        self.status = status
        self.data = data

    def __str__(self):
        return "HTTP Error {}: {}".format(self.status, self.data)

    @staticmethod
    def _get_message(res):
        try: # Assume json formatted data
            return json.dumps(res.json())
        except:
            try: # Try just raw response
                return res.text
            except:
                return None

    @classmethod
    def raise_for_status(cls, res):
        if 400 <= res.status_code <= 600: # handle both Client and Server errors
            msg = cls._get_message(res)
            raise cls(res.status_code, msg)

class KeyCloakLoginError(KeyCloakError):
    def __init__(self, target, username):
        message = "Could not login to Keycloak at {} with username {}".format(target, username)
        super(KeyCloakLoginError, self).__init__(None, message)