import logging
import random

from generic_tree.utils.exceptions import *


class Node:
    def __init__(self, key, children=None):
        self.key = key
        self.children = children or []


class GenericTree:
    def __init__(self):
        self.root = None
        logging.basicConfig(filename='generic_tree.log', filemode='w',
                            format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%Y-%m-%d:%H:%M:%S')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

    def add_node(self, new_key, parent_key=None):
        """
        Add a new node to the tree
        :param new_key: key for the new node
        :param parent_key: key of the parent node
        :return: None
        """
        new_node = Node(new_key)
        if parent_key is None:
            self.root = new_node
            logging.info("Root of the tree added --> {}".format(new_key))
        else:
            parent_node = self.find_node(parent_key)
            if not parent_node:
                logging.error('No node was found with the parent key --> {}'.format(parent_key))
                raise NodeNotFoundException('No node was found with the parent key --> {}'.format(parent_key))
            parent_node.children.append(new_node)
            logging.info("Child --> {} added to parent --> {}".format(new_key,parent_key))

    def find_node(self, key):
        """
         Find node with the key given
        :param key: key of node to find in tree
        :return: node having the value as key
        """
        if self.root is None:
            logging.error("Root node not found for the tree")
            raise EmptyTreeException("Root node not found for the tree")
        if self.root.key == key:
            logging.info("Node with key {} found as root".format(key))
            return self.root
        node_q = [self.root]
        while len(node_q):
            node = node_q[0]
            node_q.pop(0)
            if node.key == key:
                logging.info("Node with key {} found".format(node.key))
                return node
            for i in range(len(node.children)):
                node_q.append(node.children[i])
        logging.error("Node with key {} not found".format(key))
        raise NodeNotFoundException('No node was found with the parent key --> {}'.format(key))

    def create_tree(self, tree_size):
        """
        Create tree with the given size
        :param tree_size: Size of the tree to be formed
        :return: Return parents list in the tree
        """
        if tree_size == 0:
            logging.error("Tree size provided as 0. Cannot create tree")
            raise ZeroTreeSizeException("Tree size provided as 0. Cannot create tree")
        random_choice = random.randint(1, tree_size*2)
        # Adding root node
        self.add_node(random_choice)
        new_nodes = []
        parent_nodes_list = [-1]
        new_nodes.append(random_choice)

        # Adding rest other nodes
        for i in range(1, tree_size):
            while True:
                random_choice = random.randint(1, tree_size*2)
                if random_choice not in new_nodes:
                    break
            parent_choice = random.choice(new_nodes)
            self.add_node(random_choice, parent_choice)
            new_nodes.append(random_choice)
            parent_nodes_list.append(parent_choice)
        logging.info("Parent nodes list --> {}".format(parent_nodes_list))
        return parent_nodes_list

    def num_internal_nodes(self, parent_nodes):
        """
        Finds number of internal nodes in the tree
        :param parent_nodes: List of parent nodes
        :return: number of internal nodes
        """
        if not parent_nodes:
            logging.error("No parent nodes found")
            raise EmptyTreeException("No parent nodes found")
        num_internal_nodes = len(set(parent_nodes)) - 1
        return num_internal_nodes

    def print_tree(self, node, tree_format):
        """
        Returns printable tree format
        :param node: node from which tree needs to be printed
        :param tree_format: string to represent tree
        :return: tree format in the form parent(child)
        """
        if node is None:
            logging.error("Tree is empty. Cannot print anything")
            raise EmptyTreeException("Tree is empty. Cannot print anything")
        tree_format += str(node.key) + '('
        for i in range(len(node.children)):
            child = node.children[i]
            end = ',' if i < len(node.children) - 1 else ''
            tree_format = self.print_tree(child, tree_format) + end
        tree_format += ')'
        return tree_format

    def __str__(self):
        return self.print_tree(self.root, "")


if __name__ == "__main__":
    tree = GenericTree()
    parent_nodes = tree.create_tree(20)
    logging.info("Tree looks like {}".format(tree))
    logging.info("Number of internal nodes in the tree = {}".format(tree.num_internal_nodes(parent_nodes)))