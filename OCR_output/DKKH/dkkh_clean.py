import re
import json

# Kết quả OCR từ Google Cloud Vision
ocr_text = """
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
So: 122
F12
GIẤY CHỨNG NHẬN KẾT HÔN
Họ, chữ đệm, tên vợ:
PHÙNG I
Ngày, tháng, năm sinh: 20/01/1993
Dân tộc: Kinh
wwwwww
Quốc tịch: Việt Nam
Nơi cư trú: Thôn 08 xã Ea Đar, huyện Ea
Kar, tỉnh Đắk Lắk
Họ, chữ đệm, tên chồng:
NGUYỄN
Ngày, tháng, năm sinh: 30/10/1988
Dân tộc: Kinh
Quốc tịch: Việt Nam
Nơi cư trú: Phường Đông Hòa,thị xã Dĩ An.
tỉnh Bình Dương
Giấy tờ tùy thân: Giấy CCCD số Giấy tờ tùy thân: Giấy CMND số
---, Công an tỉnh Đắk Lắk cấp ngày
11/3/2011
Công an tỉnh Bình Dương cấp
ngày 14/3/2018
Nơi đăng ký kết hôn: Uỷ ban nhân dân Xã Ea Đar, huyện Ea Kar, tỉnh Đắk
Lắk
Ngày, tháng, năm đăng ký: 05/12/2018
Vợ
(Ký, ghi rõ họ, chữ đệm, tên)
зы
Chồng
(Ký, ghi rõ họ, chữ đệm, tên)
NGƯỜI KÝ GIẤY CHỨNG NHẬN KẾT HÔN
(Ký, ghi rõ họ, chữ đệm, tên, chức vụ, đóng dấu)
PHÓ CHỦ TỊCH
Y Na Mlo
PS D:\Code\OCR>


(Ký, ghi rõ họ, chữ đệm, tên)
зы
Chồng
(Ký, ghi rõ họ, chữ đệm, tên)
NGƯỜI KÝ GIẤY CHỨNG NHẬN KẾT HÔN
(Ký, ghi rõ họ, chữ đệm, tên, chức vụ, đóng dấu)
PHÓ CHỦ TỊCH
Y Na Mlo
"""

# Hàm loại bỏ các phần văn bản lặp hoặc không cần thiết
def clean_text(text):
    # Loại bỏ các dòng thừa, các đoạn lặp lại, v.v.
    text = re.sub(r'(Chồng \(Ký, ghi rõ họ, chữ đệm, tên\))', '', text)
    text = re.sub(r'(Vợ \(Ký, ghi rõ họ, chữ đệm, tên\))', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Hàm trích xuất thông tin từ văn bản
def extract_info(text):
    # Các thông tin khác (vợ, chồng, nơi cư trú, vv.)
    wife_name = re.search(r"Họ, chữ đệm, tên vợ:\s*(\w+)", text)
    wife_name = wife_name.group(1).strip() if wife_name else "Không rõ"

    husband_name = re.search(r"Họ, chữ đệm, tên chồng:\s*(\w+)", text)
    husband_name = husband_name.group(1).strip() if husband_name else "Không rõ"

    wife_dob = re.search(r"Ngày, tháng, năm sinh:\s*(\d{2}/\d{2}/\d{4})", text)
    wife_dob = wife_dob.group(1).strip() if wife_dob else "Không rõ"

    husband_dob = re.search(r"Ngày, tháng, năm sinh:\s*(\d{2}/\d{2}/\d{4})", text)
    husband_dob = husband_dob.group(1).strip() if husband_dob else "Không rõ"

    wife_residence = re.search(r"Nơi cư trú:\s*(.*?)Họ, chữ đệm, tên chồng:", text)
    wife_residence = wife_residence.group(1).strip() if wife_residence else "Không rõ"

    husband_residence = re.search(r"Nơi cư trú:\s*(.*)", text.split("Nơi cư trú:")[2])
    husband_residence = husband_residence.group(1).strip() if husband_residence else "Không rõ"

    # Trích xuất loại giấy tờ tùy thân của vợ
    wife_identity_card = re.search(r"Giấy tờ tùy thân:\s*(\w+\s*\w*) số\s*(\w+).*cấp ngày\s*(\d{1,2}/\d{1,2}/\d{4})", text)
    wife_identity_card_type = wife_identity_card.group(1).strip() if wife_identity_card else "Không rõ"
    wife_identity_card_number = wife_identity_card.group(2).strip() if wife_identity_card else "Không rõ"
    wife_identity_card_issued_date = wife_identity_card.group(3).strip() if wife_identity_card else "Không rõ"
    wife_identity_card_issued_place = "Công an tỉnh Đắk Lắk cấp"  # Có thể cần thay đổi nếu trích xuất thêm

    # Trích xuất loại giấy tờ tùy thân của chồng
    husband_identity_card = re.search(r"Giấy tờ tùy thân:\s*(\w+\s*\w*) số\s*(\w+).*cấp ngày\s*(\d{1,2}/\d{1,2}/\d{4})", text)
    husband_identity_card_type = husband_identity_card.group(1).strip() if husband_identity_card else "Không rõ"
    husband_identity_card_number = husband_identity_card.group(2).strip() if husband_identity_card else "Không rõ"
    husband_identity_card_issued_date = husband_identity_card.group(3).strip() if husband_identity_card else "Không rõ"
    husband_identity_card_issued_place = "Công an tỉnh Bình Dương cấp"  # Có thể cần thay đổi nếu trích xuất thêm

    # Các thông tin khác
    registration_place = re.search(r"Nơi đăng ký kết hôn:\s*(.*?)Ngày, tháng, năm đăng ký:", text)
    registration_place = registration_place.group(1).strip() if registration_place else "Không rõ"

    registration_date = re.search(r"Ngày, tháng, năm đăng ký:\s*(\d{2}/\d{2}/\d{4})", text)
    registration_date = registration_date.group(1).strip() if registration_date else "Không rõ"

    signing_officer = re.search(r"PHÓ CHỦ TỊCH\s*(.*)", text)
    signing_officer_name = signing_officer.group(1).strip() if signing_officer else "Không rõ"

    # Kết quả JSON
    return {
        "document_type": "Giấy chứng nhận kết hôn",
        "wife": {
            "full_name": wife_name,
            "date_of_birth": wife_dob,
            "ethnicity": "Kinh",
            "nationality": "Việt Nam",
            "place_of_residence": wife_residence,
            "identity_card": {
                "type": wife_identity_card_type,
                "number": wife_identity_card_number,
                "issued_date": wife_identity_card_issued_date,
                "issued_place": wife_identity_card_issued_place
            }
        },
        "husband": {
            "full_name": husband_name,
            "date_of_birth": husband_dob,
            "ethnicity": "Kinh",
            "nationality": "Việt Nam",
            "place_of_residence": husband_residence,
            "identity_card": {
                "type": husband_identity_card_type,
                "number": husband_identity_card_number,
                "issued_date": husband_identity_card_issued_date,
                "issued_place": husband_identity_card_issued_place
            }
        },
        "marriage_registration_place": registration_place,
        "marriage_registration_date": registration_date,
        "signing_officer": {
            "position": "Phó Chủ Tịch",
            "name": signing_officer_name
        }
    }

# Tiền xử lý văn bản
cleaned_text = clean_text(ocr_text)

# Trích xuất thông tin
extracted_info = extract_info(cleaned_text)

# Tạo JSON
json_result = json.dumps(extracted_info, ensure_ascii=False, indent=4)
print("Kết quả JSON:\n", json_result)
