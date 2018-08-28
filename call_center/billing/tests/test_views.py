import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from datetime import timedelta, datetime

from billing.models import Call, Charge
from billing.serializers import CallSerializer, BillSerializer

# initialize the APIClient app
client = Client()


class GetAllCallsTest(TestCase):
    """
    Test module for GET calls API
    """

    def setUp(self):
        call_1 = Call.objects.create(
            source="991366272",
            destination="991970287",
            start="2018-08-24 08:30:00+00:00",
            call_id=30
        )
        call_2 = Call.objects.create(
            source="991970287",
            destination="991905858",
            start="2018-08-24 12:30:00+00:00",
            end="2018-08-24 12:40:00+00:00",
            call_id=31
        )

    def test_get_all_completed_calls(self):
        # get API response
        response = client.get(reverse('get_post_calls'))
        # get data from db, exluding unfinished calls
        calls = Call.objects.all().exclude(end=None)
        serializer = CallSerializer(calls, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_incomplete_calls(self):
        # get API response
        response = client.get(reverse('get_incomplete_calls'))
        # get data from db, exluding unfinished calls
        calls = Call.objects.all().filter(end=None)
        serializer = CallSerializer(calls, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class POSTCallTest(TestCase):
    """
    Test module for completing a call from begining to end
    """

    def setUp(self):
        Charge.objects.create(
            standing_charge=0.36,
            minute_charge=0.09,
            reduced_tariff_start=22,
            reduced_tariff_end=6
        )

        self.end_response = ""
        self.start_response = ""
        # IDEA: multiple valid start and end payloads
        self.valid_start_payload = {
            'type': "start",
            'source': "991366272",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': "10"
        }
        self.valid_end_payload = {
            'type': "end",
            'end': "2018-08-24 08:40:00+00:00",
            'call_id': "10"
        }

        self.invalid_start_payloads = ({
            'type': "start",
            'source': "",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': "10"
        }, {
            'type': "start",
            'source': "991366272",
            'destination': "",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': "10"
        }, {
            'type': "start",
            'source': "991366272",
            'destination': "991970287",
            'start': "",
            'call_id': "10"
        }, {
            'type': "start",
            'source': "991366272",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': ""
        },)
        self.invalid_end_payloads = ({
            'type': "end",
            'end': "2018-08-24 08:40:00+00:00"
        }, {
            'type': "end",
            'end': "",
            'call_id': "10"
        }, {
            'type': "",
            'end': "2018-08-24 08:40:00+00:00",
            'call_id': "10"
        },
        )

    def test_start_valid_call(self):
        self.start_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_start_payload),
            content_type='application/json'
        )
        self.assertEqual(self.start_response.status_code,
                         status.HTTP_201_CREATED)

    def test_start_invalid_call(self):
        for payload in self.invalid_start_payloads:
            self.start_response = client.post(
                reverse('get_post_calls'),
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(self.start_response.status_code,
                             status.HTTP_400_BAD_REQUEST, "Failed Payload: {}".format(payload))

    def test_start_end_valid_call(self):
        # test looking through the client side
        self.start_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_start_payload),
            content_type='application/json'
        )
        self.assertEqual(self.start_response.status_code,
                         status.HTTP_201_CREATED)

        self.end_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_end_payload),
            content_type='application/json'
        )
        self.assertEqual(self.end_response.status_code,
                         status.HTTP_201_CREATED)

    def test_invalid_end_call(self):
        self.start_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_start_payload),
            content_type='application/json'
        )
        self.assertEqual(self.start_response.status_code,
                         status.HTTP_201_CREATED)

        for payload in self.invalid_end_payloads:
            self.end_response = client.post(
                reverse('get_post_calls'),
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(self.end_response.status_code,
                             status.HTTP_400_BAD_REQUEST, "Failed Payload: {}".format(payload))

    def test_billing_10_minutes_no_reduced_tariff(self):
        self.test_start_end_valid_call()

        self.assertEqual(self.end_response.data['call_price'], 1.25)


class GetBillTest(TestCase):

    def setUp(self):
        Charge.objects.create(
            standing_charge=0.36,
            minute_charge=0.09,
            reduced_tariff_start=22,
            reduced_tariff_end=6
        )
        # From the challenge specification
        # These calls are between the numbers 99988526423 (source) and 9993468278 (destination).
        # * call_id: 70, started at 2016-02-29T12:00:00Z and ended at 2016-02-29T14:00:00Z.
        # * call_id: 71, started at 2017-12-12T15:07:13Z and ended at 2017-12-12T15:14:56Z.
        # * call_id: 72, started at 2017-12-12T22:47:56Z and ended at 2017-12-12T22:50:56Z.
        # * call_id: 73, started at 2017-12-12T21:57:13Z and ended at 2017-12-12T22:10:56Z.
        # * call_id: 74, started at 2017-12-12T04:57:13Z and ended at 2017-12-12T06:10:56Z.
        # * call_id: 75, started at 2017-12-12T21:57:13Z and ended at 2017-12-13T22:10:56Z.
        # * call_id: 76, started at 2017-12-12T15:07:58Z and ended at 2017-12-12T15:12:56Z.
        # * call_id: 77, started at 2018-02-28T21:57:13Z and ended at 2018-03-01T22:10:56Z.
        # the following call was added to test the last closed period
        # * call_id: 78, started at 2018-07-12T15:07:58Z and ended at 2018-07-12T15:12:56Z.
        start_payloads = (
            {
                'type': "start",
                'source': "99988526423",
                'destination': "9993468278",
                'start': "2016-02-29T12:00:00Z",
                'call_id': "70"
            }, {
                'type': "start",
                'source': "99988526423",
                'destination': "9993468278",
                'start': "2017-12-12T15:07:13Z",
                'call_id': "71"
            }, {
                'type': "start",
                'source': "99988526423",
                'destination': "9993468278",
                'start': "2017-12-12T22:47:56Z",
                'call_id': "72"
            }, {
                'type': "start",
                'source': "99988526423",
                'destination': "9993468278",
                'start': "2017-12-12T21:57:13Z",
                'call_id': "73"
            }, {
                'type': "start",
                'source': "99988526423",
                'destination': "9993468278",
                'start': "2017-12-12T04:57:13Z",
                'call_id': "74"
            }, {
                'type': "start",
                'source': "99988526423",
                'destination': "9993468278",
                'start': "2017-12-12T21:57:13Z",
                'call_id': "75"
            }, {
                'type': "start",
                'source': "99988526423",
                'destination': "9993468278",
                'start': "2017-12-12T15:07:58Z",
                'call_id': "76"
            }, {
                'type': "start",
                'source': "99988526423",
                'destination': "9993468278",
                'start': "2018-02-28T21:57:13Z",
                'call_id': "77"
            }, {
                'type': "start",
                'source': "99988526423",
                'destination': "9993468278",
                'start': "2018-07-12T15:07:58Z",
                'call_id': "78"
            },
        )
        end_payloads = (
            {
                'type': "end",
                'end': "2016-02-29T14:00:00Z",
                'call_id': "70"
            }, {
                'type': "end",
                'end': "2017-12-12T15:14:56Z",
                'call_id': "71"
            }, {
                'type': "end",
                'end': "2017-12-12T22:50:56Z",
                'call_id': "72"
            }, {
                'type': "end",
                'end': "2017-12-12T22:10:56Z",
                'call_id': "73"
            }, {
                'type': "end",
                'end': "2017-12-12T06:10:56Z",
                'call_id': "74"
            }, {
                'type': "end",
                'end': "2017-12-13T22:10:56Z",
                'call_id': "75"
            }, {
                'type': "end",
                'end': "2017-12-12T15:12:56Z",
                'call_id': "76"
            }, {
                'type': "end",
                'end': "2018-03-01T22:10:56Z",
                'call_id': "77"
            }, {
                'type': "end",
                'end': "2018-07-12T15:12:56Z",
                'call_id': "78"
            },
        )

        for payload in start_payloads:
            response = client.post(
                reverse('get_post_calls'),
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(response.status_code,
                             status.HTTP_201_CREATED, "Failed Payload: {}".format(payload))

        for payload in end_payloads:
            response = client.post(
                reverse('get_post_calls'),
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(response.status_code,
                             status.HTTP_201_CREATED, "Failed Payload: {}".format(payload))

    def test_single_call_bill(self):
        # Ask the server for the february 2016 bill
        response = client.get(
            reverse('get_period_bills',
                    kwargs={'source': '99988526423',
                            'year': '2016',
                            'month': '02'}))

        # compare with the one stored in the database
        calls = Call.objects.filter(source='99988526423').filter(
            end__year=2016).filter(end__month=2)
        serializer = BillSerializer(calls, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_multiple_call_bill(self):
        # Ask the server for the december 2017 bill
        response = client.get(
            reverse('get_period_bills',
                    kwargs={'source': '99988526423',
                            'year': '2017',
                            'month': '12'}))

        # compare with the one stored in the database
        calls = Call.objects.filter(source='99988526423').filter(
            end__year=2017).filter(end__month=12)
        serializer = BillSerializer(calls, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_last_closed_period_bill(self):
        response = client.get(
            reverse('get_last_period_bills',
                    kwargs={'source': '99988526423'}))

        bill_period = datetime.now(tz=None).replace(day=1) - timedelta(days=1)
        # compare with the one stored in the database
        calls = Call.objects.filter(source='99988526423').filter(
            end__year=bill_period.year).filter(end__month=bill_period.month)
        serializer = BillSerializer(calls, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_invalid_number_period_bill(self):
        # Ask the server for the december 2017 bill
        response = client.get(
            reverse('get_period_bills',
                    kwargs={'source': '12345',
                            'year': '2017',
                            'month': '12'}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date_period_bill(self):
        # Ask the server for the december 2017 bill
        response = client.get(
            reverse('get_period_bills',
                    kwargs={'source': '99988526423',
                            'year': '2030',
                            'month': '12'}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_last_closed_period_bill(self):
        response = client.get(
            reverse('get_last_period_bills',
                    kwargs={'source': '12345'}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class POSTCallTest(TestCase):
    """
    Test module for completing a call from begining to end
    """

    def setUp(self):
        Charge.objects.create(
            standing_charge=0.36,
            minute_charge=0.09,
            reduced_tariff_start=22,
            reduced_tariff_end=6
        )

        self.end_response = ""
        self.start_response = ""
        # IDEA: multiple valid start and end payloads
        self.valid_start_payload = {
            'type': "start",
            'source': "991366272",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': "10"
        }
        self.valid_end_payload = {
            'type': "end",
            'end': "2018-08-24 08:40:00+00:00",
            'call_id': "10"
        }

        self.invalid_start_payloads = ({
            'type': "start",
            'source': "",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': "10"
        }, {
            'type': "start",
            'source': "991366272",
            'destination': "",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': "10"
        }, {
            'type': "start",
            'source': "991366272",
            'destination': "991970287",
            'start': "",
            'call_id': "10"
        }, {
            'type': "start",
            'source': "991366272",
            'destination': "991970287",
            'start': "2018-08-24 08:30:00+00:00",
            'call_id': ""
        },)
        self.invalid_end_payloads = ({
            'type': "end",
            'end': "2018-08-24 08:40:00+00:00"
        }, {
            'type': "end",
            'end': "",
            'call_id': "10"
        }, {
            'type': "",
            'end': "2018-08-24 08:40:00+00:00",
            'call_id': "10"
        },
        )

    def test_start_valid_call(self):
        self.start_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_start_payload),
            content_type='application/json'
        )
        self.assertEqual(self.start_response.status_code,
                         status.HTTP_201_CREATED)

    def test_start_invalid_call(self):
        for payload in self.invalid_start_payloads:
            self.start_response = client.post(
                reverse('get_post_calls'),
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(self.start_response.status_code,
                             status.HTTP_400_BAD_REQUEST, "Failed Payload: {}".format(payload))

    def test_start_end_valid_call(self):
        # test looking through the client side
        self.start_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_start_payload),
            content_type='application/json'
        )
        self.assertEqual(self.start_response.status_code,
                         status.HTTP_201_CREATED)

        self.end_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_end_payload),
            content_type='application/json'
        )
        self.assertEqual(self.end_response.status_code,
                         status.HTTP_201_CREATED)

    def test_invalid_end_call(self):
        self.start_response = client.post(
            reverse('get_post_calls'),
            data=json.dumps(self.valid_start_payload),
            content_type='application/json'
        )
        self.assertEqual(self.start_response.status_code,
                         status.HTTP_201_CREATED)

        for payload in self.invalid_end_payloads:
            self.end_response = client.post(
                reverse('get_post_calls'),
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(self.end_response.status_code,
                             status.HTTP_400_BAD_REQUEST, "Failed Payload: {}".format(payload))

    def test_billing_10_minutes_no_reduced_tariff(self):
        self.test_start_end_valid_call()

        self.assertEqual(self.end_response.data['call_price'], 1.25)


class POSTChargeTest(TestCase):

    def setUp(self):
        self.payload = {
            'standing_charge': "0.36",
            'minute_charge': "0.09",
            'reduced_tariff_start': "22",
            'reduced_tariff_end': "6"
        }
        self.invalid_payloads = (
            {
                'minute_charge': "0.09",
                'reduced_tariff_start': "22",
                'reduced_tariff_end': "6"
            }, {
                'standing_charge': "0.36",
                'reduced_tariff_start': "22",
                'reduced_tariff_end': "6"
            }, {
                'standing_charge': "0.36",
                'minute_charge': "0.09",
                'reduced_tariff_end': "6"
            }, {
                'standing_charge': "0.36",
                'minute_charge': "0.09",
                'reduced_tariff_start': "22",
            },
        )

    def test_start_valid_charge(self):
        start_response = client.post(
            reverse('get_post_charges'),
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(start_response.status_code,
                         status.HTTP_201_CREATED)

    def test_start_invalid_charge(self):
        for payload in self.invalid_payloads:
            start_response = client.post(
                reverse('get_post_charges'),
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(start_response.status_code,
                             status.HTTP_400_BAD_REQUEST, "Failed Payload: {}".format(payload))
