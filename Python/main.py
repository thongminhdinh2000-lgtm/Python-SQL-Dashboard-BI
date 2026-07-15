import os
import shutil
from config import (
    PROCESSED_FOLDER,
    ERROR_FOLDER
)
from merge_excel import merge_excel
from clean_data import clean_all_reports
from load_sql import load_all_reports

def move_files(file_list, destination):
    os.makedirs(destination, exist_ok=True)
    for file in file_list:
        try:
            shutil.move(
                file,
                os.path.join(
                    destination,
                    os.path.basename(file)
                )
            )
            print(f"Đã chuyển: {os.path.basename(file)}")

        except Exception as e:
            print(f"Không thể chuyển {file}")
            print(e)
def main():

    print("=" * 70)
    print("BƯỚC 1: ĐỌC VÀ GỘP FILE EXCEL")
    print("=" * 70)

    merged_data = merge_excel()

    if len(merged_data) == 0:
        print("Không có dữ liệu để xử lý.")
        return

    print()
    print("=" * 70)
    print("BƯỚC 2: LÀM SẠCH DỮ LIỆU")
    print("=" * 70)

    clean_reports = clean_all_reports(merged_data)

    print()
    print("=" * 70)
    print("BƯỚC 3: IMPORT SQL SERVER")
    print("=" * 70)

    success_files, error_files = load_all_reports(clean_reports)

    print()
    print("=" * 70)
    print("BƯỚC 4: CHUYỂN FILE")
    print("=" * 70)

    if success_files:
        print("Chuyển sang Processed...")
        move_files(
            success_files,
            PROCESSED_FOLDER
        )
    if error_files:
        print("Chuyển sang Error...")
        move_files(
            error_files,
            ERROR_FOLDER
        )
    print()
    print("=" * 70)
    print("HOÀN THÀNH")
    print("=" * 70)

    print(f"Thành công : {len(success_files)} file")
    print(f"Lỗi        : {len(error_files)} file")


if __name__ == "__main__":
    main()
