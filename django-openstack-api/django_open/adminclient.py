# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 Midokura KK
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

import openstack.compute
from django.conf import settings

class OpenManager(object):
    """
    Nova Openstack API client using the openstack.compute library.
    """
    def __init__(self):
        # set openstack.compute to use the Openstack API without Rackspace API extensions
        self._cp = openstack.compute.Compute(username=settings.OPENSTACK_USER,
                                            apikey=settings.OPENSTACK_ACCESS_KEY,
                                            auth_url=settings.OPENSTACK_MANAGER_URL,
                                            cloud_api = 'OPENSTACK')

    def list_instances(self):
        return self._cp.servers.list()

    # the only information that this returns not in the raw list is the flavor ID
    def get_instance(self, server_id):
        return self._cp.servers.get(server_id)

    def terminate_instance(self, instance_id):
        inst = self._cp.servers.get(instance_id)
        self._cp.servers.delete(inst)

    def launch_instance(self, name, image_id, flavor_id):
        im = self._cp.images.get(image_id)
        fl = self._cp.flavors.get(flavor_id)
        self._cp.servers.create(name, im, fl)

    def list_images(self):
        return self._cp.images.list()
            
    def get_image(self, image_id):
        return self._cp.images.get(image_id)

    def list_flavors(self):
        return self._cp.flavors.list()
        
    def get_flavor(self, flavor_id):
        return self._cp.flavors.get(flavor_id)

    # for use in listing where instance may be in an invalid state,
    # just display blank instead of blowing up
    def get_instance_flavor(self, server_id):
        try:
            fl_id = self.get_instance(server_id).flavorId
            flav =  self.get_flavor(fl_id)
            return (flav.id, flav.name)
        except:
            return ( None, '')