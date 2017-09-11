#!/usr/bin/python
#
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import logging
from google.cloud.logging.resource import Resource
import getpass
import os
import socket


def write(text, severity='INFO', env=None, port=None, ver=None, **kwargs):
    '''Wrapper method for assembling the payload to send to logger.log_text.'''

    # Extract and build Stackdriver log id from environment.
    # For example: 'prod.0112.8001'
    if not env:
        env = os.getenv('ENV')
    if not port:
        port = os.getenv('port')
    if not ver:
        ver = os.getenv('VER')

    if not env or not port or not ver:
        raise Exception('One or more log name tokens are empty. Unable to log.')
    # end if

    # Assemble logger name.
    logger_name = '.'.join([
        env,
        port,
        ver
    ])

    print '# Logging to %s...' % logger_name

    # Build logger object.
    logging_client = logging.Client()
    logger = logging_client.logger(logger_name)

    # Assemble the required log metadata.
    label_payload = {
        "username" : getpass.getuser(),
        "hostname" : socket.gethostname(),
        "env" : env,
        "ver" : ver,
        "port" : port
    }

    # Add optional kwargs to payload.
    label_payload.update(kwargs)

    # Write log.
    logger.log_text(
        text,
        resource=Resource(type='project', labels={'project_id':show}),
        severity=severity,
        labels=label_payload
    )

# end write

