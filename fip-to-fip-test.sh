openstack network create private2
openstack subnet create --subnet-range 10.0.0.0/26 --network private2 private2-subnet
openstack router create router2
openstack router set --external-gateway public router2
openstack router add subnet router2 private2-subnet
openstack server create --image cirros-0.3.5-x86_64-disk --flavor cirros256 --network private t1
openstack server create --image cirros-0.3.5-x86_64-disk --flavor cirros256 --network private2 t2
sleep 10
export PORT1ID=$(openstack port list --server t1 --format value -c ID)
export PORT2ID=$(openstack port list --server t2 --format value -c ID)
export SGID=$(openstack port show $PORT1ID -f value -c security_group_ids)
openstack security group rule create --protocol icmp --ingress --remote-group $SGID $SGID
openstack security group rule create --protocol tcp --dst-port 22 --ingress --remote-group $SGID $SGID
openstack floating ip create --port $PORT1ID public
openstack floating ip create --port $PORT2ID public
