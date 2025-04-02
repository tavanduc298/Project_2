import os
from datetime import datetime

class FileManager:
    def get_file_info(self, path):
        """Lấy thông tin về một tệp tin hoặc thư mục."""
        try:
            stats = os.stat(path)  # Lấy thông tin thuộc tính của tệp/thư mục
            info = {
                "name": os.path.basename(path),  # Lấy tên tệp/thư mục
                "attributes": self.get_attributes(path),  # Lấy danh sách thuộc tính
                "date_created": datetime.fromtimestamp(stats.st_ctime).date(),  # Ngày tạo
                "time_created": datetime.fromtimestamp(stats.st_ctime).time(),  # Thời gian tạo
            }
            if os.path.isfile(path):  # Nếu là tệp tin, thêm thông tin về kích thước
                info["size"] = stats.st_size  
            return info
        except Exception as e:
            return {"error": str(e)}  # Xử lý lỗi nếu có

    def get_attributes(self, path):
        """Lấy các thuộc tính của tệp/thư mục."""
        attrs = []
        if os.path.isfile(path):
            attrs.append("File")  # Là tệp tin
        if os.path.isdir(path):
            attrs.append("Directory")  # Là thư mục
        if os.access(path, os.R_OK):
            attrs.append("Readable")  # Có quyền đọc
        if os.access(path, os.W_OK):
            attrs.append("Writable")  # Có quyền ghi
        return attrs

    def get_text_content(self, path):
        """Đọc nội dung văn bản từ tệp tin."""
        if os.path.isfile(path) and path.lower().endswith(('.txt', '.log')):  # Chỉ đọc tệp .txt, .log
            try:
                with open(path, 'r', errors='ignore') as f:
                    return f.read()  # Đọc toàn bộ nội dung tệp
            except Exception as e:
                return f"Lỗi khi đọc nội dung: {str(e)}"  # Xử lý lỗi khi đọc
        return ""

    def list_directory(self, path):
        """Liệt kê nội dung của một thư mục."""
        try:
            return os.listdir(path)  # Lấy danh sách tệp/thư mục bên trong
        except PermissionError:
            return []  # Trả về danh sách rỗng nếu không có quyền truy cập
        except Exception as e:
            return [f"Lỗi: {str(e)}"]  # Xử lý lỗi khác nếu có
