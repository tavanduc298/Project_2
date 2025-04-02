import tkinter as tk
from tkinter import ttk

class PartitionGUI:
    def __init__(self, root):
        """Khởi tạo giao diện đồ họa hiển thị phân vùng."""
        self.root = root
        self.root.title("Partition Viewer") # Tiêu đề cửa sổ
        self.root.geometry("800x600")   # Kích thước cửa sổ

         # Khung chính
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Nhãn hiển thị danh sách phân vùng
        self.partition_label = ttk.Label(self.main_frame, text="Detected Partitions:")
        self.partition_label.pack()
        
         # Danh sách chọn phân vùng
        self.partition_var = tk.StringVar()
        self.partition_dropdown = ttk.Combobox(self.main_frame, textvariable=self.partition_var)
        self.partition_dropdown.pack(pady=5)

       # Cây thư mục hiển thị nội dung của phân vùng
        self.tree = ttk.Treeview(self.main_frame, columns=("format"), selectmode="browse")
        self.tree.heading("#0", text="Directory Tree")  # Cột chính hiển thị cây thư mục
        self.tree.heading("format", text="Format")  # Cột hiển thị định dạng của thư mục/tệp
        self.tree.pack(fill="both", expand=True, side="left")

        # Thanh cuộn dọc cho cây thư mục
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="left", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Khung thông tin tệp/thư mục
        self.info_frame = ttk.LabelFrame(self.main_frame, text="File/Folder Info")
        self.info_frame.pack(side="right", fill="both", expand=True, padx=10)

        # Ô hiển thị thông tin của tệp/thư mục
        self.info_text = tk.Text(self.info_frame, height=10, width=40)
        self.info_text.pack(pady=5)

        # Ô hiển thị nội dung tệp (nếu là tệp văn bản)
        self.content_text = tk.Text(self.info_frame, height=10, width=40)
        self.content_text.pack(pady=5)

    def set_partition_options(self, partitions):
        """Thiết lập danh sách phân vùng trong dropdown."""
        self.partition_dropdown['values'] = list(partitions.keys())
        if partitions:  # Nếu có phân vùng, chọn phần tử đầu tiên làm mặc định
            self.partition_dropdown.set(list(partitions.keys())[0])

    def clear_tree(self):
        """Xóa toàn bộ dữ liệu trong cây thư mục."""
        self.tree.delete(*self.tree.get_children())

    def clear_info(self):
        """Xóa nội dung hiển thị trong khung thông tin và nội dung tệp."""
        self.info_text.delete(1.0, tk.END)
        self.content_text.delete(1.0, tk.END)