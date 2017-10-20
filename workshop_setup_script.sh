#!/bin/bash

# Script
# Go home
cd
. devstack/openrc admin admin
#Add cirros+tcpdump image
openstack image create --file cirros-u14.04-kver-3.13.0-85-x86_64-disk.img cirros-tcpdump
#Create cirros+tcpdump instance (name: vm-tcpdump)
openstack server create --image cirros-tcpdump --flavor cirros256 --network private vm-tcpdump
#Create regular instance (name: vm-vanilla)
openstack server create --image cirros-0.3.5-x86_64-disk --flavor cirros256 --network private vm-vanilla
sleep 30
#Add FIP to vm-tcpdump
TCPDUMP_PORT=$(openstack port list -c ID -f value --server vm-tcpdump)
openstack floating ip create --port $TCPDUMP_PORT public
#Add FIP to vm-vanilla
VANILLA_PORT=$(openstack port list -c ID -f value --server vm-vanilla)
openstack floating ip create --port $VANILLA_PORT public
#Print IPs
echo -n "tcpdump machine: "
openstack floating ip list -c "Floating IP Address" -f value --port $TCPDUMP_PORT

echo -n "vanilla machine: "
openstack floating ip list -c "Floating IP Address" -f value --port $VANILLA_PORT
