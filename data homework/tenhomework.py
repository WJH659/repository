class BTreeNode:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t  # 最小度数，3阶B-Tree的t=2
    
    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t - 1):
            new_root = BTreeNode(False)
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.root = new_root
            self.insert_non_full(new_root, k)
        else:
            self.insert_non_full(root, k)
    
    def split_child(self, parent, i):
        t = self.t
        full_child = parent.children[i]
        new_child = BTreeNode(full_child.leaf)
        
        # 获取中间键值（索引t-1）
        mid_key = full_child.keys[t-1]
        
        # 新节点获得右半部分键值
        new_child.keys = full_child.keys[t:]
        
        # 原节点保留左半部分键值（不包括中间键值）
        full_child.keys = full_child.keys[:t-1]
        
        # 如果不是叶子节点，移动子节点
        if not full_child.leaf:
            new_child.children = full_child.children[t:]
            full_child.children = full_child.children[:t]
        
        # 将中间键值插入到父节点
        parent.keys.insert(i, mid_key)
        parent.children.insert(i + 1, new_child)
    
    def insert_non_full(self, node, k):
        i = len(node.keys) - 1
        
        if node.leaf:
            # 在叶子节点中插入键值
            node.keys.append(k)
            # 保持键值有序
            node.keys.sort()
        else:
            # 找到合适的子树
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            
            # 如果子节点已满，先分裂
            if len(node.children[i].keys) == (2 * self.t - 1):
                self.split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], k)
    
    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        
        indent = "  " * level
        keys_str = ", ".join(map(str, node.keys))
        node_type = "Leaf" if node.leaf else "Internal"
        children_count = len(node.children)
        
        print(f"{indent}[{keys_str}] ({children_count} children, {node_type})")
        
        if not node.leaf:
            for child in node.children:
                self.print_tree(child, level + 1)
    
    def verify_properties(self):
        print("\n验证B-Tree性质：")
        print("=" * 50)
        
        # 性质1：所有叶子节点在同一层
        leaf_levels = []
        self._collect_leaf_levels(self.root, 0, leaf_levels)
        same_level = len(set(leaf_levels)) == 1
        print(f"1. 所有叶子节点在同一层: {'✓' if same_level else '✗'}")
        
        # 性质2：每个节点最多有2t-1个键值
        max_keys = 2 * self.t - 1
        valid_key_count = self._check_key_count(self.root, max_keys)
        print(f"2. 每个节点最多有 {max_keys} 个键值: {'✓' if valid_key_count else '✗'}")
        
        # 性质3：根节点至少有1个键值
        root_valid = len(self.root.keys) >= 1
        print(f"3. 根节点至少有1个键值: {'✓' if root_valid else '✗'}")
        
        # 性质4：非根节点至少有t-1个键值
        min_keys = self.t - 1
        non_root_valid = self._check_non_root_keys(self.root, min_keys)
        print(f"4. 非根节点至少有 {min_keys} 个键值: {'✓' if non_root_valid else '✗'}")
        
        # 性质5：键值按非降序排列
        sorted_keys = self._check_sorted(self.root)
        print(f"5. 键值按非降序排列: {'✓' if sorted_keys else '✗'}")
        
        # 性质6：内部节点的子节点数量 = 键值数量 + 1
        child_count_valid = self._check_child_count(self.root)
        print(f"6. 内部节点的子节点数量 = 键值数量 + 1: {'✓' if child_count_valid else '✗'}")
        
        # 性质7：所有键值都是唯一的
        unique_keys = self._check_unique_keys(self.root)
        print(f"7. 所有键值都是唯一的: {'✓' if unique_keys else '✗'}")
        
        # 性质8：BST分隔性质
        bst_property = self._check_bst_property(self.root)
        print(f"8. BST分隔性质: {'✓' if bst_property else '✗'}")
        
        return all([same_level, valid_key_count, root_valid, non_root_valid, 
                   sorted_keys, child_count_valid, unique_keys, bst_property])
    
    def _collect_leaf_levels(self, node, level, leaf_levels):
        if node.leaf:
            leaf_levels.append(level)
        else:
            for child in node.children:
                self._collect_leaf_levels(child, level + 1, leaf_levels)
    
    def _check_key_count(self, node, max_keys):
        if len(node.keys) > max_keys:
            return False
        if not node.leaf:
            for child in node.children:
                if not self._check_key_count(child, max_keys):
                    return False
        return True
    
    def _check_non_root_keys(self, node, min_keys, is_root=True):
        if not is_root and len(node.keys) < min_keys:
            return False
        if not node.leaf:
            for child in node.children:
                if not self._check_non_root_keys(child, min_keys, False):
                    return False
        return True
    
    def _check_sorted(self, node):
        for i in range(1, len(node.keys)):
            if node.keys[i] <= node.keys[i-1]:
                return False
        if not node.leaf:
            for child in node.children:
                if not self._check_sorted(child):
                    return False
        return True
    
    def _check_child_count(self, node):
        # 只对内部节点检查：子节点数量 = 键值数量 + 1
        if not node.leaf:  # 内部节点
            expected_children = len(node.keys) + 1
            if len(node.children) != expected_children:
                return False
            for child in node.children:
                if not self._check_child_count(child):
                    return False
        # 叶子节点没有子节点，不需要检查
        return True
    
    def _check_unique_keys(self, node, seen=None):
        if seen is None:
            seen = set()
        for key in node.keys:
            if key in seen:
                return False
            seen.add(key)
        if not node.leaf:
            for child in node.children:
                if not self._check_unique_keys(child, seen):
                    return False
        return True
    
    def _check_bst_property(self, node):
        if node.leaf:
            return True
        
        for i in range(len(node.keys)):
            # 左子树的所有键值应小于node.keys[i]
            if i < len(node.children):
                left_keys = self._get_all_keys(node.children[i])
                if any(k >= node.keys[i] for k in left_keys):
                    return False
            
            # 右子树的所有键值应大于node.keys[i]
            if i + 1 < len(node.children):
                right_keys = self._get_all_keys(node.children[i + 1])
                if any(k <= node.keys[i] for k in right_keys):
                    return False
        
        for child in node.children:
            if not self._check_bst_property(child):
                return False
        return True
    
    def _get_all_keys(self, node):
        keys = node.keys.copy()
        if not node.leaf:
            for child in node.children:
                keys.extend(self._get_all_keys(child))
        return keys

