class TreeNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# Function to build ASCII representation of a binary tree
# Returns list of strings, width, height, and horizontal coordinate of the root

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

# Example usage and tests
if __name__ == "__main__":
    # Construct the tree
    t = TreeNode(1,
                  TreeNode(2,
                          TreeNode(4,
                                    TreeNode(7)),
                          TreeNode(9)),
                  TreeNode(3,
                          TreeNode(5),
                          TreeNode(6)))

    # Print the tree with dynamic underscores
    print_ascii_tree(t)
#              1
#         /____ ____\
#        2           3
#      /_ _\       /_ _\
#     4     9     5     6
#   /_
#  7
