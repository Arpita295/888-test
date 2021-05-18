from unittest import TestCase
from datetime import datetime
from crud_app.crud import SQL


class TestCrudApp(TestCase):

    def setUp(self) -> None:
        self.mysql = SQL('root', 'root', 'localhost')
        self.mysql.create_database('online_gaming')

    def test_insert_sports(self):
        test_input = {'name': 'poker1'}
        self.mysql.insert('sports', args=test_input)
        self.mysql.execute_query("DELETE from sports where name='poker1'")

    def test_insert_events(self):
        test_input = {'name': 'poker event1', 'sport': 'poker1', 'type': 'inplay', 'status': 'pending',
                      'scheduled_start': datetime.utcnow(), 'actual_start':datetime.utcnow()}
        self.mysql.insert('events', args=test_input)
        self.mysql.execute_query("DELETE from events where sport='poker1'")

    def test_read_without_conditions(self):
        self.mysql.read_table("sports")

    def test_read_table_with_conditions(self):
        condition = "where sport='casino'"
        self.mysql.read_table('events', condition=condition)

    def test_update(self):
        condition = "name='casino'"
        args = {'slug': 'casino'}
        self.mysql.update_table("sports", condition, args=args)

    def test_read_complex_filters(self):
        condition = 'name="casino event"'
        condition += 'and sport="casino"'
        args = {'type': 'preplay', 'status': 'ended'}
        self.mysql.update_table("events", condition, args=args)

