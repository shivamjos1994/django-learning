from django.db.models import Max
from django.test import Client, TestCase
from .models import Flight, Airport, Passenger

# Create your tests here.


class FlightTestCase(TestCase):
    def setUp(self):
        # creating dummy airports
        a1 = Airport.objects.create(code="AAA", city="A")
        a2 = Airport.objects.create(code="BBB", city="B")
    
        # creating dummy flights
        Flight.objects.create(origin=a1, destination=a2, duration=350)
        Flight.objects.create(origin=a1, destination=a1, duration=230)
        Flight.objects.create(origin=a1, destination=a2, duration=-120)

    # testing the departures count
    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    # testing the arrivals count
    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    # testing if the flight is valid
    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=350)
        self.assertTrue(f.is_valid_flight())

    # testing if the flight's destination is inavlid
    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1, duration= 230)
        self.assertFalse(f.is_valid_flight())

    # testing if the flight's duration is invalid
    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-120)
        self.assertFalse(f.is_valid_flight())

    # testing if index view returns a response or not
    def test_index(self):
        # Client() method is a dummy web browser, can be used to test the behaviour of your app without actually running it on server.
        c = Client()
        response = c.get("/flights/")
        print(response)
        # checks if status is OK or not
        self.assertEqual(response.status_code, 200)

    # testing the valid flight page
    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.create(origin=a1, destination=a1, duration = 343)
        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    # testing the invalid flight page, that should not return any info
    def test_invalid_flight_page(self):
        # will get the max_id from the database
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]
        c = Client()
        # it'll raise 404 status code, if anyone tries to enter the value greater than the max_id
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    # testing the flight page for the passengers
    def test_flight_page_passengers(self):
        # get a flight with id 1
        f = Flight.objects.get(pk=1)
        # create a passenger with first and last name
        p = Passenger.objects.create(first_name="Vikram", last_name="Batra")

        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        # checking if the passenger added to the flight is one
        self.assertEqual(response.context["passengers"].count(), 1)

    # testing the flight page for the non-passengers
    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first_name="Vikram", last_name="Batra")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
