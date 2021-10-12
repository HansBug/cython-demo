import pickle

import pytest

from cythondemo.tree import BaseTree, Tree, raw


@pytest.mark.unittest
class TestTreeCTree:
    def test_ctree(self):
        t = Tree({'a': 1, 'b': 2, 'c': raw({'x': 3, 'y': 4}), 'd': {'x': 3, 'y': 4}})

        assert not t.empty()
        assert t.size() == 4
        assert t.get('a') == 1
        assert t.get('b') == 2
        assert t.get('c') == {'x': 3, 'y': 4}
        assert isinstance(t.get('d'), Tree)

        t.set('a', 233)
        assert t.get('a') == 233
        t.set('b', {'a': 1, 'b': 2})
        assert isinstance(t.get('b'), dict)
        assert t.get('b') == {'a': 1, 'b': 2}

        d = {}
        t.set('f', d)
        assert t.get('f') is d

        t.set('g', Tree({}))
        assert isinstance(t.get('g'), Tree)
        assert t.get('g').empty()

        assert issubclass(Tree, BaseTree)

        t1 = t.copy()
        assert t1.get('c') is t.get('c')

        t2 = t.deepcopy()
        assert t2.get('c') is not t.get('c')
        assert t2.get('c') == t.get('c')

        tb = pickle.dumps(t)
        t3 = pickle.loads(tb)
        assert t3.get('a') == t.get('a')
        assert t3.get('b') == t.get('b')
        assert t3.get('c') == t.get('c')
        assert t3.get('c') is not t.get('c')
        assert t3.get('d').get('x') == t.get('d').get('x')
        assert t3.get('d').get('y') == t.get('d').get('y')
