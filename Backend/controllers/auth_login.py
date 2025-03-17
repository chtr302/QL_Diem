from Backend.database.connection import DatabaseConnection

class AuthLogin:
    @staticmethod
    def verify_student(student_id, password):
        try:
            cursor = DatabaseConnection.connection_admin().cursor()
            cursor.execute("{Call CheckSV (?, ?)}", (student_id, password))
            result = cursor.fetchone()
            if not result:
                return False, None, "Không tìm thấy thông tin sinh viên"
            status = result[0]
            if status == 1:
                try:
                    connect_sinh_vien = DatabaseConnection.connection_sv()
                    return True, connect_sinh_vien, "Đăng nhập thành công"
                except Exception as e:
                    return False, None, f"Có lỗi từ Login SV: {e}"
                finally:
                    cursor.close()
            else:
                return False, None, "Đăng nhập không thành công. Vui lòng kiểm tra Mã sinh viên và mật khẩu."
        except Exception as e:
            return False, None, f"Lỗi khi xác thực: {e}"

    @staticmethod
    def get_login_info(username):
        connection = DatabaseConnection.connection_admin()
        try:
            cursor = connection.cursor()
            cursor.execute('{Call CheckLogin (?)}', (username,))
            result = cursor.fetchone()
            if not result:
                return None
            login_info = {
                'MaGV': result[0],
                'HoTen': result[1],
                'Role': result[2]
            }
            return login_info
        except Exception as e:
            print(f'Error: {e}')
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def verify_teacher(username, password):
        login_info = AuthLogin.get_login_info(username)
        if not login_info:
            return False, None, None, "Đăng nhập không thành công. Vui lòng kiểm tra lại tài khoản và mật khẩu."
        
        try:
            connect_login = DatabaseConnection.connection_gv(username, password)
            if connect_login:
                return True, connect_login, login_info, "Đăng nhập thành công"
            else:
                return False, None, None, "Đăng nhập không thành công. Vui lòng kiểm tra lại tài khoản và mật khẩu."
        except Exception as e:
            return False, None, None, f"Lỗi kết nối: {e}"
