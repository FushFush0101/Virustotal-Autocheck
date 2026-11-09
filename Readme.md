Hướng dẫn sử dụng Script Autocheck IP với Virus Total

1./ Điền danh sách ip mà mình muốn thêm vào file text "listip.txt"

2./ Thay đổi giá trị API Key của user trên VirusTotal (Hiện đã có sẵn key API trong srouce code nếu muốn sài API của mình thì có thể edit lại phần này)
api_key = 'Your API Key'

3./ Chạy script với path tương ứng:
VD: C:\Users\phudc\Desktop\Script\Virustotal Autocheck>virustotal_autocheck.py

4./ Kiểm tra kết quả trong file Exel virus_total_results.xlsx

Note: Nếu gặp lỗi liên quan đến cấc thư viện như requests, openpyxl thì thực hiện các thao tác cài đặt sau đây.
+ pip install requests
+ pip install openpyxl