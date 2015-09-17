# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import gc
import multiprocessing
import threading

from django.contrib.auth.models import User

from desktop.lib.metrics import global_registry

global_registry().gauge_callback(
    name='python.threads.total',
    callback=lambda: len(threading.enumerate()),
    label='Thread Count',
    description='Number of threads',
    numerator='threads',
)

global_registry().gauge_callback(
    name='python.threads.daemon',
    callback=lambda: sum(1 for thread in threading.enumerate() if thread.isDaemon()),
    label='Daemon Thread Count',
    description='Number of daemon threads',
    numerator='threads',
)

# ------------------------------------------------------------------------------

global_registry().gauge_callback(
    name='python.multiprocessing.total',
    callback=lambda: len(multiprocessing.active_children()),
    label='Process Count',
    description='Number of multiprocessing processes',
    numerator='processes',
)

global_registry().gauge_callback(
    name='python.multiprocessing.active',
    callback=lambda: sum(1 for proc in multiprocessing.active_children() if proc.is_alive()),
    label='Active Multiprocessing Processes',
    description='Number of active multiprocessing processes',
    numerator='processes',
)

global_registry().gauge_callback(
    name='python.multiprocessing.daemon',
    callback=lambda: sum(1 for proc in multiprocessing.active_children() if proc.daemon),
    label='Daemon Processes Count',
    description='Number of daemon multiprocessing processes',
    numerator='processes',
)

# ------------------------------------------------------------------------------

for i in xrange(3):
  global_registry().gauge_callback(
      name='python.gc.generation.%s' % i,
      callback=lambda: gc.get_count()[i],
      label='GC Object Count in Generation %s' % i,
      description='Total number of objects in garbage collection generation %s' % i,
      numerator='objects',
      raw_counter=True,
  )

global_registry().gauge_callback(
    name='python.gc.objects',
    callback=lambda: sum(gc.get_count()),
    label='GC Object Count',
    description='Total number of objects in the Python process',
    numerator='objects',
    raw_counter=True,
)

# ------------------------------------------------------------------------------

active_requests = global_registry().counter(
    name='requests.active',
    label='Active Requests',
    description='Number of currently active requests',
    numerator='requests',
)

request_exceptions = global_registry().counter(
    name='requests.exceptions',
    label='Request Exceptions',
    description='Number requests that resulted in an exception',
    numerator='requests',
)

response_time = global_registry().timer(
    name='requests.response-time',
    label='Request Response Time',
    description='Time taken to respond to requests across all Hue endpoints',
    numerator='seconds',
    counter_numerator='requests',
    rate_denominator='seconds',
)

# ------------------------------------------------------------------------------

user_count = global_registry().gauge_callback(
    name='users',
    callback=lambda: User.objects.count(),
    label='Users',
    description='Total number of user accounts in Hue',
    numerator='users',
)

# ------------------------------------------------------------------------------

ldap_authentication_time = global_registry().timer(
    name='ldap.authentication-time',
    label='LDAP Authentication Time',
    description='The time spent waiting for LDAP to authenticate a user over the life of the process',
    numerator='seconds',
    counter_numerator='authentications',
    rate_denominator='seconds',
)

oauth_authentication_time = global_registry().timer(
    name='auth.oauth.authentication-time',
    label='OAUTH Authentication Time',
    description='The time spent waiting for OAUTH to authenticate a user over the life of the process',
    numerator='seconds',
    counter_numerator='authentications',
    rate_denominator='seconds',
)

pam_authentication_time = global_registry().timer(
    name='auth.pam.authentication-time',
    label='PAM Authentication Time',
    description='The time spent waiting for PAM to authenticate a user over the life of the process',
    numerator='seconds',
    counter_numerator='authentications',
    rate_denominator='seconds',
)

spnego_authentication_time = global_registry().timer(
    name='auth.spnego.authentication-time',
    label='SPNEGO Authentication Time',
    description='The time spent waiting for SPNEGO to authenticate a user over the life of the process',
    numerator='seconds',
    counter_numerator='authentications',
    rate_denominator='seconds',
)
