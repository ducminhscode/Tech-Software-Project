# 🏥 Ứng Dụng Quản Lý Phòng Mạch Tư

Ứng dụng hỗ trợ quản lý phòng mạch tư nhân một cách hiệu quả, bao gồm đăng ký khám bệnh, lập phiếu khám, thanh toán hóa đơn, và báo cáo thống kê. Hệ thống tự động gửi thông báo qua email và cung cấp giao diện thân thiện cho các vai trò như bệnh nhân, y tá, bác sĩ, thu ngân, và quản trị viên.

---

## 🚀 Tính năng chính

- 📅 **Đăng ký và quản lý lịch khám**: Bệnh nhân đăng ký trực tuyến hoặc trực tiếp, y tá lập danh sách khám (tối đa 40 bệnh nhân/ngày).  
- 📧 **Thông báo qua email**: Gửi email xác nhận lịch khám và thông báo cho bệnh nhân.  
- 🩺 **Lập phiếu khám và kê đơn**: Bác sĩ tra cứu lịch sử bệnh, lập phiếu khám, kê toa thuốc với 30 loại thuốc chuẩn hóa.  
- 💳 **Thanh toán hóa đơn**: Thu ngân lập và tra cứu hóa đơn tiền khám + tiền thuốc, hỗ trợ thanh toán chính xác.  
- 📊 **Báo cáo thống kê**: Quản trị viên xem báo cáo doanh thu, tần suất khám, sử dụng thuốc qua bảng và biểu đồ (sử dụng Chart.js).  
- ⚙️ **Quản lý quy định và dữ liệu**: Thay đổi quy định (phí khám, số bệnh nhân tối đa), quản lý user, thuốc, và khung giờ khám.  

---

## 🏗️ Kiến trúc hệ thống

- **Frontend**:  
  - HTML/CSS/JavaScript  
  - Chart.js (cho biểu đồ thống kê)  

- **Backend**:  
  - Python với Flask (xử lý API, form, email qua Flask-Mail)  

- **Cơ sở dữ liệu**:  
  - MySQL (với các bảng như account, patient, examination_form, receipt, medicine, v.v.)  

---
