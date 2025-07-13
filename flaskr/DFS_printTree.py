def print_res(ans, expcted):
    print("" if ans == expcted else "         ", ans, "" if ans == expcted else "\nexpected:",
            "" if ans == expcted else expcted)
class TreeNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def printTree(node, level=0, side=""):
    if node != None:
        # print(' ' * 4 * level + '-> ' + str(node.value)) # print from top to bottom, print left first
        printTree(node.right, level + 1, side="R")
        val = ""
        try: val = node.value
        except: val = node.val
        print(' ' * 4 * level + side + '-> ' + str(val)) # print from left to top and then to right, print left first
        printTree(node.left, level + 1, side="L")
        # print(' ' * 4 * level + '-> ' + str(node.value)) # print from bottom to top, print left first

def returnTree(root, level=0):
    res = []
    stack = [root]
    while stack:
        node = stack.pop(0)
        val = ""
        if not node:
            res.append(None)
        else:
            try: val = node.value
            except: val = node.val
            res.append(val)
            if node.right or node.left:
                stack.append(node.left)
                stack.append(node.right)

    return res

class ListNode:
    def __init__(self, x, next=None):
        self.val = x
        self.next = next

def printList(list: ListNode):
    res = []
    while list:
        res.append(list.val)
        # print(list.val, end=" ")
        list = list.next
    # print()
    return res

def build_tree_from_list(lst, index=0):
    # Base case: out of bounds or placeholder
    if index >= len(lst) or lst[index] is None:
        return None
    # Create node and recursively build subtrees
    node = TreeNode(
        lst[index],
        build_tree_from_list(lst, 2 * index + 1),
        build_tree_from_list(lst, 2 * index + 2)
    )
    return node

def build_ascii_tree(node):
    if node is None:
        return [], 0, 0, 0

    # Recursively build left and right subtrees
    left_lines, left_width, left_height, left_middle = build_ascii_tree(node.left)
    right_lines, right_width, right_height, right_middle = build_ascii_tree(node.right)

    value_str = str(node.value)
    root_width = len(value_str)

    # Compute overall dimensions
    height = max(left_height, right_height) + 2
    width = left_width + root_width + right_width + 2
    middle = left_width + root_width // 2 + 1

    # Initialize blank canvas
    lines = [' ' * width for _ in range(height)]

    # Place root value on first line
    root_pos = left_width + 1
    lines[0] = lines[0][:root_pos] + value_str + lines[0][root_pos + root_width:]

    # Draw branch line dynamically scaled
    if node.left or node.right:
        # Create mutable list
        branch = list(' ' * width)
        # Compute left slash position
        if node.left:
            left_root = left_middle + 1
            branch[left_root] = '/'
        # Compute right slash position
        if node.right:
            right_root = left_width + root_width + 1 + right_middle
            branch[right_root] = '\\'
        # Fill underscores between slashes, excluding root span
        if node.left and node.right:
            start = left_root + 1
            end = right_root
        elif node.left:
            start = left_root + 1
            end = root_pos
        else:
            start = root_pos + root_width
            end = right_root
        for i in range(start, end):
            # Skip positions above root value
            if i < root_pos or i >= root_pos + root_width:
                branch[i] = '_'
        lines[1] = ''.join(branch)

    # Merge subtree lines
    for i in range(max(left_height, right_height)):
        l = left_lines[i] if i < left_height else ' ' * left_width
        r = right_lines[i] if i < right_height else ' ' * right_width
        # spaces under root and branches
        mid = ' ' * (root_width + 2)
        lines[i + 2] = l + mid + r

    return lines, width, height, middle

# Print function

def print_ascii_tree(node):
    for line in build_ascii_tree(node)[0]:
        print(line.rstrip())

if __name__ == '__main__':
    # print list
    lists = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
    print("compare list")
    print_res(printList(lists), [1, 2, 3, 4])

    # print tree
    tree = TreeNode(1,
                  TreeNode(2, # left
                          TreeNode(4, # left
                                    TreeNode(7)), # left
                          TreeNode(9)), # right
                  TreeNode(3, # right
                          TreeNode(5), # left
                          TreeNode(6))) # right
    print("\ndrow tree in 90 degree rotation")
    printTree(tree)
#         R-> 6
#     R-> 3
#         L-> 5
# -> 1
#         R-> 9
#     L-> 2
#         L-> 4
#             L-> 7

    # Print the tree with dynamic underscores
    print("\ndrow ascii_tree")
    print_ascii_tree(tree)
#              1
#         /____ ____\
#        2           3
#      /_ _\       /_ _\
#     4     9     5     6
#   /_
#  7

    # buld tree from list
    tree_from_list = [1, 2, 3, 4, 9, 5, 6, 7, None]
    tree2 = build_tree_from_list(tree_from_list)

    # test tree from list
    print("\ncompare tree")
    print_res(returnTree(tree), tree_from_list)
    print_res(returnTree(tree2), tree_from_list)
    print("is trees equals: ", returnTree(tree) == returnTree(tree2))
