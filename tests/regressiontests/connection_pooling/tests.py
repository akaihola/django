
try:
    set
except NameError:
    # Python 2.3 compat
    from sets import Set as set

import unittest
import threading

class ThreadSingletonPoolTestCase(unittest.TestCase):
    def test_singleton_connection(self):
        """
        Ensure the same connection is always used in a thread.
        """
        def runner():
            from django.db import connection
            connection.cursor()
            c1 = connection.pool.get()
            connection.cursor()
            c2 = connection.pool.get()
            self.assertEqual(c1, c2)
        t = threading.Thread(target=runner)
        t.start()
        t.join()
    
    def test_unique_connections(self):
        """
        Ensure different connections are created for each thread.
        """
        connections = set()
        def runner():
            from django.db import connection
            # calling connection.cursor() will create a new connection, if
            # one is not already present
            connection.cursor()
            connections.add(connection.pool.get())
        threads = []
        for x in xrange(2):
            t = threading.Thread(target=runner)
            threads.append(t)
            t.start()
        for t in threads:
            t.join(1)
        # ensure all connections were unique
        self.assertEquals(len(connections), 2)
        