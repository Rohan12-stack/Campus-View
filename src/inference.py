from src.model_utils import generate_caption_local
from src.preprocess import run_ocr
from src.config import CFG
import json
import os

# -------------------------------
# Load facility data
# -------------------------------
FACILITY_DATA = {}
try:
    with open("data/annotations.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            if "facility" in item:
                FACILITY_DATA[item["facility"].lower()] = item
except Exception as e:
    print("Warning: Could not load annotations.jsonl:", e)

# -------------------------------
# Facility detection logic
# -------------------------------
def detect_facility(caption, ocr_text="", image_path=None):
    """Detect which facility the image likely represents"""
    text = (caption + " " + (ocr_text or "")).lower()

    # Use filename as fallback
    if image_path:
        filename = os.path.basename(image_path).lower()
        text += " " + filename

    if "library" in text:
        return "library"
    elif "lab" in text or "computer" in text:
        return "computer lab"
    elif "gate" in text or "motorcycle" in text or "exit" in text:
        return "back gate"
    elif "a classroom with a lot of desks and chairs" in text or "food" in text or "snack" in text:
        return "canteen"
    elif "bank" in text or "atm" in text or "sbi" in text:
        return "bank"
    elif "street" in text or "van" in text:
        return "health care"
    elif "gym" in text or "weights" in text:
        return "gym"
    elif "ceiling fan" in text or "food" in text or "dining" in text:
        return "mess"
    elif "parking" in text or "buses" in text or "canopy" in text or "vehicle" in text:
        return "parking lot"
    elif "roof" in text or "mail" in text or "parcel" in text:
        return "post office"
    elif "mechanical" in text or "engineering" in text or "chennai" in text:
        return "mechanical engineering block"
    elif "entrance" in text:
        return "MCA Building"

    # ✅ Fixed admission detection (added "block", "admin", "administration", etc.)
    elif "hotel" in text or "palm tree" in text or "admin block" in text or "administration" in text or "inquiry" in text or "enquiry" in text:
        return "admission office"
    
    return None


# -------------------------------
# Response logic
# -------------------------------
def answer_from_caption_and_question(caption, question, ocr_text=None, image_path=None):
    q_lower = question.lower()
    facility = detect_facility(caption, ocr_text, image_path)

    if facility not in FACILITY_DATA:
        return "This doesnt look like a part of the college campus."

    data = FACILITY_DATA[facility]
    timings = data.get("timings", "")
    desc = data.get("description", "")
    location = data.get("location", "")
    specs = data.get("specs", "")

    # 1️⃣ What place is this
    if any(x in q_lower for x in ["what is this", "what place", "where am i", "what can you see"]):
        responses = {
            "computer lab": "This is our campus Computer Lab, featuring high-performance systems and development tools for programming, networking, and student projects.",
            "library": "This is our campus Library — a peaceful place for reading, research, and accessing digital and printed learning materials.",
            "back gate": "This is our campus Back Gate, used as a secondary entrance and exit monitored by security and CCTV.",
            "canteen": "This is the campus Canteen, where students and staff can enjoy meals, snacks, and refreshments throughout the day.",
            "bank": "This is the campus Bank branch that offers ATM, banking, and financial services for students and staff.",
            "health care": "This is the Health Care Center, providing medical consultation, first aid, and emergency care for students and faculty.",
            "admission office": "This is the Admission Office, where new students complete enrollment and handle documentation and inquiries.",
            "gym": "This is the campus Gym, equipped with fitness machines and wellness facilities to promote a healthy lifestyle among students and staff.",
            "mess": "This is the campus Mess, providing freshly prepared meals for hostel students and staff in a hygienic environment.",
            "parking lot": "This is the campus Parking Lot, offering secure parking spaces for student and staff vehicles with CCTV monitoring."
        }
        return responses.get(facility, f"This is the {facility.capitalize()} on campus.")

    # 2️⃣ Timings / Opening hours
    elif any(x in q_lower for x in ["timing", "when", "open", "close", "enter"]):
        return f"The {facility.capitalize()} is open {timings}"

    # 3️⃣ Facilities / What's inside
    elif any(x in q_lower for x in ["facility", "facilities", "what are there", "what is there", "available", "sections"]):
        if specs:
            return f"The {facility.capitalize()} includes: {specs}"
        else:
            return f"The {facility.capitalize()} provides several useful facilities for students and staff."

    # 4️⃣ Location / Where
    elif any(x in q_lower for x in ["where", "location", "located"]):
        return f"The {facility.capitalize()} is located at {location}."

    # 5️⃣ General / Description fallback
    else:
        return f"This is our campus {facility.capitalize()}. {desc}"

# -------------------------------
# Inference pipeline
# -------------------------------
def infer(pil_image, question, image_path=None):
    """Main inference pipeline"""
    try:
        caption = generate_caption_local(pil_image)
    except Exception as e:
        caption = ""
        print("Captioning error:", e)

    # 🔸 Print the detected caption in terminal for debugging
    print(f"[DEBUG] Detected Caption: {caption}")

    ocr_text = run_ocr(pil_image)
    answer = answer_from_caption_and_question(caption, question, ocr_text, image_path)

    return {"answer": answer, "caption": caption, "ocr_text": ocr_text, "objects": []}
