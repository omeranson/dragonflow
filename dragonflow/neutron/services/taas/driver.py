# Copyright (c) 2016 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron_taas.services.taas import service_drivers
from oslo_log import helpers
from oslo_log import log

#from dragonflow.db.models import taas
from dragonflow.neutron.services import mixins

LOG = log.getLogger(__name__)


class DfTaasDriver(service_drivers.TaasBaseDriver, mixins.LazyNbApiMixin):
    def __init__(self, service_plugin):
        super(DfTaasDriver, self).__init__(service_plugin)
        LOG.info('DF TaaS driver initialized')

    @helpers.log_method_call
    def create_tap_service_precommit(self, _):
        pass

    @helpers.log_method_call
    def create_tap_service_postcommit(self, context):
        pass

    @helpers.log_method_call
    def delete_tap_service_precommit(self, _):
        pass

    @helpers.log_method_call
    def delete_tap_service_postcommit(self, context):
        pass

    @helpers.log_method_call
    def create_tap_flow_precommit(self, _):
        pass

    @helpers.log_method_call
    def create_tap_flow_postcommit(self, context):
        pass  # TODO(oanson) Complete in workshop

    @helpers.log_method_call
    def delete_tap_flow_precommit(self, context):
        pass

    @helpers.log_method_call
    def delete_tap_flow_postcommit(self, context):
        pass  # TODO(oanson) Complete in workshop
