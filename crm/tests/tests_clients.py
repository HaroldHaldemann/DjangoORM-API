from rest_framework import status
from rest_framework.reverse import reverse

from crm.models import Client
from crm.tests.setup import CustomAPITestCase
from users.models import User


class ClientListTests(CustomAPITestCase):
    client_list_url = reverse('crm:client_list')

    # --- Managers ---
    def test_manager_get_client_list(self):
        user = User.objects.get(username='test_manager')
        test_client = self.get_token_auth_client(user)
        response = test_client.get(self.client_list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Client.objects.all()))

    def test_manager_create_client(self):
        user = User.objects.get(username='test_manager')
        test_client = self.get_token_auth_client(user)
        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'test_client@email.com',
            'status': False
        }
        response = test_client.post(self.client_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Sales ---
    def test_sales_get_client_list(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        response = test_client.get(self.client_list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            if item['status'] is True:
                self.assertEqual(item['sales_contact'], user.id)
            else:
                self.assertFalse(item['status'])

    def test_sales_post_prospect(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'test_client@email.com',
            'status': False
        }
        response = test_client.post(self.client_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('test_client@email.com', response.data['email'])

    def test_sales_post_client_status_true(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'test_client@email.com',
            'status': True
        }
        response = test_client.post(self.client_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('test_client@email.com', response.data['email'])
        self.assertEqual(user.id, response.data['sales_contact'])

    def test_sales_post_client_status_false(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'test_client@email.com',
            'status': False
        }
        response = test_client.post(self.client_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('test_client@email.com', response.data['email'])
        self.assertEqual(response.data['sales_contact'], None)

    def test_post_client_incomplete_data(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        response = test_client.post(self.client_list_url, data={'first_name': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Support ---
    def test_support_get_client_list(self):
        user = User.objects.get(username='test_support')
        test_client = self.get_token_auth_client(user)
        response = test_client.get(self.client_list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            client = Client.objects.get(id=item['id'])
            self.assertIn(client, Client.objects.filter(contract__event__support_contact=user.id))

    def test_support_post_client(self):
        user = User.objects.get(username='test_support')
        test_client = self.get_token_auth_client(user)
        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'test_client@email.com',
            'status': False
        }
        response = test_client.post(self.client_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ClientDetailTests(CustomAPITestCase):

    # --- Managers ---
    def test_manager_get_client_detail(self):
        user = User.objects.get(username='test_manager')
        test_client = self.get_token_auth_client(user)
        id_list = self.get_id_list(Client.objects.all())

        for i in range(len(id_list)):
            response = test_client.get(reverse('crm:client_detail', kwargs={'pk': id_list[i]}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- Sales ---
    def test_sales_get_client_detail(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        id_list = self.get_id_list(Client.objects.all())

        for i in range(len(id_list)):
            response = test_client.get(reverse('crm:client_detail', kwargs={'pk': id_list[i]}))
            client = Client.objects.get(id=id_list[i])
            if client.status is True and client.sales_contact != user:
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            else:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                if response.data['status'] is True:
                    self.assertEqual(Client.objects.get(id=id_list[i]).sales_contact, user)
                else:
                    self.assertFalse(Client.objects.get(id=id_list[i]).status)

    def test_sales_update_client_status_true(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'updated_email@email.com',
            'status': True
        }
        response = test_client.put('/crm/clients/3/', data)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual('updated_email@email.com', response.data['email'])
        self.assertEqual(response.data['sales_contact'], user.id)

    def test_sales_update_client_status_false(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        data = {
            'first_name': 'Michel',
            'last_name': 'Leblanc',
            'email': 'updated_email@email.com',
            'status': False
        }
        response = test_client.put('/crm/clients/4/', data)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('updated_email@email.com', response.data['email'])
        self.assertEqual(response.data['sales_contact'], None)

    def test_sales_update_converted_client_status(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'compta-dupont@email.com',
            'status': False
        }
        response = test_client.put('/crm/clients/2/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"detail": "Cannot change status of converted client."})

    def test_sales_delete_prospect(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        response = test_client.delete(reverse('crm:client_detail', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_sales_delete_converted_client(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        response = test_client.delete(reverse('crm:client_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_client_incomplete_data(self):
        user = User.objects.get(username='test_sales')
        test_client = self.get_token_auth_client(user)
        response = test_client.put('/crm/clients/2/', data={'first_name': 'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Support ---
    def test_support_get_client_detail(self):
        user = User.objects.get(username='test_support')
        test_client = self.get_token_auth_client(user)

        response = test_client.get(reverse('crm:client_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = test_client.get(reverse('crm:client_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_support_update_client(self):
        user = User.objects.get(username='test_support')
        test_client = self.get_token_auth_client(user)
        data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'updated_email@email.com',
            'status': True
        }
        response = test_client.put('/crm/clients/4/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_support_delete_client(self):
        user = User.objects.get(username='test_support')
        test_client = self.get_token_auth_client(user)
        response = test_client.delete(reverse('crm:client_detail', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
