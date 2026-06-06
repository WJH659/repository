class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def array_to_binary_tree(arr):
    """将数组转换为二叉树"""
    if not arr or arr[0] is None:
        return None
    
    root = TreeNode(arr[0])
    queue = [root]
    index = 1
    
    while queue and index < len(arr):
        node = queue.pop(0)
        
        # 处理左子节点
        if index < len(arr) and arr[index] is not None:
            node.left = TreeNode(arr[index])
            queue.append(node.left)
        index += 1
        
        # 处理右子节点
        if index < len(arr) and arr[index] is not None:
            node.right = TreeNode(arr[index])
            queue.append(node.right)
        index += 1
            
    return root

def get_tree_height(root):
    """获取树的高度"""
    if not root:
        return 0
    return 1 + max(get_tree_height(root.left), get_tree_height(root.right))

def print_pretty_tree(root):
    """以美观的图形化方式打印二叉树"""
    if not root:
        return
    
    height = get_tree_height(root)
    # 最底层需要的宽度 (假设每个数字占1个字符宽度)
    max_width = (2 ** height) - 1 
    # 存储每一行的字符串内容
    result_lines = [" " * max_width for _ in range(height)]

    def fill_line(node, level, pos):
        if not node:
            return
        # 将当前节点的值放入对应的位置
        result_lines[level] = result_lines[level][:pos] + str(node.val) + result_lines[level][pos+1:]
        
        # 计算下一层左右子节点的相对偏移量
        offset = 2 ** (height - level - 2)
        
        # 填充连线 '/' 和 '\'
        if node.left:
            # 在当前位置和左子节点位置之间画 '/'
            result_lines[level + 1] = result_lines[level + 1][:pos - offset] + "/" + result_lines[level + 1][pos - offset + 1:]
            fill_line(node.left, level + 1, pos - offset)
            
        if node.right:
            # 在当前位置和右子节点位置之间画 '\'
            result_lines[level + 1] = result_lines[level + 1][:pos + offset] + "\\" + result_lines[level + 1][pos + offset + 1:]
            fill_line(node.right, level + 1, pos + offset)

    # 根节点从中间位置开始
    root_pos = max_width // 2
    fill_line(root, 0, root_pos)
    
    # 打印结果
    for line in result_lines:
        print(line.rstrip())

# ================= 测试执行 =================
arr = [10, 5, 15, 3, 7, None, 20]
tree_root = array_to_binary_tree(arr)

print("还原后的二叉树形态如下：")
print_pretty_tree(tree_root)