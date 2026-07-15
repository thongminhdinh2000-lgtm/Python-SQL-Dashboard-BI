import os
import pandas as pd
import smtplib
from email.message import EmailMessage
from datetime import datetime

# =============================
# THÔNG TIN EMAIL
# =============================
EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"

# =============================
# ĐỌC DANH SÁCH EMAIL
# =============================
df = pd.read_excel(r"D:\BaoCao\DanhSachEmail.xlsx")

bcc_receivers = df["Email"].dropna().tolist()

# =============================
# THƯ MỤC PDF
# =============================
FOLDER = r"D:\BaoCao"

today = datetime.now().date()

pdf_files = []

for file in os.listdir(FOLDER):

    if file.lower().endswith(".pdf"):

        path = os.path.join(FOLDER, file)

        file_date = datetime.fromtimestamp(
            os.path.getmtime(path)
        ).date()

        if file_date == today:
            pdf_files.append(path)

if len(pdf_files) == 0:
    print("Không có báo cáo hôm nay.")
    exit()

# =============================
# TẠO EMAIL
# =============================
msg = EmailMessage()

msg["Subject"] = f"Báo cáo ngày {today:%d/%m/%Y}"

msg["From"] = EMAIL

msg["To"] = EMAIL

msg["Bcc"] = ", ".join(bcc_receivers)

msg.set_content(f"""
Kính gửi Anh/Chị,

Đính kèm là báo cáo ngày {today:%d/%m/%Y}.

Trân trọng.
""")

# =============================
# ĐÍNH KÈM PDF
# =============================
for file in pdf_files:

    with open(file, "rb") as f:

        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(file)
        )

# =============================
# GỬI MAIL
# =============================
with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:

    smtp.login(EMAIL, APP_PASSWORD)

    smtp.send_message(msg)

print(f"Đã gửi {len(pdf_files)} file PDF cho {len(bcc_receivers)} người.")
