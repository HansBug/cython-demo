import pytest

from cythondemo.tree.ctree import _CTree, raw


@pytest.mark.unittest
class TestTreeCTree:
    def test_ctree(self):
        t = _CTree({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})

        assert not t.empty()
        assert t.size() == 4
        assert t.get('a') == 1
        assert t.get('b') == 2
        assert t.get('c') == {'x': 3, 'y': 4}
        assert isinstance(t.get('d'), _CTree)

        t.set('a', 233)
        assert t.get('a') == 233
        t.set('b', {'a': 1, 'b': 2})
        assert isinstance(t.get('b'), dict)
        assert t.get('b') == {'a': 1, 'b': 2}

        d = {}
        t.set('f', d)
        assert t.get('f') is d

        t.set('g', _CTree({}))
        assert isinstance(t.get('g'), _CTree)
        assert t.get('g').empty()
