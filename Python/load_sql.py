import urllib
from sqlalchemy import create_engine

from config import (
    SERVER,
    DATABASE,
    USE_WINDOWS_AUTH,
    USERNAME,
    PASSWORD,
    REPORTS
)


# ==========================================
# Kết nối SQL Server
# ==========================================

def get_engine():

    if USE_WINDOWS_AUTH:

        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            "Trusted_Connection=yes;"
        )

    else:

        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD};"
        )

    params = urllib.parse.quote_plus(connection_string)

    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={params}",
        fast_executemany=True
    )

    return engine


# ==========================================
# Đưa một DataFrame vào SQL
# ==========================================

def load_dataframe(report_name, df):

    table_name = REPORTS[report_name]["table_name"]

    engine = get_engine()

    try:

        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
            chunksize=5000
        )

        print(f"Đã import {len(df)} dòng vào bảng {table_name}")

        return True

    except Exception as e:

        print(f"Lỗi import {table_name}")

        print(e)

        return False


# ==========================================
# Import tất cả báo cáo
# ==========================================

def load_all_reports(clean_reports):

    success_files = []

    error_files = []

    for report_name, info in clean_reports.items():

        print("=" * 60)

        print(f"Đang import {report_name}")

        ok = load_dataframe(
            report_name,
            info["data"]
        )

        if ok:

            success_files.extend(
                info["source_files"]
            )

        else:

            error_files.extend(
                info["source_files"]
            )

    return success_files, error_files
