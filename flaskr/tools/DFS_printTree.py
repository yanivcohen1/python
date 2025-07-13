def print_res(ans, expcted):
    print("" if ans == expcted else "         ", ans, "" if ans == expcted else "\nexpected:",
            "" if ans == expcted else expcted)
class TreeNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def printTree(node, level=0):
    if node != None:
        # print(' ' * 4 * level + '-> ' + str(node.value)) # print from top to bottom, print left first
        printTree(node.right, level + 1)
        val = ""
        try: val = node.value
        except: val = node.val
        print(' ' * 4 * level + '-> ' + str(val)) # print from left to top and then to right, print left first
        printTree(node.left, level + 1)
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

if __name__ == '__main__':
    t = TreeNode(1, TreeNode(2, TreeNode(4, TreeNode(7)),   TreeNode(9)),
            TreeNode(3, TreeNode(5),    TreeNode(6)))
    printTree(t)
#             -> 7
#         -> 4
#     -> 2
#         -> 9
# -> 1
#         -> 5
#     -> 3
#         -> 6

    print_res(returnTree(t), [1, 2, 3, 4, 9, 5, 6, 7, None])

    t = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
    print_res(printList(t), [1, 2, 3, 4])
