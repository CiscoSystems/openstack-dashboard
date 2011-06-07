# vim: tabstop=4 shiftwidth=4 softtabstop=4

import mox

from django import test
from django_openstack.core import connection
from django_openstack.nova.manager import ProjectManager
from nova_adminclient import client as nova_client


TEST_USER = 'testUser'
TEST_PROJECT_NAME = 'testProject'
TEST_PROJECT_DESCRIPTION = 'testDescription'
TEST_PROJECT_MANAGER_ID = 100
TEST_PROJECT_MEMBER_IDS = []
TEST_REGION_ENDPOINT = 'http://testServer:8773/services/Cloud'
TEST_REGION_NAME = 'testRegion'
TEST_REGION = {'endpoint': TEST_REGION_ENDPOINT, 'name': TEST_REGION_NAME}


class ProjectManagerTests(test.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.project = nova_client.ProjectInfo()
        self.project.projectname = TEST_PROJECT_NAME
        self.project.description = TEST_PROJECT_DESCRIPTION
        self.project.projectManagerId = TEST_PROJECT_MANAGER_ID
        self.project.memberIds = TEST_PROJECT_MEMBER_IDS

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_get_openstack_connection(self):
        manager = ProjectManager(TEST_USER, self.project, TEST_REGION)
        self.mox.StubOutWithMock(connection, 'get_nova_admin_connection')
        admin_mock = self.mox.CreateMock(nova_client.NovaAdminClient)
        admin_mock.connection_for(TEST_USER, TEST_PROJECT_NAME,
                                  clc_url=TEST_REGION_ENDPOINT,
                                  region=TEST_REGION_NAME)
        connection.get_nova_admin_connection().AndReturn(admin_mock)

        self.mox.ReplayAll()

        manager.get_openstack_connection()

        self.mox.VerifyAll()

    def test_get_zip(self):
        """docstring for test_get_zip"""
        pass

    def test_get_images(self):
        """docstring for test_get_images"""
        pass

    def test_get_image(self):
        """docstring for test_get_image"""
        pass

    def test_deregister_image(self):
        """docstring for test_deregister_image"""
        pass

    def test_update_image(self):
        """docstring for test_update_image"""
        pass

    def test_modify_image_attribute(self):
        """docstring for test_modify_image_attribute"""
        pass

    def test_run_instances(self):
        """docstring for test_run_instances"""
        pass

    def test_get_instance_count(self):
        """docstring for get_instance_count"""
        pass

    def test_get_instances(self):
        """docstring for get_instances"""
        pass

    def test_get_instance(self):
        """docstring for get_instance"""
        pass

    def test_update_instance(self):
        pass

    def test_get_instance_graph(self):
        pass

    def test_terminate_instance(self):
        pass

    def test_get_security_groups(self):
        pass

    def test_get_security_group(self):
        pass

    def test_has_security_group(self):
        pass

    def test_create_security_group(self):
        pass

    def test_delete_security_group(self):
        pass

    def test_authorize_security_group(self):
        pass

    def test_revoke_security_group(self):
        pass

    def test_get_key_pairs(self):
        pass

    def test_get_key_pair(self):
        pass

    def test_has_key_pair(self):
        pass

    def test_create_key_pair(self):
        pass

    def test_delete_key_pair(self):
        pass

    def test_get_volumes(self):
        pass

    def test_create_volume(self):
        pass

    def test_delete_volume(self):
        pass

    def test_attach_volume(self):
        pass

    def test_detach_volume(self):
        pass
