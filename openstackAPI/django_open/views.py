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

from django import http
from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django_nova.exceptions import handle_nova_error
from django_open import adminclient

@login_required
@handle_nova_error
def instances(request, project_id=None):
    project = None
    instances = adminclient.OpenManager().list_instances()
    #import pdb; pdb.set_trace()

    return render_to_response('instances.html', {
        'region': None,
        'project': project,
        'instances': instances,
        'detail' : False,
    }, context_instance = template.RequestContext(request))

@login_required
@handle_nova_error
def instances_terminate(request):
    if request.method == 'POST':
        instance_id = request.POST['instance_id']

        try:
            adminclient.OpenManager().terminate_instance(instance_id)
        except exceptions.NovaApiError, e:
            messages.error(request,
                           'Unable to terminate %s: %s' %
                           (instance_id, e.message,))
        else:
            messages.success(request,
                             'Instance %s has been terminated.' % instance_id)

    return redirect('novaO_instances')

@login_required
@handle_nova_error
def images(request):
    images = adminclient.OpenManager().list_images()

    return render_to_response ('images.html', {
        'images': images}, context_instance = template.RequestContext(request))

@login_required
@handle_nova_error
def flavors(request):
    flavors = sorted(adminclient.OpenManager().list_image_flavors(),
                     key=lambda flavor: flavor.id)

    return render_to_response ('flavors.html', {
        'flavors': flavors}, context_instance = template.RequestContext(request))

@login_required
@handle_nova_error
def keys(request):
    return render_to_response ('keys.html', {
        'keys': None}, context_instance = template.RequestContext(request))

@login_required
@handle_nova_error
def volumes(request):
    return render_to_response ('volumes.html', {
        'volumes': None}, context_instance = template.RequestContext(request))
