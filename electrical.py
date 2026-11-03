from typing import Any, Dict


def analyze_dc(voltage_v: float, resistance_ohm: float) -> Dict[str, Any]:
    """คำนวณและวิเคราะห์พารามิเตอร์ทางไฟฟ้ากระแสตรง (DC) สำหรับวงจรตัวต้านทาน"""
    # 1. ตรวจสอบชนิดข้อมูล
    if not isinstance(voltage_v, (int, float)) or not isinstance(
        resistance_ohm, (int, float)
    ):
        raise TypeError("แรงดันและความต้านทานต้องเป็นข้อมูลชนิดตัวเลขเท่านั้น")

    # 2. ตรวจสอบค่าความต้านทาน (ต้องเป็นบวกตามเกณฑ์ของแล็บ)
    if resistance_ohm <= 0:
        raise ValueError("Resistance must be positive")

    # 3. คำนวณค่ากระแสและกำลังไฟฟ้า
    current_a = voltage_v / resistance_ohm
    power_w = (voltage_v**2) / resistance_ohm

    # 4. แนะนำพิกัดตัวต้านทานมาตรฐาน (Derating factor 50%)
    standard_ratings = [0.125, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
    safe_power_requirement = power_w * 2.0

    recommended_wattage = None
    for rating in standard_ratings:
        if rating >= safe_power_requirement:
            recommended_wattage = f"{rating} W"
            break
    if not recommended_wattage:
        recommended_wattage = (
            "> 10 W (กำลังสูญเสียสูง แนะนำใช้ Power Resistor หรือติด Heatsink)"
        )

    return {
        "current_a": current_a,
        "power_w": power_w,
        "voltage_v": round(float(voltage_v), 4),
        "resistance_ohm": round(float(resistance_ohm), 4),
        "current_ma": round(current_a * 1000, 2),
        "power_mw": round(power_w * 1000, 2),
        "recommended_rating": recommended_wattage,
    }


def print_circuit_report(data: Dict[str, Any]) -> None:
    """แสดงผลลัพธ์ในรูปแบบตารางรายงานผลทางวิศวกรรม"""
    print("=" * 45)
    print("      DC CIRCUIT ANALYSIS REPORT")
    print("=" * 45)
    print(f" แรงดันไฟฟ้าตกคร่อม (V)   : {data['voltage_v']} V")
    print(f" ค่าความต้านทาน (R)       : {data['resistance_ohm']} Ω")
    print("-" * 45)
    print(
        f" กระแสไฟฟ้าในวงจร (I)    : {data['current_a']} A  ({data['current_ma']} mA)"
    )
    print(
        f" กำลังไฟฟ้าที่สูญเสีย (P) : {data['power_w']} W  ({data['power_mw']} mW)"
    )
    print(f" พิกัดตัวต้านทานที่แนะนำ : {data['recommended_rating']}")
    print("=" * 45)


if __name__ == "__main__":
    try:
        result = analyze_dc(voltage_v=12.0, resistance_ohm=6.0)
        print_circuit_report(result)
    except (ValueError, TypeError) as err:
        print(f"[Error]: {err}")