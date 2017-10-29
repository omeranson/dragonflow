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

import dragonflow.db.field_types as df_fields
import dragonflow.db.model_framework as mf
from dragonflow.db.models import l2
from dragonflow.db.models import mixins

direction_enum = ('IN', 'OUT', 'BOTH')


@mf.register_model
@mf.construct_nb_db_model(indexes={'source_port': 'source_port'})
class TapFlow(mf.ModelBase, mixins.BasicEvents, mixins.Topic):
    table_name = 'tap_flow'

    source_port = df_fields.ReferenceField(l2.LogicalPort)
    direction = df_fields.EnumField(direction_enum)
    tap_service = df_fields.ReferenceField(l2.LogicalPort)
