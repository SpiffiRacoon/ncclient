# Copyright 2009 Shikhar Bhushan
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

'Session-related NETCONF operations'

from ncclient.content.parsers import RPCParser
from rpc import RPC


class CloseSession(RPC):
    
    def __init__(self):
        RPC.__init__(self)
        self.spec = { 'tag': 'close-session' }
    
    def _response_cb(self, reply):
        RPC._response_cb(self, reply)
        if RPCParser.parse_ok(reply):
            self._listener.expect_close()
        self._session.close()
    
    def request(self, *args, **kwds):
        self._do_request(spec, *args, **kwds)


class KillSession(RPC):
    
    def __init__(self):
        RPC.__init__(self)
        self.spec = {
            'tag': 'kill-session',
            'children': [ { 'tag': 'session-id', 'text': None} ]
            }
    
    def request(self, session_id, reply_event=None):
        if not isinstance(session_id, basestring): # just make sure...
            session_id = str(session_id)
        self.spec['children'][0]['text'] = session_id
        self._do_request(self.spec, reply_event)