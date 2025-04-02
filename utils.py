def format_size(bytes_size):
    """Chuyển đổi dung lượng từ byte sang định dạng dễ đọc hơn."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:  # Danh sách các đơn vị
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"  # Trả về giá trị với 2 chữ số thập phân
        bytes_size /= 1024  # Chia để chuyển sang đơn vị cao hơn
    return f"{bytes_size:.2f} TB"  # Trả về giá trị tính theo TB nếu lớn hơn GB
