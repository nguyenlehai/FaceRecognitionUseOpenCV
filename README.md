# Face Recognition use OpenCV
### Overview:
Tự động xác nhận những khách hàng đã đến cửa hàng dựa trên sự huấn luyên dữ 
liệu hình ảnh đã có sẵn(training) dựa trên thư viện OpenCV và hệ thống có thể 
tìm kiếm thông tin, dữ liệu khách hàng. 
Từ đó cửa hàng sẽ phân công các nhân viên liên quan đến để hỗ trợ 
khách hàng một cách nhanh chóng và chính xác.  
Hệ thống có thể hoạt động với số lượng lớn khách hàng từ 10 người 
trở lên đến cùng lúc, độ chính xác tương đối cao và an toàn.

### Usage:
1.Cai dat moi truong
 - Cai dat  Microsoft SQL SERVER 2012
 - Cai dat Python 3.6.4
 - Cai dat Pycharm Community(De code va run chuong trinh)
 - Cai dat cac thu vien python lien quan: OpenCV, PIL, numpy, PyQt5, pyodbc, pandas...
 - Restore Database (File backup de trong .\M2\database)

-------------------------------------------------------------------------------------
2.Xoa het du lieu chuong trinh de thuc hien lai
- Buoc 1: Stop chuong trinh

- Buoc 2: Xoa du lieu cac bang trong Database
	- DELETE FROM dbo.INVOICE_DETAIL
	- DELETE FROM dbo.INVOICE_HEADER
	- DELETE FROM dbo.ITEM 
	- DELETE FROM dbo.CUSTOMER
	- DELETE FROM dbo.EMPLOYEE

- Buoc 3: Xoa het du lieu trong cac folder sau:
	- .\M2\dataset
	- .\M2\image
	- .\M2\trainer
