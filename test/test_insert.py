import unittest

from api.elasticsearch_util import insert_log_in_db


def insert_utility():
    """
    Utility to insert data into DB
    :return:
    """
    with open("test_entry.json") as f:
        log_entry = f.read()
        f.close()
    insert_log_in_db(log_entry)

def remove_utility():
    """

    :return:
    """



class TestInsert(unittest.TestCase):

    def test_one_insertion(self):
        """
        Test to check if insertion is working or not
        :return:
        """
        insert_utility()

