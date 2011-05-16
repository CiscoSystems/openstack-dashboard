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

from datetime import datetime
from django import http
from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django_open.exceptions import handle_nova_error
from django_open import adminclient
import django_open.forms

@login_required
@handle_nova_error
def instances(request, project_id=None):
    instances = adminclient.OpenManager().list_instances()
    return render_to_response('instances.html', { 'instances': instances },
                              context_instance = template.RequestContext(request))

@login_required
@handle_nova_error
def instances_terminate(request):
    if request.method == 'POST':
        inst = request.POST['instance_id']
        instance_id = int(inst)

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

    for im in images:
        im.created = datetime.strptime(im.created, "%Y-%m-%dT%H:%M:%SZ") if im.created else ""
        im.updated = datetime.strptime(im.updated, "%Y-%m-%dT%H:%M:%SZ") if im.updated else ""

    return render_to_response ('images.html', {
        'images': images}, context_instance = template.RequestContext(request))

@login_required
@handle_nova_error
def image_launch(request, image_id):
    print "Image ID:", image_id
    if request.method == 'POST':
        form = django_open.forms.LaunchForm(request.POST)
        if form.is_valid():
            #import pdb; pdb.set_trace()
            userdata = form.clean()

            adminclient.OpenManager().launch_instance(userdata['name'],
                                                      int(userdata['image_id']),
                                                      int(userdata['flavor']))
            return redirect('novaO_instances')
    else:
        form = django_open.forms.LaunchForm(initial={'image_id' : image_id})

    return render_to_response('image_launch.html', {'form': form, },
                              context_instance=template.RequestContext(request))

@login_required
@handle_nova_error
def flavors(request):
    flavors = sorted(adminclient.OpenManager().list_flavors(),
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
