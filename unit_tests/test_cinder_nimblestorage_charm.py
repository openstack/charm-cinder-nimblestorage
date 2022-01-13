# Copyright 2016 Canonical Ltd
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

import unittest
from src.charm import CinderNimblestorageCharm
from ops.model import ActiveStatus
from ops.testing import Harness


class TestCinderNimblestorageCharm(unittest.TestCase):

    def setUp(self):
        self.harness = Harness(CinderNimblestorageCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()
        self.harness.set_leader(True)
        relation_id = self.harness.add_relation('storage-backend', 'cinder')
        self.harness.add_relation_unit(relation_id, 'cinder/0')

    def test_base(self):
        self.assertEqual(
            self.harness.framework.model.app.name,
            'cinder-nimblestorage')
        self.harness.update_config({})
        self.assertTrue(isinstance(
            self.harness.model.unit.status, ActiveStatus))

    def test_configuration(self):
        test_config = {
            'volume-driver': 'iscsi',
            'volume-backend-name': 'nimble-storage-iscsi',
            'san-ip': '10.11.12.13',
            'san-login': 'admin',
            'san-password': 'admin',
            'use-multipath-for-image-xfer': True,
            'encryption': 'yes',
            'performance-policy-name': 'test-performance-policy',
            'multi-initiator': True,
            'pool-name': 'default',
            'subnet-label': '*',
            'verify-cert-path': 'None',
            'verify-cert': 'False'
        }
        config = self.harness.model.config

        self.harness.update_config(test_config)

        for k in test_config:
            self.assertEqual(test_config[k], config[k])
