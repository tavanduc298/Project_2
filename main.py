from gui import PartitionGUI
from partition_manager import PartitionManager
from file_manager import FileManager
import tkinter as tk

class PartitionViewerApp:
    def __init__(self):
        """Khởi tạo ứng dụng giao diện xem phân vùng."""
        self.root = tk.Tk()  # Tạo cửa sổ chính
        self.gui = PartitionGUI(self.root)  # Khởi tạo giao diện
        self.partition_mgr = PartitionManager()  # Quản lý phân vùng
        self.file_mgr = FileManager()  # Quản lý tệp tin

        # Gán sự kiện
        self.gui.partition_dropdown.bind('<<ComboboxSelected>>', self.load_directory_tree)  # Xử lý khi chọn phân vùng
        self.gui.tree.bind('<<TreeviewSelect>>', self.display_info)  # Xử lý khi chọn một thư mục/tệp

        # Thiết lập ban đầu
        self.setup_partitions()
        self.root.mainloop()  # Chạy vòng lặp giao diện

    def setup_partitions(self):
        """Thiết lập danh sách phân vùng khi khởi động."""
        partitions = self.partition_mgr.detect_partitions()  # Phát hiện các phân vùng
        self.gui.set_partition_options(partitions)  # Cập nhật danh sách phân vùng trong giao diện

    def load_directory_tree(self, event=None):
        """Tải cây thư mục của phân vùng được chọn."""
        self.gui.clear_tree()  # Xóa cây thư mục cũ
        selected_partition = self.gui.partition_var.get()  # Lấy phân vùng đang chọn
        if not selected_partition:
            return  # Không làm gì nếu không có phân vùng nào được chọn

        format_type = self.partition_mgr.partitions[selected_partition]  # Lấy định dạng của phân vùng
        root_node = self.gui.tree.insert("", "end", text=selected_partition, 
                                       values=(format_type,), open=True)  # Thêm phân vùng vào cây thư mục
        
        for item in self.file_mgr.list_directory(selected_partition):  # Duyệt qua các tệp/thư mục trong phân vùng
            full_path = f"{selected_partition}/{item}"  # Đường dẫn đầy đủ
            node = self.gui.tree.insert(root_node, "end", text=item)  # Thêm tệp/thư mục vào cây
            if self.file_mgr.get_file_info(full_path).get("attributes", []).count("Directory"):
                self.gui.tree.insert(node, "end", text="Loading...")  # Nếu là thư mục, thêm một node tạm thời

    def display_info(self, event):
        """Hiển thị thông tin của tệp/thư mục được chọn."""
        selected_item = self.gui.tree.selection()  # Lấy mục được chọn trong cây thư mục
        if not selected_item:
            return  # Nếu không có gì được chọn thì thoát

        # Duyệt lên cây thư mục để lấy đường dẫn đầy đủ
        path_parts = []
        current = selected_item[0]
        while current:
            path_parts.append(self.gui.tree.item(current)["text"])
            current = self.gui.tree.parent(current)
        
        path = "/".join(reversed(path_parts))  # Ghép lại thành đường dẫn
        self.gui.clear_info()  # Xóa thông tin cũ

        info_dict = self.file_mgr.get_file_info(path)  # Lấy thông tin về tệp/thư mục
        if "error" in info_dict:
            self.gui.info_text.insert(tk.END, f"Lỗi: {info_dict['error']}")  # Hiển thị lỗi nếu có
            return

        # Hiển thị thông tin về tệp/thư mục
        info_text = (f"Tên: {info_dict['name']}\n"
                    f"Thuộc tính: {', '.join(info_dict['attributes'])}\n"
                    f"Ngày tạo: {info_dict['date_created']}\n"
                    f"Thời gian tạo: {info_dict['time_created']}\n")
        if "size" in info_dict:
            info_text += f"Kích thước: {info_dict['size']} bytes\n"

        self.gui.info_text.insert(tk.END, info_text)  # Hiển thị thông tin trong khung bên phải
        content = self.file_mgr.get_text_content(path)  # Lấy nội dung của tệp (nếu có)
        if content:
            self.gui.content_text.insert(tk.END, content)  # Hiển thị nội dung của tệp văn bản

if __name__ == "__main__":
    PartitionViewerApp()  # Khởi chạy ứng dụng
