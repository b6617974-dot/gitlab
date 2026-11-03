from typing import Any, Dict


def analyze_dc(voltage_v: float, resistance_ohm: float) -> Dict[str, Any]:
    """คำนวณและวิเคราะห์พารามิเตอร์ทางไฟฟ้ากระแสตรง (DC) สำหรับวงจรตัวต้านทาน

    Parameters:
        voltage_v (float): แรงดันตกคร่อมตัวต้านทาน (โวลต์, V)
        resistance_ohm (float): ค่าความต้านทาน (โอห์ม, Ω)

    Returns:
        dict: ผลการคำนวณกระแส, กำลังไฟฟ้า, พิกัดตัวต้านทานที่แนะนำ
    """
    # ตรวจสอบชนิดข้อมูล
    if not isinstance(voltage_v, (int, float)) or not isinstance(
        resistance_ohm, (int, float)
    ):
        raise TypeError("แรงดันและความต้านทานต้องเป็นข้อมูลชนิดตัวเลขเท่านั้น")

    # ตรวจสอบค่าทางกายภาพของวงจร
    if resistance_ohm == 0:
        raise ZeroDivisionError(
            "เกิดสภาวะลัดวงจร (Short Circuit): ค่าความต้านทานเป็น 0 Ω กระแสไฟฟ้าพุ่งสูงอนันต์"
        )
    if resistance_ohm < 0:
        raise ValueError(
            "ค่าความต้านทานของอุปกรณ์ Passive ต้องมีค่ามากกว่า 0 Ω"
        )

    # 1. คำนวณกระแสไฟฟ้าตามกฎของโอห์ม: I = V / R
    current_a = voltage_v / resistance_ohm

    # 2. คำนวณกำลังไฟฟ้า: P = V * I (หรือ V^2 / R)
    power_w = (voltage_v**2) / resistance_ohm

    # 3. กำหนดพิกัดตัวต้านทานมาตรฐานพร้อมค่าเผื่อความปลอดภัย (Derating factor 50% หรือ 2 เท่าของโหลด)
    standard_ratings = [0.125, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
    safe_power_requirement = power_w * 2.0

    recommended_wattage = None
    for rating in standard_ratings:
        if rating >= safe_power_requirement:
            recommended_wattage = f"{rating} W"
            break
    if not recommended_wattage:
        recommended_wattage = (
            f"> 10 W (กำลังสูญเสียสูง แนะนำใช้ Power Resistor หรือติด Heatsink)"
        )

    return {
        "voltage_v": round(float(voltage_v), 4),
        "resistance_ohm": round(float(resistance_ohm), 4),
        "current_a": round(current_a, 4),
        "current_ma": round(current_a * 1000, 2),
        "power_w": round(power_w, 4),
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
    # ตัวอย่างที่ 1: การคำนวณและแสดงผลปกติ
    try:
        result = analyze_dc(voltage_v=12.0, resistance_ohm=6.0)
        print_circuit_report(result)
    except (ValueError, TypeError, ZeroDivisionError) as err:
        print(f"[Error]: {err}")

    print()

    # ตัวอย่างที่ 2: วงจรแรงดันต่ำกระแสต่ำ (mA / mW)
    try:
        sensor_resistor = analyze_dc(voltage_v=3.3, resistance_ohm=1000.0)
        print_circuit_report(sensor_resistor)
    except (ValueError, TypeError, ZeroDivisionError) as err:
        print(f"[Error]: {err}")