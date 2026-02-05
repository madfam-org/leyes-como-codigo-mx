import json
from pathlib import Path


def merge_registries():
    registry_path = Path("data/law_registry.json")
    discovery_path = Path("data/discovered_laws.json")

    if not registry_path.exists() or not discovery_path.exists():
        print("❌ Missing input files")
        return

    with open(registry_path, "r") as f:
        registry = json.load(f)

    with open(discovery_path, "r") as f:
        discovered = json.load(f)

    existing_ids = {law["id"] for law in registry["federal_laws"]}
    existing_by_remote = {
        law.get("remote_path", ""): law
        for law in registry["federal_laws"]
        if "remote_path" in law
    }

    added_count = 0
    updated_count = 0

    for new_law in discovered:
        # Match by ID or Remote Path
        matched = False

        # Check by ID
        if new_law["id"] in existing_ids:
            # Update info if needed (e.g. URL changed)
            for law in registry["federal_laws"]:
                if law["id"] == new_law["id"]:
                    if law.get("url") != new_law["url"]:
                        law["url"] = new_law["url"]
                        updated_count += 1
                    matched = True
                    break

        if not matched:
            # New Law!
            # Add default metadata
            new_law["priority"] = 3  # Default low priority
            new_law["status"] = "discovered"
            new_law["tier"] = "general"
            new_law["category"] = "uncategorized"
            new_law["short_name"] = (
                new_law["name"][:50] + "..."
                if len(new_law["name"]) > 50
                else new_law["name"]
            )

            registry["federal_laws"].append(new_law)
            added_count += 1

    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4, ensure_ascii=False)

    print(f"✅ Merge Complete!")
    print(f"   Added: {added_count}")
    print(f"   Updated: {updated_count}")
    print(f"   Total: {len(registry['federal_laws'])}")


if __name__ == "__main__":
    merge_registries()
