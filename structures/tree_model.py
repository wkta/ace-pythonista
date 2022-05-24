

class Treex:
    """models the tree in its entirety"""
    def __init__(self, root_content):
        self.root = TreeNode(root_content, None)
        self.__allnodes = set()
        self.__allnodes.add(self.root)

    def add_content(self, content, parent_node):
        if parent_node not in self.__allnodes:
            raise ValueError('cannot find specified parent_node')

        n = TreeNode(content, parent_node)
        parent_node.childs.append(n)
        self.add_node(n)

    def add_node(self, n_val):
        raise NotImplementedError  # TODO complete this implem.

    def count(self):
        return len(self.__allnodes)

    def get_node_by_content(self, searched_content):
        queue = [self.root]
        while len(queue) > 0:
            exn = queue.pop()
            if searched_content == exn.content:
                return exn
            if not exn.is_leaf():
                queue.extend(exn.childs)
        return None

    def cut_from_node(self, ref_node):
        if ref_node == self.root:
            raise ValueError('empty tree not allowed')

        if not ref_node.is_leaf():
            # if node has childs, we shall cut the whole branch
            for c in ref_node.childs:
                self.cut_from_node(c)

        ref_node.parent.childs.remove(ref_node)
        self.__allnodes.remove(ref_node)


class Tree:
    def __init__(self, r):
        self._rootref = r


class TreeNode:
    _free_id = -6789*(10**8)

    def __init__(self, v, parent=None):
        cls = self.__class__
        self._ident = cls._free_id
        cls._free_id += 1

        self._childs = list()
        self.v = v
        if parent:
            self._parent = parent
            self._tree = parent.tree
        else:
            self._parent = None
            self._tree = Tree(self)

    @property
    def tree(self):
        return self._tree
    
    @property
    def id(self):
        return self._ident

    def rebase(new_parent):
        raise NotImplementedError
    
    def add_child(self, newnode):
        
        err_msg = 'node already in the tree!'
        if self.id == newnode.id:
            raise ValueError(err_msg)
        
        # find the root
        if self.is_root():
            roo = self
        else:
            roo = self._parent
            while not roo.is_root():
                roo = roo._parent
        
        # look down, starting from root
        if TreeNode.look_node_down(roo, newnode.id):
           raise ValueError(err_msg)

        self._childs.append(newnode)
        newnode._parent = self
        newnode._tree = self.tree

    def look_node_down(self, given_ident):
        if given_ident == self.id:
            return self
        for n in self._childs:
            tmp = TreeNode.look_node_down(n, given_ident)
            if tmp:
                return tmp

    def get_root(self):
        # find the root
        if self.is_root():
            return self
        roo = self._parent
        while not roo.is_root():
            return roo._parent
        raise ValueError('cannot find root?')

    @property
    def child_count(self):
        return len(self._childs)

    @property
    def depth(self):
        cpt = 0
        r = self
        while not r.is_root():
            r = r._parent
            cpt += 1
        return cpt

    def is_root(self):
        return self._parent is None

    def is_leaf(self):
        return self.child_count == 0


# tests
if __name__ == '__main__':
    x = TreeNode(1)
    y = TreeNode(88)
    x.add_child(y)
    z = TreeNode(15)
    y.add_child(z)
    # prints:
    # 0 1 2
    print(x.depth, y.depth, z.depth)
    # prints:
    # False, False, True, False, 1, 0
    print(y.is_root(), x.is_leaf(), z.is_leaf(), y.is_leaf(), y.child_count, z.child_count)
    
    # should raise an error
    kappa=TreeNode(128)
    y.add_child(kappa)
    print(z.depth)
    #y.add_child(kappa)
    # z.add_child(x)
