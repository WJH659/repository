class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BST:
    def __init__(self):
        self.root = None

    # 任务一：插入节点
    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert(self.root, val)

    def _insert(self, node, val):
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert(node.left, val)
        elif val > node.val:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert(node.right, val)

    # 任务二：删除节点 (策略选择)
    def delete(self, val, strategy="successor"):
        self.root = self._delete(self.root, val, strategy)

    def _delete(self, node, val, strategy):
        if not node: 
            return None
        
        if val < node.val:
            node.left = self._delete(node.left, val, strategy)
        elif val > node.val:
            node.right = self._delete(node.right, val, strategy)
        else:
            # 找到要删除的节点
            if not node.left and not node.right: 
                return None
            elif not node.left: 
                return node.right
            elif not node.right: 
                return node.left
            else:
                # 有两个子节点，根据策略选择替换者
                if strategy == "predecessor":
                    predecessor = self._get_max(node.left)
                    node.val = predecessor.val
                    node.left = self._delete(node.left, predecessor.val, strategy)
                else:
                    successor = self._get_min(node.right)
                    node.val = successor.val
                    node.right = self._delete(node.right, successor.val, strategy)
        return node

    def _get_min(self, node):
        while node.left: node = node.left
        return node

    def _get_max(self, node):
        while node.right: node = node.right
        return node

    # 核心：按层级格式化打印树（修复版）
    def print_tree(self):
        if not self.root:
            print("Empty Tree")
            return
            
        lines = self._build_display(self.root)
        for line in lines:
            print(line)

    def _build_display(self, node):
        if not node:
            return []
    
        line = str(node.val)
        left_lines = self._build_display(node.left)
        right_lines = self._build_display(node.right)
    
    # 叶子节点
        if not left_lines and not right_lines:
            width = max(4, len(line) + 2)
            pad = ' ' * ((width - len(line)) // 2)
            return [pad + line + ' ' * (width - len(pad) - len(line))]
    
    # 只有左子树
        if not right_lines:
            lw = len(left_lines[0])
            pad = ' ' * ((lw - len(line)) // 2)
            current_line = pad + line + ' ' * (lw - len(pad) - len(line))
            return [current_line] + left_lines
    
    # 只有右子树
        if not left_lines:
            rw = len(right_lines[0])
            pad = ' ' * ((rw - len(line)) // 2)
            current_line = pad + line + ' ' * (rw - len(pad) - len(line))
            return [current_line] + right_lines
    
    # 同时有左右子树
        lw = len(left_lines[0])
        rw = len(right_lines[0])
    
    # 增加一点间距，让树更美观
        spacing = 2  # 左右子树之间的间距
        total_width = lw + rw + spacing
    
    # 将当前节点放在总宽度的中心
        pad_left = ' ' * ((total_width - len(line)) // 2)
        current_line = pad_left + line + ' ' * (total_width - len(pad_left) - len(line))
    
        result = []
        max_h = max(len(left_lines), len(right_lines))
    
        for i in range(max_h):
            l_str = left_lines[i] if i < len(left_lines) else ' ' * lw
            r_str = right_lines[i] if i < len(right_lines) else ' ' * rw
            result.append(l_str + ' ' * spacing + r_str)
    
        return [current_line] + result


# ================= 执行任务 =================
if __name__ == "__main__":
    sequence = [50, 30, 70, 20, 40, 60, 80]
    
    # 任务一：构建并打印初始 BST
    print("=== 任务一：初始 BST ===")
    bst = BST()
    for num in sequence: bst.insert(num)
    bst.print_tree()
    
    print("\n=== 任务二：删除根节点 50 (中序后继策略) ===")
    bst_succ = BST()
    for num in sequence: bst_succ.insert(num)
    bst_succ.delete(50, strategy="successor")
    bst_succ.print_tree()
    
    print("\n=== 任务二：删除根节点 50 (中序前驱策略) ===")
    bst_pred = BST()
    for num in sequence: bst_pred.insert(num)
    bst_pred.delete(50, strategy="predecessor")
    bst_pred.print_tree()