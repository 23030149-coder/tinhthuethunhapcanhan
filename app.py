
import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="App Tính Thuế TNCN Việt Nam 2026",
    page_icon="💰",
    layout="centered"
)

# =========================
# LOGO
# =========================
try:
    st.image("logo.jpg.jpg", width=200)
except:
    st.warning("Không tìm thấy file logo.jpg.jpg")

# =========================
# THÔNG TIN
# =========================
st.markdown("### 📝 Đặng Gia Hân")

st.title("💰 Ứng Dụng Tính Thuế Thu Nhập Cá Nhân")
st.write("Cập nhật đầy đủ Lương, Thưởng, Tăng ca, Phụ cấp theo luật thuế mới nhất năm 2026")

st.markdown("---")

# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📋 Nhập thông tin thu nhập tháng này")

gross_salary = st.number_input(
    "1. Lương đóng BHXH (VND)",
    min_value=0,
    value=30000000,
    step=500000
)

gross_bonus_pay = st.number_input(
    "2. Tiền thưởng / Bonus (VND)",
    min_value=0,
    value=0,
    step=500000
)

overtime_pay = st.number_input(
    "3. Tiền tăng ca / làm thêm giờ (VND)",
    min_value=0,
    value=0,
    step=500000
)

st.markdown("**4. Các khoản phụ cấp**")

col1, col2 = st.columns(2)

with col1:
    lunch_allowance = st.number_input(
        "Phụ cấp ăn trưa (VND)",
        min_value=0,
        value=0,
        step=50000
    )

with col2:
    other_allowance = st.number_input(
        "Phụ cấp điện thoại, xăng xe (VND)",
        min_value=0,
        value=0,
        step=50000
    )

dependents = st.number_input(
    "5. Số người phụ thuộc",
    min_value=0,
    value=1,
    step=1
)

st.markdown("---")


# =========================
# HÀM TÍNH THUẾ
# =========================
def tinh_thue_tncn(
    gross,
    bonus,
    overtime,
    lunch,
    other,
    deps
):
    total_income = gross + bonus + overtime + lunch + other

    # Bảo hiểm
    bhxh = gross * 0.08
    bhyt = gross * 0.015
    bhtn = gross * 0.01

    total_insurance = bhxh + bhyt + bhtn

    # Giảm trừ
    self_reduction = 15500000
    dependent_reduction = deps * 6200000

    total_reduction = (
        self_reduction
        + dependent_reduction
    )

    # Miễn thuế
    exempt_lunch = min(lunch, 730000)
    exempt_allowance = other

    total_exempt_income = (
        overtime
        + exempt_lunch
        + exempt_allowance
    )

    assessable_income = max(
        0,
        total_income
        - total_exempt_income
        - total_insurance
        - total_reduction
    )

    tax = 0

    brackets = [
        (10000000, 0.05, "Bậc 1 (5%)"),
        (30000000, 0.10, "Bậc 2 (10%)"),
        (60000000, 0.20, "Bậc 3 (20%)"),
        (100000000, 0.30, "Bậc 4 (30%)"),
        (float("inf"), 0.35, "Bậc 5 (35%)")
    ]

    temp_income = assessable_income
    previous_limit = 0

    tax_breakdown = []

    for limit, rate, desc in brackets:

        if temp_income <= 0:
            break

        range_size = limit - previous_limit

        taxable_amount = min(
            temp_income,
            range_size
        )

        tax_amount = taxable_amount * rate

        tax += tax_amount

        tax_breakdown.append(
            {
                "Bậc thuế": desc,
                "Thu nhập tính thuế": f"{taxable_amount:,.0f} VND",
                "Thuế phải nộp": f"{tax_amount:,.0f} VND"
            }
        )

        temp_income -= taxable_amount
        previous_limit = limit

    net_salary = (
        total_income
        - total_insurance
        - tax
    )

    return {
        "total_income": total_income,
        "bhxh": bhxh,
        "bhyt": bhyt,
        "bhtn": bhtn,
        "total_insurance": total_insurance,
        "dependent_reduction": dependent_reduction,
        "exempt_lunch": exempt_lunch,
        "exempt_allowance": exempt_allowance,
        "assessable_income": assessable_income,
        "tax": tax,
        "net_salary": net_salary,
        "tax_breakdown": tax_breakdown
    }


# =========================
# NÚT TÍNH THUẾ
# =========================
if st.button("🧮 Tính Thuế & Nhận Kết Quả"):

    res = tinh_thue_tncn(
        gross_salary,
        gross_bonus_pay,
        overtime_pay,
        lunch_allowance,
        other_allowance,
        dependents
    )

    st.subheader("🎯 Kết Quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tổng thu nhập",
            f"{res['total_income']:,.0f} VND"
        )

        st.metric(
            "Tổng bảo hiểm",
            f"{res['total_insurance']:,.0f} VND"
        )

    with col2:
        st.metric(
            "Thuế TNCN",
            f"{res['tax']:,.0f} VND"
        )

        st.metric(
            "Thực nhận",
            f"{res['net_salary']:,.0f} VND"
        )

    st.markdown("---")

    st.subheader("📊 Chi tiết")

    st.write(
        f"Thu nhập tính thuế: {res['assessable_income']:,.0f} VND"
    )

    if res["tax"] > 0:
        st.table(res["tax_breakdown"])
    else:
        st.success(
            "Không phát sinh thuế TNCN."
        )
```
