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

"""
URL patterns for managing openstack Nova.
"""
from django.conf.urls.defaults import *
import django_open.views

urlpatterns = patterns('',
    url(r'^instances/$', django_open.views.instances, name='novaO_instances'),
    url(r'^instances/terminate/$', django_open.views.instances_terminate, name='novaO_terminate'),
    url(r'^images/$', django_open.views.images, name='novaO_images'),
    url(r'^images/launch$', django_open.views.image_launch, name='novaO_image_launch'),
    url(r'^flavors/$', django_open.views.flavors, name='novaO_flavors'),
    url(r'^keys/$', django_open.views.keys, name='novaO_keys'),
    url(r'^volumes/$', django_open.views.volumes, name='novaO_volumes'),
)
