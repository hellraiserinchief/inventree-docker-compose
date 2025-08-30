import os, time, json
import requests
from urllib.parse import urljoin

INVENTREE_URL = os.environ.get("INVENTREE_URL").rstrip("/") + "/"
TOKEN = os.environ.get("INVENTREE_TOKEN")
LAB_NAME = os.environ.get("LAB_NAME", "Makerspace")

if not TOKEN or not INVENTREE_URL:
    raise SystemExit("Set INVENTREE_URL and INVENTREE_TOKEN in .env.seed")

S = requests.Session()
S.headers.update({"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"})

def wait_until_ready():
    for _ in range(60):
        try:
            r = S.get(urljoin(INVENTREE_URL, "api/"))
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(2)
    raise SystemExit("InvenTree API did not become ready in time.")

def post(endpoint, payload):
    url = urljoin(INVENTREE_URL, endpoint)
    r = S.post(url, data=json.dumps(payload))
    if r.status_code not in (200, 201):
        raise SystemExit(f"POST {endpoint} failed: {r.status_code} {r.text}")
    return r.json()

wait_until_ready()

# Locations
locations = [
    {"name": f"{LAB_NAME} - Workshop", "description": "Main workshop area", "items": [
        {"name": "Shelf A - Power Tools"},
        {"name": "Shelf B - Mechanical Hardware"},
        {"name": "Tool Cabinet - Hand Tools"},
        {"name": "Drawer Unit - Bearings & Bushings"},
    ]},
    {"name": f"{LAB_NAME} - Electronics Lab", "description": "ESD benches & electronics work", "items": [
        {"name": "Bench 1 - Soldering Station"},
        {"name": "Bench 2 - Assembly Area"},
        {"name": "Component Wall - Passives"},
        {"name": "Component Wall - Actives"},
        {"name": "Testing Station"},
    ]},
    {"name": f"{LAB_NAME} - Server Room", "description": "Racks and network gear", "items": [
        {"name": "Rack 1"},
        {"name": "Rack 2"},
        {"name": "Spare Parts Bin"},
        {"name": "Cable Wall"},
    ]},
]

for loc in locations:
    parent = post("api/stock/location/", {"name": loc["name"], "description": loc.get("description", "")})
    for child in loc.get("items", []):
        post("api/stock/location/", {"name": child["name"], "description": child.get("description", ""), "parent": parent["pk"]})

