# vim: tabstop=4 shiftwidth=4 softtabstop=4

import boto
import mox

from boto.ec2.connection import EC2Connection
from django import test
from django_openstack.core import connection
from django_openstack.nova.manager import ProjectManager
from mox import And, IgnoreArg, In
from nova_adminclient import client as nova_client


TEST_IMAGE_ID = 1
TEST_PROJECT_NAME = 'testProject'
TEST_PROJECT_DESCRIPTION = 'testDescription'
TEST_PROJECT_MANAGER_ID = 100
TEST_PROJECT_MEMBER_IDS = []
TEST_REGION_ENDPOINT = 'http://testServer:8773/services/Cloud'
TEST_REGION_NAME = 'testRegion'
TEST_REGION = {'endpoint': TEST_REGION_ENDPOINT, 'name': TEST_REGION_NAME}
TEST_USER = 'testUser'


class ProjectManagerTests(test.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        project = nova_client.ProjectInfo()
        project.projectname = TEST_PROJECT_NAME
        project.projectManagerId = TEST_PROJECT_MANAGER_ID

        self.manager = ProjectManager(TEST_USER, project, TEST_REGION)

    def tearDown(self):
        self.mox.UnsetStubs()

    def stub_conn_mock(self, count=1):
        ''' 
        Stubs get_openstack_connection as an EC2Connection and returns the
        EC2Connection mock 
        '''
        self.mox.StubOutWithMock(self.manager, 'get_openstack_connection')
        conn_mock = self.mox.CreateMock(EC2Connection)
        for i in range(count):
            self.manager.get_openstack_connection().AndReturn(conn_mock)
        return conn_mock


    def test_get_openstack_connection(self):
        self.mox.StubOutWithMock(connection, 'get_nova_admin_connection')
        admin_mock = self.mox.CreateMock(nova_client.NovaAdminClient)
        admin_mock.connection_for(TEST_USER, TEST_PROJECT_NAME,
                                  clc_url=TEST_REGION_ENDPOINT,
                                  region=TEST_REGION_NAME)
        connection.get_nova_admin_connection().AndReturn(admin_mock)

        self.mox.ReplayAll()

        self.manager.get_openstack_connection()

        self.mox.VerifyAll()

    def test_get_zip(self):
        self.mox.StubOutWithMock(connection, 'get_nova_admin_connection')
        admin_mock = self.mox.CreateMock(nova_client.NovaAdminClient)
        admin_mock.get_zip(TEST_USER, TEST_PROJECT_NAME)
        connection.get_nova_admin_connection().AndReturn(admin_mock)

        self.mox.ReplayAll()

        self.manager.get_zip()

        self.mox.VerifyAll()

    def test_get_images(self):
        ''' TODO: Need to figure out what I'm doing here...'''
        self.assertTrue(False)
        TEST_IMAGE_IDS = [TEST_IMAGE_ID,TEST_IMAGE_ID + 1]
        self.mox.StubOutwithMock(self.manager, 'get_openstack_connection')
        conn_mock = self.mox.CreateMock(EC2Connection)
        images_mock = self.mox.CreateMockAnything()
        

    def test_get_image(self):
        TEST_IMAGE_BAD_ID = TEST_IMAGE_ID + 1
        self.mox.StubOutWithMock(self.manager, 'get_images')
        self.manager.get_images(image_ids=[TEST_IMAGE_ID]).AndReturn([TEST_IMAGE_ID])
        self.manager.get_images(image_ids=[TEST_IMAGE_BAD_ID]).AndReturn([])

        self.mox.ReplayAll()

        image_result = self.manager.get_image(TEST_IMAGE_ID)
        self.assertEqual(TEST_IMAGE_ID, image_result)
        
        image_result = self.manager.get_image(TEST_IMAGE_BAD_ID)
        self.assertTrue(image_result is None)

        self.mox.VerifyAll()

    def test_deregister_image(self):
        conn_mock = self.stub_conn_mock()
        conn_mock.deregister_image(TEST_IMAGE_ID).AndReturn(TEST_IMAGE_ID)

        self.mox.ReplayAll()

        deregistered_id = self.manager.deregister_image(TEST_IMAGE_ID)

        self.assertEqual(deregistered_id, TEST_IMAGE_ID)

        self.mox.VerifyAll()


    def test_update_image(self):
        TEST_DISPLAY_NAME = 'testDisplayName'
        TEST_DESCRIPTION = 'testDescription'
        TEST_RETURN = 'testReturnString'

        conn_mock = self.stub_conn_mock(count=2)

        # TODO: Figure out why the arg parsing isn't working... 
        conn_mock.get_object('UpdateImage', 
                             #And(In(TEST_IMAGE_ID), In(TEST_DISPLAY_NAME),
                             #    In(TEST_DESCRIPTION)),
                             IgnoreArg(),
                             boto.ec2.image.Image).AndReturn(TEST_RETURN)
        conn_mock.get_object('UpdateImage',
                             #And(In(TEST_IMAGE_ID), In(None)),
                             IgnoreArg(),
                             boto.ec2.image.Image).AndReturn(TEST_RETURN)

        self.mox.ReplayAll()

        update_result = self.manager.update_image(TEST_IMAGE_ID, 
                                  display_name=TEST_DISPLAY_NAME, 
                                  description=TEST_DESCRIPTION)

        self.assertEqual(update_result, TEST_RETURN)

        update_result = self.manager.update_image(TEST_IMAGE_ID)

        self.assertEqual(update_result, TEST_RETURN)

        self.mox.VerifyAll()

    def test_modify_image_attribute(self):
        TEST_RETURN = 'testReturnValue'
        TEST_ATTRIBUTE = 'testAttribute'
        TEST_OPERATION = 'testOperation'
        TEST_GROUPS = 'testGroups'

        conn_mock = self.stub_conn_mock(count=2)

        # Test: default attributes passed
        conn_mock.modify_image_attribute(TEST_IMAGE_ID, 
                                         attribute=None, 
                                         operation=None, 
                                         groups='all').AndReturn(TEST_RETURN)
        # Test: custom attributes passed
        conn_mock.modify_image_attribute(TEST_IMAGE_ID, 
                                         attribute=TEST_ATTRIBUTE, 
                                         operation=TEST_OPERATION, 
                                         groups=TEST_GROUPS).AndReturn(TEST_RETURN)

        self.mox.ReplayAll()

        modify_return = self.manager.modify_image_attribute(TEST_IMAGE_ID)
        self.assertEqual(modify_return, TEST_RETURN)

        modify_return = self.manager.modify_image_attribute(TEST_IMAGE_ID,
                                                            attribute=TEST_ATTRIBUTE,
                                                            operation=TEST_OPERATION,
                                                            groups=TEST_GROUPS)
        self.assertEqual(modify_return, TEST_RETURN)

        self.mox.VerifyAll()

    def test_run_instances(self):
        TEST_RETURN = 'testReturnValue'

        conn_mock = self.stub_conn_mock()

        conn_mock.run_instances(TEST_IMAGE_ID,
                                key_name='testKey',
                                user_data='userData').AndReturn(TEST_RETURN)

        self.mox.ReplayAll()
        
        run_return = self.manager.run_instances(TEST_IMAGE_ID, 
                                                key_name='testKey',
                                                user_data='userData')
        self.assertEqual(run_return, TEST_RETURN)

        self.mox.VerifyAll()

    def test_get_instance_count(self):
        TEST_LEN = 5
        self.mox.StubOutWithMock(self.manager, 'get_instances')

        def valid_instance_list():
            self.manager.get_instances().AndReturn([i for i in range(TEST_LEN)])
            self.mox.ReplayAll()
            self.assertEqual(TEST_LEN, self.manager.get_instance_count())
            self.mox.VerifyAll()
            self.mox.ResetAll()

        def invalid_instance_list():
            self.manager.get_instances().AndReturn(None)
            self.mox.ReplayAll()
            self.assertTrue(self.manager.get_instance_count() is None)
            self.mox.VerifyAll()
            self.mox.ResetAll()

        valid_instance_list()
        invalid_instance_list()

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
