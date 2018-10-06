from collections import deque
arr = [1, 2, 3, 4, 5, 6, 7, None, 8, 9, 10]
arr2 = [1, 2, 3, 4, 5, 6, None, 7, 8, None, 9, 10, 11, 12, 13, 14, 15, 16, 17]
arr3 = [1, None, None, 2, 3, 4]
arr4 = [1, None, 2, 3, 4, 5, None, 6, 7, 8, None, 9, 10]


class Node:
    def __init__(self, value, next_node, lc, rc, parent):
        self.next_node = next_node
        self.left_child = lc
        self.right_child = rc
        self.parent = parent
        self.value = value

    def __str__(self):
        return str(self.value)


def print_tree(root):
    thislevel = [root]
    while thislevel:
        nextlevel = list()
        for n in thislevel:
            print(n.value, " ", end="")
            if n.left_child: nextlevel.append(n.left_child)
            if n.right_child: nextlevel.append(n.right_child)
        print ("\n")
        thislevel = nextlevel

def parse(input_array):
    root = None
    curr = root
    last_placed = None
    for item in input_array:
        new_node = Node(item, None, None, None, None)

        print(item)

        if root is None:
            root = new_node
            curr = root
            last_placed = root
            continue

        if curr is None:
            raise Exception("Invalid input provided")

        if curr.left_child is None:
            curr.left_child = new_node
        elif curr.right_child is None:
            curr.right_child = new_node

        if new_node.value is not None:
            last_placed.next_node = new_node
            last_placed = new_node

        if curr.right_child is not None:
            curr = curr.next_node

    return root

def spiral_traverse(root):
    thislevel = [root]
    level = 0
    while thislevel:
        nextlevel = list()
        printList = thislevel
        if level % 2 == 1:
            printList = reversed(thislevel)

        for n in printList:
            print(n.value)

        for n in thislevel:
            if n.left_child: nextlevel.append(n.left_child)
            if n.right_child: nextlevel.append(n.right_child)
        thislevel = nextlevel
        level += 1

def print_in_order(root):
    while root is not None:
        print(root.value)
        root = root.next_node

root = parse(arr4)
print_tree(root=root)
spiral_traverse(root)
