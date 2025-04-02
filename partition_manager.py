class PartitionManager:
    def __init__(self):
        """Khởi tạo đối tượng quản lý phân vùng."""
        self.partitions = {}  # Lưu danh sách các phân vùng và định dạng của chúng

    def detect_partitions(self):
        """Phát hiện các phân vùng trên hệ thống.
        
        Phiên bản đơn giản - trong thực tế cần sử dụng các API hệ thống 
        như `psutil` (Linux, Windows) hoặc `wmi` (Windows).
        """
        self.partitions = {
            "D:": "FAT32",  # Phân vùng D: có định dạng FAT32
            "E:": "NTFS"   # Phân vùng E: có định dạng NTFS
        }
        return self.partitions  # Trả về danh sách phân vùng
