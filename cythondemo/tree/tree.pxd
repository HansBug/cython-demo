# distutils:language=c++
# cython:language_level=3

from .base cimport BaseTree

ctypedef unsigned char boolean
ctypedef unsigned int uint

cdef class Tree(BaseTree):
    cdef dict map

    cdef inline void _check_key_exist(self, str key) except *
    cdef inline void _key_validate(self, const char*key) except *
    cpdef public void set(self, str key, object value) except *
    cpdef public object get(self, str key)
    cpdef public void del_(self, str key) except *
    cpdef public boolean contains(self, str key) except *
    cpdef public uint size(self, ) except *
    cpdef public boolean empty(self, ) except *
    cpdef public dict deepdumpx(self, copy_func)
