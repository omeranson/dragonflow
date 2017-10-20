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

from oslo_log import helpers
from oslo_log import log

from dragonflow.controller.common import constants as const
from dragonflow.controller import df_base_app
from dragonflow.db.models import constants
from dragonflow.db.models import taas


LOG = log.getLogger(__name__)


class TapAsAServiceApp(df_base_app.DFlowApp):

    def switch_features_handler(self, ev):
        self.add_flow_go_to_table(
            table=const.TAP_SERVICE_DUPLICATE_TABLE,
            priority=const.PRIORITY_DEFAULT,
            goto_table_id=const.EGRESS_PORT_SECURITY_TABLE,
        )

    @df_base_app.register_event(taas.TapFlow, constants.EVENT_CREATED)
    @helpers.log_method_call
    def _tap_flow_created(self, tap_flow):
        pass  # TODO(oanson) Complete in workshop

    @df_base_app.register_event(taas.TapFlow, constants.EVENT_DELETED)
    @helpers.log_method_call
    def _tap_flow_deleted(self, tap_flow):
        pass  # TODO(oanson) Complete in workshop
