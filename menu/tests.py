from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Plato


class AutenticacionWebTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('chef', 'chef@ejemplo.cl', 'ClaveSegura123')

    def test_vistas_protegidas_redirigen_al_login(self):
        plato = Plato.objects.create(nombre='Cazuela', precio=5000)
        urls = [
            reverse('lista_platos'), reverse('crear_plato'),
            reverse('editar_plato', args=[plato.pk]), reverse('eliminar_plato', args=[plato.pk]),
        ]
        for url in urls:
            r = self.client.get(url)
            self.assertEqual(r.status_code, 302)
            self.assertIn(reverse('login'), r['Location'])

    def test_login_correcto_e_incorrecto(self):
        r = self.client.post(reverse('login'), {'username': 'chef', 'password': 'mala'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'incorrectos')
        r = self.client.post(reverse('login'), {'username': 'chef', 'password': 'ClaveSegura123'})
        self.assertRedirects(r, reverse('lista_platos'))

    def test_logout(self):
        self.client.login(username='chef', password='ClaveSegura123')
        r = self.client.post(reverse('logout'))
        self.assertRedirects(r, reverse('home'))
        self.assertEqual(self.client.get(reverse('lista_platos')).status_code, 302)

    def test_registro(self):
        r = self.client.post(reverse('registro'), {
            'username': 'nuevo', 'email': 'nuevo@ejemplo.cl',
            'password1': 'OtraClave12345', 'password2': 'OtraClave12345'})
        self.assertRedirects(r, reverse('lista_platos'))
        self.assertTrue(User.objects.filter(username='nuevo').exists())


class CrudWebTests(TestCase):
    def setUp(self):
        User.objects.create_user('chef', 'chef@ejemplo.cl', 'ClaveSegura123')
        self.client.login(username='chef', password='ClaveSegura123')

    def test_crud_completo(self):
        cat = Categoria.objects.create(nombre='Fondos')
        self.client.post(reverse('crear_plato'), {'nombre': 'Lomo saltado', 'precio': 9000, 'categoria': cat.pk, 'disponible': 'on'})
        plato = Plato.objects.get(nombre='Lomo saltado')
        self.assertEqual(plato.categoria, cat)
        self.client.post(reverse('editar_plato', args=[plato.pk]), {'nombre': 'Lomo saltado', 'precio': 9500})
        plato.refresh_from_db()
        self.assertEqual(plato.precio, 9500)
        self.client.post(reverse('eliminar_plato', args=[plato.pk]))
        self.assertFalse(Plato.objects.filter(pk=plato.pk).exists())

    def test_validaciones_no_guardan_datos_invalidos(self):
        casos = [
            {'nombre': '', 'precio': 1000},
            {'nombre': 'Plato123', 'precio': 1000},
            {'nombre': 'ab', 'precio': 1000},
            {'nombre': 'Cazuela', 'precio': 0},
            {'nombre': 'Cazuela', 'precio': -5},
            {'nombre': 'Cazuela', 'precio': 'abc'},
            {'nombre': 'Cazuela', 'precio': 2000000},
        ]
        for datos in casos:
            r = self.client.post(reverse('crear_plato'), datos)
            self.assertEqual(r.status_code, 200, datos)
            self.assertEqual(Plato.objects.count(), 0, datos)

    def test_nombre_duplicado(self):
        Plato.objects.create(nombre='Cazuela', precio=5000)
        self.client.post(reverse('crear_plato'), {'nombre': 'cazuela', 'precio': 6000})
        self.assertEqual(Plato.objects.count(), 1)
