from odoo.tests.common import TransactionCase
from odoo.tests import tagged


import logging
_logger = logging.getLogger(__name__)


@tagged('-at_install', 'post_install')
class TestAddCar(TransactionCase):
    def setUp(self):
        super(TestAddCar, self).setUp()
        self.auto_parking = self.env['auto.parking']
        auto_brand = self.env['auto.parking.brand']
        auto_model = self.env['auto.parking.model']
        self.records_before = self.auto_parking.search_count(
            [('name', '=', 'HOT777')])
        self.sample_brand = auto_brand.create({
            'name': 'GAZ',
            'model_ids': [(0, 0, {'name': 'Vodka'})]
        })
        self.sample_model = auto_model.search([('name', '=', 'Vodka')])

        self.sample_car = self.auto_parking.create({
            'name': 'HOT777',
            'brand_id': self.sample_brand.id,
            'model_id': self.sample_model.id,
        })
        self.records_after = self.auto_parking.search_count(
            [('name', '=', 'HOT777')])

    def test_if_car_status_true(self):
        self.assertEqual(
            self.sample_car.car_active,
            True,
            'Cars should have default state of true'
        )
        print('test_car_status was succesfull!')

    def test_car_insertion_succesful(self):
        self.assertEqual(
            self.records_after,
            self.records_before + 1,
            'Expected one additional record.'
        )

        print('test_car_insertion was succesfull!')

    def test_status_change(self):
        #parking_form = Form(self.auto_parking)
        # parking_form.name = "HHH888"
        # parking_form.brand_id = self.sample_brand
        # parking_form.model_id = self.sample_model
        # parking_data = parking_form.start_parking
        # state = parking_data.state
        status_before = self.sample_car.state
        self.sample_car.start_parking()
        status_after = self.sample_car.state

        self.assertNotEqual(
            status_before,
            status_after,
            msg='State should not be equal'
        )

        self.sample_car.end_parking()
        self.assertEqual(
            self.sample_car.state,
            'finished', msg='Car should be with state finished'
        )

        print('test_status_change was succesfull!')

    def test_valid_to(self):
        self.sample_car.write({
            'car_active': False,
        })
        self.sample_car._set_end_date()
        self.assertIsNot(
            self.sample_car.date_to,
            False,
            msg='Car should have valid to field set'
        )
        print('test_valid_to was succesfull!')

    def test_constrains(self):
        # test fails only if one of these doesnt throw exeception
        with self.assertRaises(Exception):
            self.auto_parking.create({
                'name': 'test',
                'brand_id': self.sample_brand.id,
                'model_id': self.sample_model.id,
            })

        with self.assertRaises(Exception):
            self.auto_parking.create({
                'name': 'HGZ777',
                'model_id': self.sample_model.id,
            })

        with self.assertRaises(Exception):
            self.auto_parking.create({
                'name': 'HGZ777',
                'brand_id': self.sample_brand.id,
            })

        print('test_constrains was succesfull!')

    def test_unlink_car_user(self):
        # user should not be able to delete
        simple_user = self.env['res.users'].search([('partner_id', '=', 'user')])
        self.env= self.env(user=simple_user)
        delete_failed = True
        if self.auto_parking.search([('name', '=', 'HOT777')]).unlink():
            delete_failed = False
        self.assertFalse(delete_failed, msg='Users should not be able to delete records')
        print('test_unlink_car_user was succesfull!')
        
