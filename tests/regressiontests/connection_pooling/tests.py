
try:
    set
except NameError:
    # Python 2.3 compat
    from sets import Set as set

import unittest
import threading

class ThreadLocalPoolTestCase(unittest.TestCase):
    def test_thread_singleton_connections(self):
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
        