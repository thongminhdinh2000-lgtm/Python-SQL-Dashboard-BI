import os
import glob
import pandas as pd

from config import (
    INPUT_FOLDER,
    REPORTS
)


def detect_report(header):
    """
    Xác định loại báo cáo dựa vào header
    """

    header = [str(col).strip() for col in header]

    for report_name, report in REPORTS.items():

        required = report["required_columns"]

        if all(col in header for col in required):
            return report_name

    return None


def merge_excel():

    groups = {}

    files = glob.glob(os.path.join(INPUT_FOLDER, "*.xlsx"))

    if len(files) == 0:
        print("Không tìm thấy file Excel.")
        return groups

    print(f"Tìm thấy {len(files)} file.\n")

    for file in files:

        try:

            # Chỉ đọc header
            header = list(
                pd.read_excel(
                    file,
                    nrows=0
                ).columns
            )

            report = detect_report(header)

            if report is None:

                print(f"[BỎ QUA] {os.path.basename(file)}")
                print("Không nhận diện được loại báo cáo.\n")

                continue

            if report not in groups:
                groups[report] = []

            groups[report].append(file)

            print(f"[OK] {os.path.basename(file)}")
            print(f"Loại báo cáo : {report}\n")

        except Exception as e:

            print(f"Lỗi đọc {file}")
            print(e)

    # ===========================
    # Gộp từng nhóm
    # ===========================

    merged_data = {}

    for report, file_list in groups.items():

        print("=" * 60)
        print(f"Gộp báo cáo: {report}")

        dfs = []

        for file in file_list:

            df = pd.read_excel(file)

            df["NguonFile"] = os.path.basename(file)

            dfs.append(df)

            print("   ", os.path.basename(file))

        merged_df = pd.concat(
            dfs,
            ignore_index=True
        )

        merged_data[report] = {

            "data": merged_df,

            "files": file_list

        }

        print(
            f"Tổng số dòng: {len(merged_df)}\n"
        )

    return merged_data
