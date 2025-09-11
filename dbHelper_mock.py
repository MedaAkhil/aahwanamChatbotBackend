# dbHelper_mock.py

def print_joined_service_categories(connection=None):
    """Mock: Returns top services with categories"""
    columns = ["service_name", "service_description", "category_names", "category_descriptions"]
    data = [
        ("Bartender", "Bartender service provided by expert vendors.", None, None),
        ("Chef", "Chef service provided by expert vendors.",
         "Appetizers, Beverages, Cake, Chinese",
         "Appetizers category for food services, Beverages category for food services, Cake category for food services, Chinese category for food services"),
        ("Decoration", "Decoration service provided by expert vendors.", None, None),
        ("Photography", "Photography service provided by expert vendors.", None, None),
    ]

    output = ["\n🔍 Service and Categories:", "=" * 50]
    output.append(" | ".join(columns))
    output.append("-" * 50)
    for row in data:
        output.append(" | ".join(str(item) if item is not None else "NULL" for item in row))
    return "\n".join(output)


def getServicePackages(conn=None):
    """Mock: Returns available packages"""
    columns = ["package_name", "base_price", "description"]
    data = [
        ("Silver", "8000", "Basic décor + Photography"),
        ("Gold", "15000", "Décor + Photography + Catering"),
        ("Platinum", "25000", "Full package: Décor + Photography + Catering + Music"),
    ]

    output = ["\n📦 Service Packages:", "=" * 50]
    output.append(" | ".join(columns))
    output.append("-" * 50)
    for row in data:
        output.append(" | ".join(str(item) if item is not None else "NULL" for item in row))
    return "\n".join(output)


def getservicesbylocation(conn=None, cityorstatename="Mumbai"):
    """Mock: Returns services by location"""
    columns = ["city", "state", "listofservice", "description"]
    data = [
        (cityorstatename, "Telangana",
         "Décor, Photography, Catering, Music",
         "Décor service, Photography service, Catering service, Music/DJ service")
    ]

    output = [f"\n📍 Services in '{cityorstatename}':", "=" * 50]
    output.append(" | ".join(columns))
    output.append("-" * 50)
    for row in data:
        output.append(" | ".join(str(item) if item is not None else "NULL" for item in row))
    return "\n".join(output)
