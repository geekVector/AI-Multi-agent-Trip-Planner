from iata_map import IATA_MAP
import re

def Flight_search(query):
    dep_city, arr_city = "", ""
    query_lower = query.lower()

    # Pattern 1: "from X to Y"
    match = re.search(r'from\s+(.+?)\s+to\s+([a-zA-Z\s]+?)(?:\s+for|\s+on|\s+in|\s+during|\s+\d|$)', query_lower)
    if match:
        dep_city = match.group(1).strip()
        arr_city = match.group(2).strip()
    else:
        # Pattern 2: "to Y from X"
        match2 = re.search(r'to\s+([a-zA-Z\s]+?)\s+from\s+([a-zA-Z\s]+?)(?:\s+for|\s+on|\s+in|\s+\d|$)', query_lower)
        if match2:
            arr_city = match2.group(1).strip()
            dep_city = match2.group(2).strip()
        elif " to " in query_lower:
            # Pattern 3: plain "X to Y"
            parts = query_lower.split(" to ")
            dep_city = parts[0].strip().split()[-1]
            arr_city = parts[1].strip().split()[0]

    dep_iata = IATA_MAP.get(dep_city, dep_city.upper())
    arr_iata = IATA_MAP.get(arr_city, arr_city.upper())

    return f"""
Flight Route: {dep_city.title()} ({dep_iata}) → {arr_city.title()} ({arr_iata})

Common airlines on this route:
- IndiGo (6E): Frequent daily flights on major Indian routes
- Air India (AI): Full service carrier with wide domestic/international network
- SpiceJet (SG): Budget carrier with extensive domestic coverage
- Vistara (UK): Premium economy and business class options
- Emirates (EK): International routes via Dubai hub
- Qatar Airways (QR): International routes via Doha hub
- Lufthansa (LH): International routes via Frankfurt hub
- British Airways (BA): International routes via London hub

Typical flight details:
- Short domestic routes: ~1-2 hrs
- Medium haul (India to Middle East/SE Asia): ~4-6 hrs
- Long haul (India to Europe/USA): ~9-14 hrs
- Baggage: 15-23kg check-in (economy, varies by carrier)
- Connecting hubs: Dubai (DXB), Doha (DOH), Delhi (DEL), Mumbai (BOM)
- Booking: MakeMyTrip, Cleartrip, EaseMyTrip, Yatra, Google Flights

Note: For live prices and exact schedules, check Google Flights or MakeMyTrip.
"""