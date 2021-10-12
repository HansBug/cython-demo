# distutils:language=c++
# cython:language_level=3

from libc.string cimport strlen
from .base cimport unraw, BaseTree

cdef class Tree(BaseTree):
    def __cinit__(self, dict value):
        self.map = {}
        cdef str k
        cdef object v
        for k, v in value.items():
            if isinstance(v, dict):
                self.map[k] = Tree(v)
            else:
                self.map[k] = unraw(v)

    cdef inline void _check_key_exist(self, str key) except *:
        if key not in self.map.keys():
            raise KeyError(f"Key {repr(key)} not found in this tree.")

    cdef inline void _key_validate(self, const char*key) except *:
        cdef int n = strlen(key)
        if n < 1:
            raise KeyError(f'Key {repr(key)} is too short, minimum length is 1 but {n} found.')
        elif n > 256:
            raise KeyError(f'Key {repr(key)} is too long, maximum length is 256 but {n} found.')

        cdef int i
        for i in range(n):
            if not (b'a' <= key[i] <= b'z' or b'A' <= key[i] <= b'Z' or key[i] == b'_'):
                raise KeyError(f'Invalid char {repr(key[i])} detected in key {repr(key)}.')

    cpdef public void set(self, str key, object value) except *:
        self._key_validate(key.encode())
        self.map[key] = value

    cpdef public object get(self, str key):
        self._check_key_exist(key)
        return self.map[key]

    cpdef public void del_(self, str key) except *:
        self._check_key_exist(key)
        del self.map[key]

    cpdef public boolean contains(self, str key):
        return key in self.map.keys()

    cpdef public uint size(self, ):
        return len(self.map)

    cpdef public boolean empty(self, ):
        return not self.map
