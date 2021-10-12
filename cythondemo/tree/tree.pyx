# distutils:language=c++
# cython:language_level=3

from libc.string cimport strlen

from .base cimport raw, unraw, BaseTree

cdef class Tree(BaseTree):
    def __cinit__(self, dict value):
        self.map = {}
        cdef str k
        cdef object v
        for k, v in value.items():
            self._key_validate(k.encode())
            if isinstance(v, dict):
                self.map[k] = Tree(v)
            else:
                self.map[k] = unraw(v)

    def __getnewargs_ex__(self):  # for __cinit__, when pickle.loads
        return ({},), {}

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
        try:
            return self.map[key]
        except KeyError:
            raise KeyError(f"Key {repr(key)} not found in this tree.")

    cpdef public void del_(self, str key) except *:
        try:
            del self.map[key]
        except KeyError:
            raise KeyError(f"Key {repr(key)} not found in this tree.")

    cpdef public boolean contains(self, str key):
        return key in self.map

    cpdef public uint size(self, ):
        return len(self.map)

    cpdef public boolean empty(self, ):
        return not self.map

    cpdef public dict deepdumpx(self, copy_func):
        cdef dict result = {}
        cdef str k
        cdef object v
        for k, v in self.map.items():
            if isinstance(v, BaseTree):
                result[k] = v.dump()
            else:
                result[k] = raw(copy_func(v))

        return result

    def __getstate__(self):
        return self.map

    def __setstate__(self, state):
        self.map = state
