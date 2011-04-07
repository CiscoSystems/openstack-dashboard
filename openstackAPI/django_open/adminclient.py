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
        self._cp = openstack.compute.Compute(username=settings.OPENSTACK_USER,
                                            apikey=settings.OPENSTACK_ACCESS_KEY,
                                            auth_url=settings.OPENSTACK_MANAGER_URL)

    def list_instances(self):
        return self._cp.servers.list()

    def terminate_instance(self, instance):
        pass

    def list_images(self):
        """ Currently there's an issue with images not returning name that blows
            up openstack compute """
        try:
            return self._cp.images.list()
        except:
            return []

    def list_image_flavors(self):
        return self._cp.flavors.list()
