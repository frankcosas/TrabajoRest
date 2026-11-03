from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token

from .models import Plato


class ApiTokenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('chef', 'chef@ejemplo.cl', 'ClaveSegura123')

    def obtener_token(self):
        r = self.client.post('/api/token/', {'username': 'chef', 'password': 'ClaveSegura123'},
                             content_type='application/json')
        self.assertEqual(r.status_code, 200)
        return r.json()['token']

    def test_login_devuelve_token(self):
        self.assertTrue(Token.objects.filter(key=self.obtener_token(), user=self.user).exists())

    def test_login_invalido(self):
        r = self.client.post('/api/token/', {'username': 'chef', 'password': 'mala'},
                             content_type='application/json')
        self.assertEqual(r.status_code, 400)

    def test_sin_token_401(self):
        self.assertEqual(self.client.get('/api/platos/').status_code, 401)

    def test_token_invalido_401(self):
        r = self.client.get('/api/platos/', HTTP_AUTHORIZATION='Token inventado')
        self.assertEqual(r.status_code, 401)


class ApiPlatosTests(TestCase):
    def setUp(self):
        User.objects.create_user('chef', 'chef@ejemplo.cl', 'ClaveSegura123')
        r = self.client.post('/api/token/', {'username': 'chef', 'password': 'ClaveSegura123'},
                             content_type='application/json')
        self.auth = {'HTTP_AUTHORIZATION': 'Token ' + r.json()['token']}

    def test_get_lista_y_detalle(self):
        p = Plato.objects.create(nombre='Cazuela', precio=5000)
        r = self.client.get('/api/platos/', **self.auth)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)
        r = self.client.get(f'/api/platos/{p.pk}/', **self.auth)
        self.assertEqual(r.json()['nombre'], 'Cazuela')

    def test_post_crea(self):
        r = self.client.post('/api/platos/', {'nombre': 'Pastel de choclo', 'precio': 7000},
                             content_type='application/json', **self.auth)
        self.assertEqual(r.status_code, 201)
        self.assertTrue(Plato.objects.filter(nombre='Pastel de choclo').exists())

    def test_put_actualiza(self):
        p = Plato.objects.create(nombre='Cazuela', precio=5000)
        r = self.client.put(f'/api/platos/{p.pk}/', {'nombre': 'Cazuela', 'precio': 5500, 'disponible': False},
                            content_type='application/json', **self.auth)
        self.assertEqual(r.status_code, 200)
        p.refresh_from_db()
        self.assertEqual((p.precio, p.disponible), (5500, False))

    def test_delete_elimina(self):
        p = Plato.objects.create(nombre='Cazuela', precio=5000)
        r = self.client.delete(f'/api/platos/{p.pk}/', **self.auth)
        self.assertEqual(r.status_code, 204)
        self.assertFalse(Plato.objects.filter(pk=p.pk).exists())

    def test_inexistente_404(self):
        for metodo in ('get', 'delete'):
            r = getattr(self.client, metodo)('/api/platos/9999/', **self.auth)
            self.assertEqual(r.status_code, 404)
        r = self.client.put('/api/platos/9999/', {'nombre': 'Algo', 'precio': 1},
                            content_type='application/json', **self.auth)
        self.assertEqual(r.status_code, 404)

    def test_datos_invalidos_400(self):
        casos = [{'nombre': '', 'precio': 1000}, {'nombre': 'Plato123', 'precio': 1000},
                 {'nombre': 'Cazuela', 'precio': 0}, {'nombre': 'Cazuela', 'precio': 'abc'},
                 {'precio': 1000}]
        for datos in casos:
            r = self.client.post('/api/platos/', datos, content_type='application/json', **self.auth)
            self.assertEqual(r.status_code, 400, datos)
        self.assertEqual(Plato.objects.count(), 0)

    def test_json_malformado_400(self):
        r = self.client.post('/api/platos/', '{mal', content_type='application/json', **self.auth)
        self.assertEqual(r.status_code, 400)
