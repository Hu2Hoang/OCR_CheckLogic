# validate.py
import json
import re
from datetime import datetime

from extract_idcard import extract_info


json_data_path = './json/json_sample.json'

def check_id_pp_regex(id_pp):
    # Định nghĩa regex theo quy tắc đã nêu
    regex = re.compile(r'^[A-Z]\d{7}$')
    
    if regex.match(id_pp):
        return 220, f'Regex Passport Number Correct'  # Status code for valid ID format
    else:
        return 221, f'Regex Passport Number Incorrect'  # Status code for invalid ID format
    
def extract_ocr_data(json_data_path):
    with open(json_data_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    ocr_data = {
        'id_pp': data['data'][0]['passport_number'],
        'id_ocr': data['data'][0]['id_number'],
        'doe_ocr': data['data'][0]['doe'],
        'doi_ocr': data['data'][0]['doi'],
        'dob_ocr': data['data'][0]['dob'],
        'sex_ocr': data['data'][0]['sex'],
        'home_ocr': data['data'][0]['pob']
    }
    
    return ocr_data

ocr_data = extract_ocr_data(json_data_path)

def doubleCheck_idCrad_infor(ocr_data):
    
    id_pp = ocr_data['id_pp']
    id_ocr = ocr_data['id_ocr']
    doe_ocr = ocr_data['doe_ocr']
    doi_ocr = ocr_data['doi_ocr']
    dob_ocr = ocr_data['dob_ocr']
    sex_ocr = ocr_data['sex_ocr']
    home_ocr = ocr_data['home_ocr']

    
    yob_ocr = int(dob_ocr.split('/')[-1])

    check_id_pp = check_id_pp_regex(id_pp)
    if check_id_pp[0] != 220:
        return check_id_pp[0], check_id_pp[1]

    idCard_extract = extract_info(id_ocr)

    #Kiểm tra ngày hợp lê:  CCCD hết hạn, Chưa đủ 18 tuổi, Ngày hết hạn không hợp lệ,....
    dates_to_validate = [
        (dob_ocr, 412, "DOB không hợp lệ"),
        (doe_ocr, 413, "DOE không hợp lệ"),
        (doi_ocr, 414, "DOI không hợp lệ")
    ]

    result = validate_dates(dates_to_validate)
    if result:
        return result

    check_datetime = check_vali_datetime(yob_ocr,doi_ocr,doe_ocr)
    if check_datetime[0] != 400:
        return check_datetime[0], check_datetime[1]

    extract_code_status = idCard_extract[0]
    if extract_code_status==200:
        extract_code_status, province, gender, yob = idCard_extract
        province = province.upper()
        if gender == sex_ocr and yob == yob_ocr and home_ocr == province:
            return 300, f"Passport: {id_ocr} Thông tin trích xuất từ Passport trùng với OCR"
        else:
            return 310, f"Passport: {id_ocr} Thông tin trích xuất từ Passport không trùng với OCR (Giới tính, Năm Sinh)"
    else:
        return extract_code_status, f"Passport: {id_ocr} is invalid"

current_year = int(datetime.now().year)

def is_valid_date(date_string):
    try:
        # Định dạng ngày tháng năm là dd/mm/yyyy
        datetime.strptime(date_string, "%d/%m/%Y")
        return 410, f"Ngày hợp lệ"
    except ValueError:
        return 411, f"Ngày không hợp lệ"

def validate_dates(dates):
    for date, error_code, error_message in dates:
        check = is_valid_date(date)
        if check[0] != 410:
            return error_code, error_message
    return None

def check_vali_datetime(yob, doi, doe):

    yoi_ocr = int(doi.split('/')[-1])
    yoe_ocr = int(doe.split('/')[-1])

    if(yob > current_year or yoi_ocr > current_year):
       return 401, f"Year of birth or Issue date is invalid"
    else:
        if( yoe_ocr < current_year ):
            return 402, f"Date of expiry is invalid"
        else:
            if(current_year - yob <18):
                return 403, f"Chưa đủ 18 tuổi"
            else:
                date_format = "%d/%m/%Y"

                doi_date = datetime.strptime(doi, date_format)
                doe_date = datetime.strptime(doe, date_format)
                
                # Calculate the expected DOE (10 years after DOI)
                expected_doe_date = doi_date.replace(year=doi_date.year + 10)
                
                if doe_date == expected_doe_date:
                    return 400, "Date valid"
                else:
                    return 405, "Ngày hết hạn không hợp lệ."

test, message = doubleCheck_idCrad_infor(ocr_data)
if test:
    print(test, message)
else:
    print(message)




