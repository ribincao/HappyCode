import json

from conf import *
import xlrd


def format_config(config):
    config_dict = {}
    # print(config)
    game_name, game_start_id = "", 0
    for row in config:
        if row[0] != '':
            game_start_id = game_maps[row[0]]
            game_name = row[0]
        if row[1] == '':
            continue
        attr = attr_maps[row[1]]
        config_dict[attr] = row[2:]
    result = {}
    for attr, attr_values in config_dict.items():
        for idx in range(len(attr_values)):
            if attr_values[idx] == '':
                continue
            game_id = game_start_id + idx
            if game_id not in result:
                result[game_id] = dict()
                result[game_id]["name"] = level_maps[idx]
            value = -1
            if attr_values[idx] != '不限':
                value = int(attr_values[idx])
            result[game_id][attr] = value
    # print(config_dict)
    # print(result)
    output = dict()
    output["name"] = game_name
    output["result"] = result
    return output


def get_config(url):
    book = xlrd.open_workbook(url)
    sheet = book.sheets()[0]
    # print(sheet.nrows, sheet.ncols)
    configs = []
    for i in range(1, sheet.nrows - 5):
        values = sheet.row_values(i)
        configs.append(values)
    # print(len(configs))

    n = len(configs) // 5
    split_configs = []
    for index in range(n):
        start = index * 5
        split_configs.append(configs[start:start + 5])
    # print(len(split_configs), split_configs)

    json_configs = {}
    for index in range(len(split_configs)):
        each_config = split_configs[index]
        json_config = format_config(each_config)
        json_configs[json_config["name"]] = json_config["result"]
    # print(json_configs)
    return json_configs


def dump_config(data):
    with open("change_json.json", 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=False, indent=4)


def main():
    url = "场次配置表.xlsx"
    ret = get_config(url)
    dump_config(ret)
    # for k, v in ret.items():
        # print(k, v)


if __name__ == "__main__":
    main()