# ================= 主程序 =================
if __name__ == "__main__":
    print("构建3阶B-Tree")
    print("插入序列: [10, 20, 5, 6, 12, 30, 25]")
    print("=" * 60)
    
    # 创建3阶B-Tree（t=2）
    btree = BTree(t=2)
    
    # 逐步插入并显示过程
    sequence = [10, 20, 5, 6, 12, 30, 25]
    for i, key in enumerate(sequence):
        print(f"\n步骤 {i+1}: 插入 {key}")
        btree.insert(key)
        print("当前树结构:")
        btree.print_tree()
    
    print("\n" + "=" * 60)
    print("最终3阶B-Tree结构:")
    btree.print_tree()
    
    # 验证B-Tree性质
    all_valid = btree.verify_properties()
    
    print("\n" + "=" * 60)
    print(f"所有B-Tree性质验证: {'全部通过 ✓' if all_valid else '存在错误 ✗'}")
    
    # 保存到文件
    with open("correct_btree_report.txt", "w", encoding="utf-8") as f:
        f.write("3阶B-Tree构建报告（正确版本）\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"插入序列: {sequence}\n\n")
        
        f.write("最终树结构:\n")
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        btree.print_tree()
        sys.stdout = old_stdout
        tree_output = buffer.getvalue()
        f.write(tree_output)
        
        f.write("\n性质验证结果:\n")
        f.write(f"所有性质验证: {'全部通过' if all_valid else '存在错误'}\n")
    
    print("\ncorrect_btree_report.txt 已生成")