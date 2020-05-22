from task_3_tic_tac_toe.btnode import BNode


class LinkedBinaryTree:
    """Represent a binary linked tree"""
    def __init__(self, root=None):
        """Initialize the tree"""
        self._root = root

    @staticmethod
    def add_children(root_, child1, child2=None):
        """Add children to the node"""
        if child2 is None:
            root_.right = BNode(child2)
        else:
            root_.left = BNode(child1)
            root_.right = BNode(child2)
