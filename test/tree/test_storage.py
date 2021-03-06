import pickle

import pytest

from cythondemo.tree import create_storage, raw, TreeStorage


# noinspection PyArgumentList,DuplicatedCode
@pytest.mark.unittest
class TestTreeStorage:
    def test_init(self):
        _ = create_storage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})

    def test_get(self):
        t = create_storage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})
        assert t.get('a') == 1
        assert t.get('b') == 2
        assert t.get('c') == {'x': 3, 'y': 4}
        assert isinstance(t.get('d'), TreeStorage)
        assert t.get('d').get('x') == 3
        assert t.get('d').get('y') == 4

        with pytest.raises(KeyError):
            _ = t.get('fff')

    def test_set(self):
        t = create_storage({})
        t.set('a', 1)
        t.set('b', 2)
        t.set('c', {'x': 3, 'y': 4})
        t.set('d', create_storage({'x': 3, 'y': 4}))
        t.set('_0a', None)

        assert t.get('a') == 1
        assert t.get('b') == 2
        assert t.get('c') == {'x': 3, 'y': 4}
        assert isinstance(t.get('d'), TreeStorage)
        assert t.get('_0a') is None

        with pytest.raises(KeyError):
            t.set('', 233)
        with pytest.raises(KeyError):
            t.set('a' * 1000, 233)
        with pytest.raises(KeyError):
            t.set('0' + 'a' * 10, 233)

    def test_del_(self):
        t = create_storage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})
        t.del_('c')
        t.del_('b')

        assert t.get('a') == 1
        with pytest.raises(KeyError):
            _ = t.get('c')
        with pytest.raises(KeyError):
            _ = t.get('b')
        assert isinstance(t.get('d'), TreeStorage)

        with pytest.raises(KeyError):
            t.del_('fff')

    def test_contains(self):
        t = create_storage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})
        assert t.contains('a')
        assert t.contains('b')
        assert t.contains('c')
        assert t.contains('d')
        assert not t.contains('f')
        assert not t.contains('kdfsj')

    def test_size(self):
        t = create_storage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})
        assert t.size() == 4
        assert t.get('d').size() == 2

        t.set('f', None)
        assert t.size() == 5

        t.del_('a')
        t.del_('c')
        t.del_('d')
        assert t.size() == 2

    def test_empty(self):
        t = create_storage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})
        assert not t.empty()
        assert not t.get('d').empty()

        t.del_('a')
        t.del_('c')
        t.get('d').del_('x')
        assert not t.empty()
        assert not t.get('d').empty()

        t.get('d').del_('y')
        assert t.get('d').empty()

        t.del_('b')
        t.del_('d')
        assert t.empty()

    def test_dump(self):
        h1 = {'x': 3, 'y': 4}
        h2 = {'x': 3, 'y': 4}
        t = create_storage({'a': 1, 'b': 2, 'c': raw(h1), 'd': h2})

        _dumped = t.dump()
        assert _dumped['a'] == 1
        assert _dumped['b'] == 2
        assert _dumped['c'].value is h1
        assert _dumped['d']['x'] == 3
        assert _dumped['d']['y'] == 4

    def test_deepdump(self):
        h1 = {'x': 3, 'y': 4}
        h2 = {'x': 3, 'y': 4}
        t = create_storage({'a': 1, 'b': 2, 'c': raw(h1), 'd': h2})

        _dumped = t.deepdump()
        assert _dumped['a'] == 1
        assert _dumped['b'] == 2
        assert _dumped['c'].value == h1
        assert _dumped['c'] is not h1
        assert _dumped['d']['x'] == 3
        assert _dumped['d']['y'] == 4

    def test_deepdumpx(self):
        h1 = {'x': 3, 'y': 4}
        h2 = {'x': 3, 'y': 4}
        t = create_storage({'a': 1, 'b': 2, 'c': raw(h1), 'd': h2})

        _dumped = t.deepdumpx(lambda x: -x if isinstance(x, int) else {'holy': 'shit'})
        assert _dumped['a'] == -1
        assert _dumped['b'] == -2
        assert _dumped['c'].value == {'holy': 'shit'}
        assert _dumped['d']['x'] == -3
        assert _dumped['d']['y'] == -4

    def test_copy(self):
        h1 = {'x': 3, 'y': 4}
        h2 = {'x': 3, 'y': 4}
        t = create_storage({'a': 1, 'b': 2, 'c': raw(h1), 'd': h2})

        t1 = t.copy()
        assert t1.get('a') == 1
        assert t1.get('b') == 2
        assert t1.get('c') is h1
        assert t1.get('d').get('x') == 3
        assert t1.get('d').get('y') == 4

    def test_deepcopy(self):
        h1 = {'x': 3, 'y': 4}
        h2 = {'x': 3, 'y': 4}
        t = create_storage({'a': 1, 'b': 2, 'c': raw(h1), 'd': h2})

        t1 = t.deepcopy()
        assert t1.get('a') == 1
        assert t1.get('b') == 2
        assert t1.get('c') == h1
        assert t1.get('c') is not h1
        assert t1.get('d').get('x') == 3
        assert t1.get('d').get('y') == 4

    def test_deepcopyx(self):
        h1 = {'x': 3, 'y': 4}
        h2 = {'x': 3, 'y': 4}
        t = create_storage({'a': 1, 'b': 2, 'c': raw(h1), 'd': h2})

        t1 = t.deepcopyx(lambda x: -x if isinstance(x, int) else {'holy': 'shit'})
        assert t1.get('a') == -1
        assert t1.get('b') == -2
        assert t1.get('c') == {'holy': 'shit'}
        assert t1.get('d').get('x') == -3
        assert t1.get('d').get('y') == -4

    def test_pickle(self):
        h1 = {'x': 3, 'y': 4}
        h2 = {'x': 3, 'y': 4}
        t = create_storage({'a': 1, 'b': 2, 'c': raw(h1), 'd': h2})

        t1 = pickle.loads(pickle.dumps(t))
        assert t1.get('a') == 1
        assert t1.get('b') == 2
        assert t1.get('c') == h1
        assert t1.get('c') is not h1
        assert t1.get('d').get('x') == 3
        assert t1.get('d').get('y') == 4

    def test_detach(self):
        h1 = {'x': 3, 'y': 4}
        h2 = {'x': 3, 'y': 4}
        t = create_storage({'a': 1, 'b': 2, 'c': raw(h1), 'd': h2})

        dt = t.detach()
        assert dt['a'] == 1
        assert dt['b'] == 2
        assert dt['c'] == h1
        assert isinstance(dt['d'], TreeStorage)
        assert dt['d'].get('x') == 3
        assert dt['d'].get('y') == 4

    def test_copy_from(self):
        h1 = {'x': 3, 'y': 4}
        h2 = {'x': 3, 'y': 4}
        t = create_storage({'a': 1, 'b': 2, 'c': raw(h1), 'd': h2, 'f': h2})

        h3 = {'x': 33, 'y': 44}
        h4 = {'x': 33, 'y': 44}
        t1 = create_storage({'a': 11, 'e': 2333, 'c': raw(h3), 'd': h4})
        did = id(t1.get('d'))
        t1.copy_from(t)
        assert t1 is not t
        assert t1.get('a') == 1
        assert t1.get('b') == 2
        assert t1.get('c') is h1
        assert t1.get('d').get('x') == 3
        assert t1.get('d').get('y') == 4
        assert id(t1.get('d')) == did
        assert not t1.contains('e')
        assert t1.get('f').get('x') == 3
        assert t1.get('f').get('y') == 4
        assert t1.get('f') is not t.get('f')

    def test_repr(self):
        h1 = {'x': 3, 'y': 4}
        h2 = {'x': 3, 'y': 4}
        t = create_storage({'a': 1, 'b': 2, 'c': raw(h1), 'd': h2, 'f': h2})

        assert repr(('a', 'b', 'c', 'd', 'f')) in repr(t)
        assert repr(('x', 'y')) in repr(t.get('d'))
        assert repr(('x', 'y')) in repr(t.get('f'))
