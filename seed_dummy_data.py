import argparse
import json
import random
import string
import urllib.error
import urllib.request
from http.cookiejar import CookieJar


BASE_URL = "http://127.0.0.1:8000"

FIRST_NAMES = [
    "Liam", "Noah", "Olivia", "Emma", "Ava", "Sophia", "James", "Mason",
    "Mia", "Ethan", "Isabella", "Lucas", "Amelia", "Harper", "Elijah", "Evelyn",
]
LAST_NAMES = [
    "Carter", "Nguyen", "Patel", "Santos", "Reed", "Bennett", "Murphy", "Ali",
    "Brooks", "Fisher", "Diaz", "Shaw", "Parker", "Morris", "Ward", "Cole",
]
DEPARTMENTS = [
    "Finance", "Operations", "HR", "IT", "Security", "Support", "Sales", "Logistics"
]
LOCATIONS = [
    "HQ", "Branch East", "Branch West", "Warehouse", "Front Desk", "Server Room", "Remote"
]
DEVICE_TYPES = [
    ("Laptop", "Dell", "Latitude"),
    ("Desktop", "HP", "EliteDesk"),
    ("Monitor", "LG", "UltraFine"),
    ("Phone", "Samsung", "Galaxy"),
    ("Tablet", "Apple", "iPad"),
    ("Printer", "Brother", "HL"),
    ("Dock", "Dell", "WD"),
]
ROLES = ["Super Admin", "Admin", "Technician", "Auditor"]
STATUSES = ["Available", "Assigned", "Maintenance"]
CONDITIONS = ["Excellent", "Good", "Fair", "Needs Repair"]


def slug(text):
    return "".join(ch.lower() for ch in text if ch.isalnum())


def api(opener, path, method="GET", payload=None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=headers, method=method)
    try:
        with opener.open(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} failed: {body}") from exc


def login():
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
    api(opener, "/api/login", "POST", {"username": "admin", "password": "admin"})
    return opener


def make_people_payload(index):
    first = FIRST_NAMES[index % len(FIRST_NAMES)]
    last = LAST_NAMES[(index * 3) % len(LAST_NAMES)]
    full_name = f"{first} {last} {index + 1}"
    return {
        "full_name": full_name,
        "department": DEPARTMENTS[index % len(DEPARTMENTS)],
        "email": f"{slug(first)}.{slug(last)}{index + 1}@local",
        "phone": f"555-{1000 + index:04d}",
        "location": LOCATIONS[index % len(LOCATIONS)],
        "notes": f"Dummy user profile {index + 1}",
    }


def make_asset_payload(index):
    category, brand, model_root = DEVICE_TYPES[index % len(DEVICE_TYPES)]
    number = 1000 + index
    return {
        "asset_tag": f"{category[:3].upper()}-{number}",
        "device_name": f"{category} Unit {index + 1}",
        "category": category,
        "brand": brand,
        "model": f"{model_root} {500 + index}",
        "serial_number": f"SN-{brand[:3].upper()}-{number}",
        "status": "Available",
        "condition": CONDITIONS[index % len(CONDITIONS)],
        "purchase_date": f"2025-{(index % 9) + 1:02d}-{(index % 27) + 1:02d}",
        "warranty_end": f"2028-{(index % 9) + 1:02d}-{(index % 27) + 1:02d}",
        "location": LOCATIONS[index % len(LOCATIONS)],
        "notes": f"Dummy asset {index + 1}",
    }


def make_admin_payload(index):
    first = FIRST_NAMES[(index + 5) % len(FIRST_NAMES)]
    last = LAST_NAMES[(index + 7) % len(LAST_NAMES)]
    return {
        "full_name": f"{first} {last} Admin {index + 1}",
        "username": f"admin_user_{index + 1}",
        "password": f"TempPass{index + 1}!",
        "role": ROLES[index % len(ROLES)],
        "is_active": True,
    }


def ensure_people(opener, target):
    people = api(opener, "/api/people")["items"]
    for index in range(len(people), target):
        api(opener, "/api/people", "POST", make_people_payload(index))
    return api(opener, "/api/people")["items"]


def ensure_assets(opener, target):
    assets = api(opener, "/api/assets")["items"]
    for index in range(len(assets), target):
        api(opener, "/api/assets", "POST", make_asset_payload(index))
    return api(opener, "/api/assets")["items"]


def ensure_admins(opener, target):
    admins = api(opener, "/api/admin-users")["items"]
    for index in range(len(admins), target):
        api(opener, "/api/admin-users", "POST", make_admin_payload(index))
    return api(opener, "/api/admin-users")["items"]


def ensure_assignments(opener, target):
    assignments = api(opener, "/api/assignments")["items"]
    if len(assignments) >= target:
        return assignments

    people = api(opener, "/api/people")["items"]
    assets = api(opener, "/api/assets")["items"]

    available_assets = [asset for asset in assets if asset["status"] != "Assigned"]
    person_cycle = 0

    while len(assignments) < target and available_assets and people:
        asset = available_assets.pop(0)
        person = people[person_cycle % len(people)]
        person_cycle += 1
        api(opener, "/api/assignments/assign", "POST", {
            "asset_id": asset["id"],
            "person_id": person["id"],
            "notes": f"Dummy assignment for {asset['asset_tag']}",
        })
        assignments = api(opener, "/api/assignments")["items"]

    return assignments


def main():
    parser = argparse.ArgumentParser(description="Seed dummy data through the running inventory app.")
    parser.add_argument("--target", type=int, default=50, help="Target total records per section")
    args = parser.parse_args()

    opener = login()
    people = ensure_people(opener, args.target)
    assets = ensure_assets(opener, args.target)
    admins = ensure_admins(opener, args.target)
    assignments = ensure_assignments(opener, args.target)

    print(json.dumps({
        "people_total": len(people),
        "assets_total": len(assets),
        "admins_total": len(admins),
        "assignments_total": len(assignments),
    }, indent=2))


if __name__ == "__main__":
    main()
