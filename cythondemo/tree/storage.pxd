# distutils:language=c++
# cython:language_level=3

ctypedef unsigned char boolean
ctypedef unsigned int uint

cdef class TreeStorage:
    cdef dict map

    cdef inline void _key_validate(self, const char*key) except *
    cpdef public void set(self, str key, object value) except *
    cpdef public object get(self, str key)
    cpdef public void del_(self, str key) except *
    cpdef public boolean contains(self, str key)
    cpdef public uint size(self)
    cpdef public boolean empty(self)
    cpdef public dict dump(self)
    cpdef public dict deepdump(self)
    cpdef public dict deepdumpx(self, copy_func)
    cpdef public TreeStorage copy(self)
    cpdef public TreeStorage deepcopy(self)
    cpdef public TreeStorage deepcopyx(self, copy_func)
