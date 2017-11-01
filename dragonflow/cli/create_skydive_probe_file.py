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

import uuid

from oslo_serialization import jsonutils

from dragonflow.common import utils as df_utils
from dragonflow.db import api_nb
from dragonflow.db import model_framework as mf
from dragonflow.db.models import all  # noqa


DF_SKYDIVE_NAMESPACE_UUID = uuid.UUID('8a527b24-f0f5-4c1f-8f3d-6de400aa0145')


def output_edge(outf, nb_api, instance, field_name):
    field_proxy = getattr(instance, field_name)
    field = nb_api.get(field_proxy)
    id_str = '{}->{}'.format(instance.id, field.id)
    metadata = {
        'source': 'dragonflow',
        'source_type': type(instance).__name__,
        'dest_type': type(field).__name__,
        "RelationType" : "ownership"
    }
    result = {
        'ID': str(uuid.uuid5(DF_SKYDIVE_NAMESPACE_UUID, id_str)),
        'Child': "DF-{}".format(instance.id),
        'Parent': "DF-{}".format(field.id),
        'Host': 'dragonflow',
        'Metadata': metadata
    }
    outf(result)

def output_edges(outf, nb_api, table_name, field_name):
    model = mf.get_model(table_name)
    instances = nb_api.get_all(model)
    for instance in instances:
        output_edge(outf, nb_api, instance, field_name)

def output_table_node(outf, instance):
    metadata = {
        'ID': "DF-{}".format(instance.id),
        'type': type(instance).__name__,
        'source': 'dragonflow',
        'data': instance.to_struct(),
        'Name': getattr(instance, 'name') or instance.id
    }
    result = {
        'Metadata': metadata,
        'ID': "DF-{}".format(instance.id),
        'Host': 'dragonflow'}
    outf(result)

def output_table(outf, nb_api, table_name):
    model = mf.get_model(table_name)
    instances = nb_api.get_all(model)
    for instance in instances:
        output_table_node(outf, instance)

def main():
    df_utils.config_parse()
    nodes = []
    nb_api = api_nb.NbApi.get_instance(False)
    output_table(nodes.append, nb_api, 'LogicalPort')
    output_table(nodes.append, nb_api, 'LogicalSwitch')
    edges = []
    output_edges(edges.append, nb_api, 'LogicalPort', 'lswitch')
    result = {
        'Nodes': nodes,
        'Edges': edges,
    }
    with open('output.json', 'w') as f:
        jsonutils.dump(result, f)
    print('Done!')

if __name__ == "__main__":
    main()