# Categories
cats = [
    {"name": "3D Printing", "items": [
        {"name": "Printers"},
        {"name": "Filaments", "items": [
            {"name": "PLA"},
            {"name": "ABS"},
            {"name": "PETG"},
            {"name": "Flexible TPU"},
            {"name": "Specialty (Woodfill, Metalfill)"},
        ]},
        {"name": "Nozzles & Hotends"},
        {"name": "Belts & Pulleys"},
        {"name": "Boards & Drivers"},
        {"name": "Build Plates & Surfaces"},
        {"name": "Extruders & Feeders"},
        {"name": "Enclosures & Mods"},
    ]},
    {"name": "CNC", "items": [
        {"name": "Machines"},
        {"name": "Endmills", "items": [
            {"name": "Flat End"},
            {"name": "Ball Nose"},
            {"name": "V-Bits"},
        ]},
        {"name": "Workholding & Fixtures"},
        {"name": "Spindles & VFD"},
        {"name": "Linear Rails & Bearings"},
        {"name": "Stepper Motors & Drivers"},
        {"name": "Coolant & Lubrication"},
    ]},
    {"name": "Electronics", "items": [
        {"name": "Computing Platforms", "items": [
            {"name": "Single Board Computers", "items": [
                {"name": "Raspberry Pi Family"},
                {"name": "Arduino Family"},
                {"name": "Teensy"},
                {"name": "BeagleBone"},
                {"name": "NVIDIA Jetson"},
            ]},
            {"name": "FPGAs"},
            {"name": "Microcontrollers (General Purpose)"},
        ]},
        {"name": "Active Components", "items": [
            {"name": "Integrated Circuits"},
            {"name": "Transistors"},
            {"name": "Voltage Regulators"},
            {"name": "Power ICs"},
        ]},
        {"name": "Passive Components", "items": [
            {"name": "Resistors"},
            {"name": "Capacitors"},
            {"name": "Inductors"},
            {"name": "Crystals & Oscillators"},
            {"name": "Ferrites"},
        ]},
        {"name": "Connectors", "items": [
            {"name": "Headers & Sockets"},
            {"name": "Terminal Blocks"},
            {"name": "RF Connectors"},
            {"name": "USB & HDMI"},
            {"name": "Power Connectors"},
        ]},
        {"name": "Cables & Harnesses", "items": [
            {"name": "Ribbon Cables"},
            {"name": "Shielded Cables"},
            {"name": "Custom Harnesses"},
        ]},
        {"name": "Power", "items": [
            {"name": "Power Supplies"},
            {"name": "Batteries", "items": [
                {"name": "Li-ion"},
                {"name": "LiPo"},
                {"name": "NiMH"},
                {"name": "Lead Acid"},
            ]},
            {"name": "Battery Management"},
        ]},
        {"name": "Motors & Motion", "items": [
            {"name": "Stepper Motors"},
            {"name": "DC Motors"},
            {"name": "Servo Motors"},
            {"name": "Motor Drivers"},
            {"name": "Linear Actuators"},
        ]},
        {"name": "Sensors", "items": [
            {"name": "Temperature"},
            {"name": "Pressure"},
            {"name": "Proximity"},
            {"name": "IMU & Accelerometers"},
            {"name": "Light & Color"},
            {"name": "Gas"},
        ]},
        {"name": "Electronics Tools", "items": [
            {"name": "Soldering Equipment"},
            {"name": "Crimpers"},
            {"name": "Wire Strippers"},
            {"name": "Multimeters"},
            {"name": "Oscilloscopes"},
            {"name": "Logic Analyzers"},
            {"name": "Hot Air Rework"},
        ]},
    ]},
    {"name": "Mechanical", "items": [
        {"name": "Fasteners", "items": [
            {"name": "Bolts", "items": [
                {"name": "M2.5"},
                {"name": "M3"},
                {"name": "M4"},
                {"name": "M5"},
                {"name": "M6"},
                {"name": "M8"},
            ]},
            {"name": "Nuts", "items": [
                {"name": "M2.5"},
                {"name": "M3"},
                {"name": "M4"},
                {"name": "M5"},
                {"name": "M6"},
                {"name": "M8"},
            ]},
            {"name": "Washers"},
        ]},
        {"name": "Bearings", "items": [
            {"name": "Ball Bearings"},
            {"name": "Linear Bearings"},
            {"name": "Thrust Bearings"},
        ]},
        {"name": "Springs", "items": [
            {"name": "Compression"},
            {"name": "Tension"},
            {"name": "Torsion"},
        ]},
        {"name": "Bushings"},
        {"name": "Gears & Pulleys", "items": [
            {"name": "Spur Gears"},
            {"name": "Timing Pulleys"},
        ]},
        {"name": "Structural", "items": [
            {"name": "Aluminium Profiles"},
            {"name": "Brackets"},
        ]},
    ]},
    {"name": "Servers & Networking", "items": [
        {"name": "Servers"},
        {"name": "CPUs & RAM"},
        {"name": "Storage (HDD/SSD)"},
        {"name": "NICs & HBAs"},
        {"name": "Switches & Routers"},
        {"name": "Cables & Patch Panels"},
    ]},
    {"name": "Tools & Lab", "items": [
        {"name": "Hand Tools"},
        {"name": "Measurement & Test"},
        {"name": "Consumables", "items": [
            {"name": "Zip Ties"},
            {"name": "Heat Shrink"},
            {"name": "Tape"},
        ]},
        {"name": "Safety & ESD"},
    ]},
]

def create_category_tree(parent_id, children):
    for child in children:
        payload = {"name": child["name"]}
        if parent_id:
            payload["parent"] = parent_id
        node = post("api/part/category/", payload)
        if "items" in child:
            create_category_tree(node["pk"], child["items"])

for cat in cats:
    parent = post("api/part/category/", {"name": cat["name"]})
    if "items" in cat:
        create_category_tree(parent["pk"], cat["items"])

print("Creative deep seed complete.")
