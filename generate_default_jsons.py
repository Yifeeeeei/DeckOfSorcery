import json


if __name__ == "__main__":
    json_in_path = "template_mass_producer_params_xlsx.json"
    template = json.load(open(json_in_path, "r", encoding="utf-8"))
    json_path = "mass_producer_params_xlsx.json"
    json.dump(
        template, open(json_path, "w", encoding="utf-8"), ensure_ascii=False, indent=4
    )
