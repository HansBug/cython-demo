# distutils:language=c++
# cython:language_level=3

cdef class _RawWrapper:
    cdef public object value

    def __cinit__(self, v):
        self.value = v

cpdef public inline object raw(object obj):
    if not isinstance(obj, _RawWrapper) and isinstance(obj, dict):
        return _RawWrapper(obj)
    else:
        return obj

cpdef public inline object unraw(object obj):
    if isinstance(obj, _RawWrapper):
        return obj.value
    else:
        return obj

cdef class BaseTree:
    cpdef public void set(self, str key, object value) except *:
        raise NotImplementedError

    cpdef public object get(self, str key):
        raise NotImplementedError

    cpdef public void del_(self, str key) except *:
        raise NotImplementedError

    cpdef public boolean contains(self, str key) except *:
        raise NotImplementedError

    cpdef public uint size(self, ) except *:
        raise NotImplementedError

    cpdef public boolean empty(self, ) except *:
        raise NotImplementedError
