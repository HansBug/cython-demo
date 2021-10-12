# distutils:language=c++
# cython:language_level=3

from copy import deepcopy

cdef class _RawWrapper:
    cdef public object value

    def __cinit__(self, v):
        self.value = v

    def __getstate__(self):
        return self.value

    def __setstate__(self, state):
        self.value = state

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

cpdef inline object _keep_object(object obj):
    return obj

cdef class BaseTree:
    cpdef public void set(self, str key, object value) except *:
        raise NotImplementedError  # pragma: no cover

    cpdef public object get(self, str key):
        raise NotImplementedError  # pragma: no cover

    cpdef public void del_(self, str key) except *:
        raise NotImplementedError  # pragma: no cover

    cpdef public boolean contains(self, str key) except *:
        raise NotImplementedError  # pragma: no cover

    cpdef public uint size(self, ) except *:
        raise NotImplementedError  # pragma: no cover

    cpdef public boolean empty(self, ) except *:
        raise NotImplementedError  # pragma: no cover

    cpdef public dict dump(self):
        return self.deepdumpx(_keep_object)

    cpdef public dict deepdump(self):
        return self.deepcopyx(deepcopy)

    cpdef public dict deepdumpx(self, copy_func):
        raise NotImplementedError  # pragma: no cover

    cpdef public BaseTree copy(self):
        return self.deepcopyx(_keep_object)

    cpdef public BaseTree deepcopy(self):
        return self.deepcopyx(deepcopy)

    cpdef public BaseTree deepcopyx(self, copy_func):
        cdef type cls = type(self)
        return cls(self.deepdumpx(copy_func))

    def __getstate__(self):
        raise NotImplementedError  # pragma: no cover

    def __setstate__(self, state):
        raise NotImplementedError  # pragma: no cover
