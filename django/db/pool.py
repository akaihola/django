
try:
    # Only exists in Python 2.4+
    from threading import local
except ImportError:
    # Import copy of _thread_local.py from Python 2.4
    from django.utils._threading_local import local

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
