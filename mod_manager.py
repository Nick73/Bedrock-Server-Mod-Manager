import os
import json

BEHAVIOR_PACKS_JSON = "world_behavior_packs.json"
RESOURCE_PACKS_JSON = "world_resource_packs.json"

def is_excluded_pack(folder_name):
    exclude_keywords = ['vanilla', 'experimental']
    return any(keyword in folder_name.lower() for keyword in exclude_keywords)

def load_packs_json(world_path, filename):
    json_path = os.path.join(world_path, filename)
    if not os.path.isfile(json_path):
        return []
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_packs_json(world_path, filename, packs):
    json_path = os.path.join(world_path, filename)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(packs, f, indent=2)
    print(f"Wrote {len(packs)} packs to {json_path}")

class ModManager:
    def __init__(self, world_path):
        self.world_path = world_path

        self.behavior_packs = [
            mod for mod in load_packs_json(world_path, BEHAVIOR_PACKS_JSON)
            if not is_excluded_pack(mod.get('name', '')) and not is_excluded_pack(mod.get('folder', ''))
        ]
        self.resource_packs = [
            mod for mod in load_packs_json(world_path, RESOURCE_PACKS_JSON)
            if not is_excluded_pack(mod.get('name', '')) and not is_excluded_pack(mod.get('folder', ''))
        ]

    def list_packs(self, pack_type="behavior"):
        packs = self.behavior_packs if pack_type == "behavior" else self.resource_packs
        print(f"\n{'Behavior' if pack_type == 'behavior' else 'Resource'} Packs:")
        for idx, pack in enumerate(packs, 1):
            name = pack.get("name") or pack.get("folder") or pack.get("pack_id")
            print(f"{idx}. {name}")

    def move_pack(self, pack_type, old_index, new_index):
        packs = self.behavior_packs if pack_type == "behavior" else self.resource_packs
        pack = packs.pop(old_index)
        packs.insert(new_index, pack)

    def remove_pack(self, pack_type, index):
        packs = self.behavior_packs if pack_type == "behavior" else self.resource_packs
        packs.pop(index)

    def save(self):
        save_packs_json(self.world_path, BEHAVIOR_PACKS_JSON, self.behavior_packs)
        save_packs_json(self.world_path, RESOURCE_PACKS_JSON, self.resource_packs)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bedrock Mod Manager (excluding vanilla/experimental)")
    parser.add_argument("world_path", help="Path to the Minecraft world folder")
    args = parser.parse_args()

    mgr = ModManager(args.world_path)

    while True:
        print("\n--- Bedrock Mod Manager ---")
        mgr.list_packs("behavior")
        mgr.list_packs("resource")
        print("\nOptions: [m]ove [r]emove [s]ave [q]uit")
        choice = input("Enter option: ").lower()
        if choice == "m":
            t = input("Type ([b]ehavior/[r]esource): ").lower()
            pack_type = "behavior" if t == "b" else "resource"
            mgr.list_packs(pack_type)
            old = int(input("Current index (1-based): ")) - 1
            new = int(input("New index (1-based): ")) - 1
            mgr.move_pack(pack_type, old, new)
        elif choice == "r":
            t = input("Type ([b]ehavior/[r]esource): ").lower()
            pack_type = "behavior" if t == "b" else "resource"
            mgr.list_packs(pack_type)
            idx = int(input("Index to remove (1-based): ")) - 1
            mgr.remove_pack(pack_type, idx)
        elif choice == "s":
            mgr.save()
            print("Mod order saved.")
        elif choice == "q":
            break

if __name__ == "__main__":
    main()