from django.conf import settings
try:
    # Only exists in Python 2.4+
    from threading import local, currentThread
except ImportError:
    # Import copy of _thread_local.py from Python 2.4
    from django.utils._threading_local import local, currentThread

class Pool(object):
    """
    Django database connection pool.
    """
    def __init__(self):
        pass
    
    def get(self):
        """
        Returns a dbapi connection from the pool. get() may return None if
        a new connection should be added the to the pool.
        """
        raise NotImplemented()
    
    def add(self, connection):
        """
        Adds a connection to the pool.
        """
        raise NotImplemented()
    
    def empty(self):
        raise NotImplemented()

class ThreadSingletonPool(Pool):
    """
    Enforces a single connection per thread.
    """
    def __init__(self):
        self.thread = local()
    
    def get(self):
        """
        Get the thread local connection.
        """
        # ensure the current thread has a connection attribute
        if not hasattr(self.thread, "connection"):
            return None
        return self.thread.connection
    
    def add(self, connection):
        """
        Set the thread connection to the given connection.
        """
        self.thread.connection = connection
    
    def empty(self):
        """
        If there is no thread local connection then this pool is empty
        otherwise it is not empty.
        """
        # ensure the current thread has a connection attribute
        if not hasattr(self.thread, "connection"):
            return True
        if self.thread.connection is None:
            return True
        return False

class QueuePool(Pool):
    def __init__(self):
        super(QueuePool, self).__init__()
        self.max_connections = getattr(settings, "MAX_CONNECTIONS", 5)
        self.available_connections = []
        self.connections_inuse = {}
    
    def get(self):
        return self.connections_inuse.get(currentThread())
        
    
    def add(self, connection):
        if connection is None:
            conn = self.connections_inuse.pop(currentThread(), None)
            if conn is not None:
                self.available_connections.append(conn)
        self.connections_inuse[currentThread()] = connection
        
    def empty(self):
        return not self.available_connections
