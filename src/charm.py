#! /usr/bin/env python3

# Copyright 2021 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging

from ops.main import main
from ops_openstack.plugins.classes import CinderStoragePluginCharm

logger = logging.getLogger(__name__)

VOLUME_DRIVERS = {
    'fc': 'cinder.volume.drivers.nimble.NimbleFCDriver',
    'iscsi': 'cinder.volume.drivers.nimble.NimbleISCSIDriver'}


class CinderNimblestorageCharm(CinderStoragePluginCharm):

    PACKAGES = ['cinder-common']
    # Overriden from the parent. May be set depending on the charm's properties
    stateless = True
    active_active = False

    mandatory_config = [
        'san-ip', 'san-login', 'san-password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stored.is_started = True

    def cinder_configuration(self, charm_config) -> 'list[tuple]':
        """Return the configuration to be set by the principal"""
        cget = charm_config.get

        volume_driver = cget('volume-driver')

        raw_options = [
            ('volume_driver', VOLUME_DRIVERS[volume_driver]),
            ('san_ip', cget('san-ip')),
            ('san_login', cget('san-login')),
            ('san_password', cget('san-password')),
            ('use_multipath_for_image_xfer',
                cget('use-multipath-for-image-xfer')),
            ('nimble:encryption', cget('encryption')),
            ('nimble:perfpol-name',
                cget('performance-policy-name')),

            # When upgrading to OpenStack deployment
            # to Victoria or later, do unset nimble:multi-initiator extra-spec
            # and set multiattach='<is> True'.
            ('nimble:multi-initiator', cget('multi-initiator')),
            ('nimble:dedupe', cget('dedupe')),
            ('nimble:iops-limit', cget('iops-limit')),
            ('nimble:folder', cget('folder')),
            ('nimble_pool_name', cget('pool-name')),
            ('nimble_subnet_label', cget('subnet-label')),
            ('nimble_verify_cert_path', cget('verify-cert-path')),
            ('nimble_verify_certificate', cget('verify-cert'))
        ]
        options = [(x, y) for x, y in raw_options if y]
        return options


if __name__ == '__main__':
    main(CinderNimblestorageCharm)
