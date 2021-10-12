# distutils:language=c++
# cython:language_level=3

ctypedef unsigned char boolean
ctypedef unsigned int uint

cpdef public inline object raw(object obj)
cpdef public inline object unraw(object obj)

cdef class BaseTree:
    cpdef public void set(self, str key, object value) except *
    cpdef public object get(self, str key)
    cpdef public void del_(self, str key) except *
    cpdef public boolean contains(self, str key) except *
    cpdef public uint size(self, ) except *
    cpdef public boolean empty(self, ) except *
    cpdef public dict deepdump(self)
    cpdef public dict deepdumpx(self, copy_func)
    cpdef public dict dump(self, )
    cpdef public BaseTree deepcopy(self)
    cpdef public BaseTree deepcopyx(self, copy_func)
    cpdef public BaseTree copy(self, )
