import logging
from unittest import TestCase

from generic_tree.tree import GenericTree
from generic_tree.utils.exceptions import *


class TestGenericTree(TestCase):
    def setUp(self) -> None:
        self.tree = GenericTree()

    def test_add_node(self):
        logging.info("Testing add_node")
        self.tree.add_node(1)
        self.tree.add_node(2, 1)

    def test_add_node_false(self):
        logging.info("Testing add_node when parent node is not in tree")
        self.tree.add_node(1)
        self.assertRaises(NodeNotFoundException, self.tree.add_node, 1, 4)

    def test_find_node(self):
        logging.info("Testing find node")
        self.tree.add_node(1)
        self.tree.add_node(2, 1)
        self.tree.find_node(2)

    def test_find_node_false(self):
        logging.info("Testing find node when tree is empty")
        self.assertRaises(EmptyTreeException, self.tree.find_node, 4)

    def test_create_tree(self):
        logging.info("Testing create tree")
        self.tree.create_tree(5)
        logging.info("Tree looks like {}".format(self.tree))

    def test_create_tree_false(self):
        logging.info("Testing create tree if tree size is 0")
        self.assertRaises(ZeroTreeSizeException, self.tree.create_tree, 0)

    def test_num_internal_nodes(self):
        logging.info("Testing number of internal nodes")
        parent_nodes = self.tree.create_tree(5)
        logging.info("Tree looks like {}".format(self.tree))
        logging.info("Parent nodes in the tree --> {}".format(parent_nodes))
        internal_nodes = self.tree.num_internal_nodes(parent_nodes)
        logging.info("Number of internal nodes = {}".format(internal_nodes))

    def test_num_internal_nodes_false(self):
        logging.info("Testing number of internal nodes when parent nodes is empty")
        self.assertRaises(EmptyTreeException, self.tree.num_internal_nodes, [])

    def test_print_tree(self):
        logging.info("Testing print tree")
        self.tree.create_tree(5)
        logging.info(self.tree.print_tree(self.tree.root, ""))

    def test_print_tree_false(self):
        logging.info("Testing print tree when tree is empty")
        self.assertRaises(EmptyTreeException, self.tree.print_tree, None, "")
