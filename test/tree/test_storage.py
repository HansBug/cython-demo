import pytest

from cythondemo.tree import TreeStorage, raw


# noinspection PyArgumentList
@pytest.mark.unittest
class TestTreeStorage:
    def test_init(self):
        _ = TreeStorage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})

    def test_get(self):
        t = TreeStorage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})
        assert t.get('a') == 1
        assert t.get('b') == 2
        assert t.get('c') == {'x': 3, 'y': 4}
        assert isinstance(t.get('d'), TreeStorage)
        assert t.get('d').get('x') == 3
        assert t.get('d').get('y') == 4

        with pytest.raises(KeyError):
            _ = t.get('fff')

    def test_set(self):
        t = TreeStorage({})
        t.set('a', 1)
        t.set('b', 2)
        t.set('c', {'x': 3, 'y': 4})
        t.set('d', TreeStorage({'x': 3, 'y': 4}))
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
        t = TreeStorage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})
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
        t = TreeStorage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})
        assert t.contains('a')
        assert t.contains('b')
        assert t.contains('c')
        assert t.contains('d')
        assert not t.contains('f')
        assert not t.contains('kdfsj')

    def test_size(self):
        t = TreeStorage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})
        assert t.size() == 4
        assert t.get('d').size() == 2

        t.set('f', None)
        assert t.size() == 5

        t.del_('a')
        t.del_('c')
        t.del_('d')
        assert t.size() == 2

    def test_empty(self):
        t = TreeStorage({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})
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
