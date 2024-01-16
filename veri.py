class TreeNode:
    def __init__(self, student_no, name, surname, age):
        self.student_no = student_no
        self.name = name
        self.surname = surname
        self.age = age
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def update_height(self, node):
        if node is not None:
            node.height = 1 + max(self.height(node.left), self.height(node.right))

    def balance_factor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def insert(self, root, student_no, name, surname, age):
        if root is None:
            return TreeNode(student_no, name, surname, age)

        if student_no < root.student_no:
            root.left = self.insert(root.left, student_no, name, surname, age)
        elif student_no > root.student_no:
            root.right = self.insert(root.right, student_no, name, surname, age)
        else:
            # Duplicate student_no, do not allow
            print(f"Öğrenci No {student_no} zaten mevcut.")
            return root

        self.update_height(root)

        balance = self.balance_factor(root)

        # Left-Left Case
        if balance > 1 and student_no < root.left.student_no:
            return self.rotate_right(root)

        # Right-Right Case
        if balance < -1 and student_no > root.right.student_no:
            return self.rotate_left(root)

        # Left-Right Case
        if balance > 1 and student_no > root.left.student_no:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Right-Left Case
        if balance < -1 and student_no < root.right.student_no:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def insert_student(self, student_no, name, surname, age):
        self.root = self.insert(self.root, student_no, name, surname, age)

    def inorder_traversal(self, root):
        if root:
            self.inorder_traversal(root.left)
            print(f"Öğrenci No: {root.student_no}, İsim: {root.name}, Soyisim: {root.surname}, Yaş: {root.age}")
            self.inorder_traversal(root.right)

    def preorder_traversal(self, root):
        if root:
            print(f"Öğrenci No: {root.student_no}, İsim: {root.name}, Soyisim: {root.surname}, Yaş: {root.age}")
            self.preorder_traversal(root.left)
            self.preorder_traversal(root.right)

    def postorder_traversal(self, root):
        if root:
            self.postorder_traversal(root.left)
            self.postorder_traversal(root.right)
            print(f"Öğrenci No: {root.student_no}, İsim: {root.name}, Soyisim: {root.surname}, Yaş: {root.age}")

    def delete_node(self, root, student_no):
        if root is None:
            return root

        if student_no < root.student_no:
            root.left = self.delete_node(root.left, student_no)
        elif student_no > root.student_no:
            root.right = self.delete_node(root.right, student_no)
        else:
            # Node with only one child or no child
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            # Node with two children: Get the inorder successor (smallest
            # in the right subtree)
            successor = self.min_value_node(root.right)

            # Copy the inorder successor's content to this node
            root.student_no = successor.student_no
            root.name = successor.name
            root.surname = successor.surname
            root.age = successor.age

            # Delete the inorder successor
            root.right = self.delete_node(root.right, successor.student_no)

        # If the tree has only one node, return
        if root is None:
            return root

        # Update height of the current node
        self.update_height(root)

        # Balance the tree
        balance = self.balance_factor(root)

        # Left-Left Case
        if balance > 1 and self.balance_factor(root.left) >= 0:
            return self.rotate_right(root)

        # Right-Right Case
        if balance < -1 and self.balance_factor(root.right) <= 0:
            return self.rotate_left(root)

        # Left-Right Case
        if balance > 1 and self.balance_factor(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Right-Left Case
        if balance < -1 and self.balance_factor(root.right) > 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def find_node(self, root, student_no):
        if not root or root.student_no == student_no:
            return root

        if student_no < root.student_no:
            return self.find_node(root.left, student_no)

        return self.find_node(root.right, student_no)

    def subtree_size(self, root):
        if root is None:
            return 0
        return 1 + self.subtree_size(root.left) + self.subtree_size(root.right)

    def find_min_max_values(self, root):
        if root is None:
            return None, None

        min_node = root
        while min_node.left is not None:
            min_node = min_node.left

        max_node = root
        while max_node.right is not None:
            max_node = max_node.right

        return min_node.student_no, max_node.student_no

    def print_leaves(self, root):
        if root:
            if root.left is None and root.right is None:
                print(f"Yaprak - Öğrenci No: {root.student_no}, İsim: {root.name}, Soyisim: {root.surname}, Yaş: {root.age}")
            self.print_leaves(root.left)
            self.print_leaves(root.right)


def main():
    avl_tree = AVLTree()

    with open("Ogrenci.txt", "r") as file:
        lines = file.readlines()
        for line in lines[1:]:  # İlk satır başlık olduğu için atlıyoruz
            student_info = line.strip().split("\t")
            student_no = int(student_info[0])
            name = student_info[1]
            surname = student_info[2]
            age = int(student_info[3])

            avl_tree.insert_student(student_no, name, surname, age)

    while True:
        print("\n1. Yeni öğrenci ekleyin")
        print("2. Inorder sıralama")
        print("3. Preorder sıralama")
        print("4. Postorder sıralama")
        print("5. Öğrenci sil")
        print("6. Subtree boyutu")
        print("7. Min-Max değerleri")
        print("8. Yaprakları listele")
        print("9. Çıkış")

        choice = int(input("Seçiminizi yapın: "))

        if choice == 1:
            new_student_no = int(input("Yeni öğrenci numarası girin: "))
            new_name = input("İsim girin: ")
            new_surname = input("Soyisim girin: ")
            new_age = int(input("Yaş girin: "))
            avl_tree.insert_student(new_student_no, new_name, new_surname, new_age)

        elif choice == 2:
            print("\nInorder sıralama:")
            avl_tree.inorder_traversal(avl_tree.root)

        elif choice == 3:
            print("\nPreorder sıralama:")
            avl_tree.preorder_traversal(avl_tree.root)

        elif choice == 4:
            print("\nPostorder sıralama:")
            avl_tree.postorder_traversal(avl_tree.root)

        elif choice == 5:
            delete_student_no = int(input("Silmek istediğiniz öğrenci numarasını girin: "))
            avl_tree.delete_node(avl_tree.root, delete_student_no)
            print("\nÖğrenci silindi. Güncel ağaç görünümü:")
            avl_tree.inorder_traversal(avl_tree.root)

        elif choice == 6:
            subtree_root_student_no = int(input("Subtree boyutunu öğrenmek istediğiniz öğrenci numarasını girin: "))
            subtree_root = avl_tree.find_node(avl_tree.root, subtree_root_student_no)
            size = avl_tree.subtree_size(subtree_root)
            print(f"\nSubtree boyutu: {size}")

        elif choice == 7:
            min_val, max_val = avl_tree.find_min_max_values(avl_tree.root)
            print(f"\nEn küçük değer: {min_val}\nEn büyük değer: {max_val}")

        elif choice == 8:
            print("\nYaprakları listele:")
            avl_tree.print_leaves(avl_tree.root)

        elif choice == 9:
            print("Programdan çıkılıyor.")
            break

        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
