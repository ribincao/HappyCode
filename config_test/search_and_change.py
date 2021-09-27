import json
import os


name_map = {
    "新手场": "初级场",
    "平民场": "中级场",
    "小康场": "高级场",
    "土豪场": "大师场",
    "尊爵场": "至尊场",
}


def get_json_paths():
    path = ".\\"
    change_paths = []
    for root, dirs, files in os.walk(path):
        cur = root.split("\\")
        if cur[-1] != "room":
            continue
        for file in files:
            if file == "0.json":
                continue
            tmp = root + "\\" + file
            change_paths.append(tmp)
    return change_paths


def run(paths):
    print(paths)
    f = open(".\\change_config.json", 'r', encoding='utf-8')
    configs = json.loads(f.read())
    delete_config_name = []
    for game, game_config in configs.items():
        for game_id, change_config in game_config.items():
            name = change_config["name"]
            for path in paths:
                count = 0
                with open(path, "r", encoding='utf-8') as c_f:
                    content = json.loads(c_f.read())
                    if content.get("playModeName", '') == game and content.get("name", '') in [name, name_map[name]]:
                        for attr_str, value in change_config.items():
                            attrs = attr_str.split('.')
                            tmp = content
                            for i in range(len(attrs) - 1):
                                tmp = tmp[attrs[i]]
                            if tmp[attrs[-1]] != value:
                                tmp[attrs[-1]] = value
                                count += 1
                    if content.get("playModeName", '') == game and content.get("name", '') in ["尊爵场", "至尊场"]:
                        path_name = path.split("\\")[-1]
                        if path_name not in delete_config_name:
                            delete_config_name.append(path_name)
                            print(" need delete:  ", path_name, content.get("playModeName", ''), content.get("name", ''))
                if count > 0:
                    with open(path, "w", encoding='utf-8') as w_f:
                        json.dump(content, w_f, ensure_ascii=False, sort_keys=False, indent=4)
    print("OK")


if __name__ == "__main__":
    path_s = get_json_paths()
    run(path_s)
