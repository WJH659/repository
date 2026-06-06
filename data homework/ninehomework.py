class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
        self.rotation_count = 0
    
    def get_height(self, node):
        return node.height if node else 0
    
    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0
    
    def update_height(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    # 右旋（LL旋转）
    def rotate_right(self, y):
        print(f"🔄 执行右旋(LL旋转)：{y.val} 成为新的根节点")
        x = y.left
        T2 = x.right
        
        x.right = y
        y.left = T2
        
        self.update_height(y)
        self.update_height(x)
        self.rotation_count += 1
        
        return x
    
    # 左旋（RR旋转）
    def rotate_left(self, x):
        print(f"🔄 执行左旋(RR旋转)：{x.right.val} 成为新的根节点")
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        self.update_height(x)
        self.update_height(y)
        self.rotation_count += 1
        
        return y
    
    def insert(self, root, val):
        if not root:
            return AVLNode(val)
        
        if val < root.val:
            root.left = self.insert(root.left, val)
        elif val > root.val:
            root.right = self.insert(root.right, val)
        else:
            return root
        
        self.update_height(root)
        balance = self.get_balance(root)
        
        # 打印当前节点的平衡因子
        print(f"  节点 {root.val}: 高度={root.height}, 平衡因子={balance}")
        
        # LL型
        if balance > 1 and val < root.left.val:
            print(f"  ⚠️ 节点 {root.val} 失衡！类型：LL型")
            return self.rotate_right(root)
        
        # RR型
        if balance < -1 and val > root.right.val:
            print(f"  ⚠️ 节点 {root.val} 失衡！类型：RR型")
            return self.rotate_left(root)
        
        # LR型
        if balance > 1 and val > root.left.val:
            print(f"  ⚠️ 节点 {root.val} 失衡！类型：LR型")
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        
        # RL型
        if balance < -1 and val < root.right.val:
            print(f"  ⚠️ 节点 {root.val} 失衡！类型：RL型")
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        
        return root
    
    def insert_val(self, val):
        self.root = self.insert(self.root, val)
    
    def print_detailed_tree(self):
        """打印详细的树结构，包括每个节点的平衡因子"""
        print("\n📊 树结构详情（节点[值](高度,平衡因子)）：")
        self._print_detailed_node(self.root, 0)
    
    def _print_detailed_node(self, node, level):
        if node:
            indent = "  " * level
            balance = self.get_balance(node)
            print(f"{indent}{node.val}(h={node.height}, bf={balance})")
            self._print_detailed_node(node.left, level + 1)
            self._print_detailed_node(node.right, level + 1)
    
    def inorder_traversal(self, node, result=None):
        if result is None:
            result = []
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.val)
            self.inorder_traversal(node.right, result)
        return result
    
    def print_tree_visual(self):
        """可视化打印树结构"""
        if not self.root:
            print("空树")
            return
        
        lines = self._build_display(self.root)
        print("\n🌳 树形结构：")
        for line in lines:
            print(line)
    
    def _build_display(self, node):
        if not node:
            return []
        
        line = str(node.val)
        left_lines = self._build_display(node.left)
        right_lines = self._build_display(node.right)
        
        if not left_lines and not right_lines:
            width = max(4, len(line) + 2)
            pad = ' ' * ((width - len(line)) // 2)
            return [pad + line + ' ' * (width - len(pad) - len(line))]
        
        if not right_lines:
            lw = len(left_lines[0])
            pad = ' ' * ((lw - len(line)) // 2)
            current_line = pad + line + ' ' * (lw - len(pad) - len(line))
            return [current_line] + left_lines
        
        if not left_lines:
            rw = len(right_lines[0])
            pad = ' ' * ((rw - len(line)) // 2)
            current_line = pad + line + ' ' * (rw - len(pad) - len(line))
            return [current_line] + right_lines
        
        lw = len(left_lines[0])
        rw = len(right_lines[0])
        spacing = 2
        total_width = lw + rw + spacing
        
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
    print("=" * 60)
    print("AVL树构建过程演示")
    print("插入序列：[30, 20, 10, 25, 40, 35, 50]")
    print("=" * 60)
    
    avl = AVLTree()
    sequence = [30, 20, 10, 25, 40, 35, 50]
    
    for i, val in enumerate(sequence):
        print(f"\n{'='*60}")
        print(f"第 {i+1} 步：插入 {val}")
        print(f"{'='*60}")
        
        avl.insert_val(val)
        
        # 打印详细信息
        avl.print_detailed_tree()
        avl.print_tree_visual()
        
        # 验证
        inorder = avl.inorder_traversal(avl.root)
        print(f"\n✅ 中序遍历（BST验证）：{inorder}")
        
        # 检查平衡性
        def check_balance(node):
            if not node:
                return True, 0
            left_ok, left_h = check_balance(node.left)
            right_ok, right_h = check_balance(node.right)
            balanced = (left_ok and right_ok and abs(left_h - right_h) <= 1)
            return balanced, 1 + max(left_h, right_h)
        
        balanced, height = check_balance(avl.root)
        status = "✅ 平衡" if balanced else "❌ 失衡"
        print(f"📏 树高度：{height}，平衡状态：{status}")
    
    print(f"\n{'='*60}")
    print("最终AVL树统计")
    print(f"{'='*60}")
    print(f"总共执行了 {avl.rotation_count} 次旋转操作")
    
    final_inorder = avl.inorder_traversal(avl.root)
    print(f"最终中序遍历：{final_inorder}")
    
    # 最终验证
    is_bst = all(final_inorder[i] < final_inorder[i+1] for i in range(len(final_inorder)-1))
    print(f"BST性质验证：{'✅ 通过' if is_bst else '❌ 失败'}")
    
    def final_check(node):
        if not node:
            return True, 0
        left_ok, left_h = final_check(node.left)
        right_ok, right_h = final_check(node.right)
        balanced = (left_ok and right_ok and abs(left_h - right_h) <= 1)
        return balanced, 1 + max(left_h, right_h)
    
    final_balanced, final_height = final_check(avl.root)
    print(f"AVL平衡性验证：{'✅ 通过' if final_balanced else '❌ 失败'}")
    print(f"最终树高度：{final_height}")