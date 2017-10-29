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
        if tap_flow.direction in {'OUT', 'BOTH'}:
            self._tap_flow_create_out(tap_flow)
        if tap_flow.direction in {'IN', 'BOTH'}:
            self._tap_flow_create_in(tap_flow)

    def _tap_flow_create_in(self, tap_flow):
        pass  # Not supported

    def _tap_flow_create_out(self, tap_flow):
        parser = self.parser
        match = self._get_tap_flow_match(tap_flow)
        actions = (
            parser.NXActionResubmitTable(
                table_id=const.EGRESS_PORT_SECURITY_TABLE),
            parser.OFPActionSetField(
                reg7=tap_flow.tap_service.unique_key),
            parser.NXActionResubmitTable(
                table_id=const.INGRESS_DISPATCH_TABLE),
        )
        self.mod_flow(
            actions=actions,
            table_id=const.TAP_SERVICE_DUPLICATE_TABLE,
            priority=const.PRIORITY_MEDIUM,
            match=match)

    @df_base_app.register_event(taas.TapFlow, constants.EVENT_DELETED)
    @helpers.log_method_call
    def _tap_flow_deleted(self, tap_flow):
        if tap_flow.direction in {'OUT', 'BOTH'}:
            self._tap_flow_delete_out(tap_flow)
        if tap_flow.direction in {'IN', 'BOTH'}:
            self._tap_flow_delete_in(tap_flow)

    def _tap_flow_delete_in(self, tap_flow):
        pass  # Not supported

    def _tap_flow_delete_out(self, tap_flow):
        ofproto = self.ofproto
        match = self._get_tap_flow_match(tap_flow)
        self.mod_flow(
            command=ofproto.OFPFC_DELETE,
            table_id=const.TAP_SERVICE_DUPLICATE_TABLE,
            priority=const.PRIORITY_MEDIUM,
            match=match)

    def _get_tap_flow_match(self, tap_flow):
        parser = self.parser
        lport = tap_flow.source_port
        match = parser.OFPMatch(
            reg6=lport.unique_key,
            metadata=lport.lswitch.unique_key)
        return match
