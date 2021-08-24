import json
import os


def get_all_module_name(path):
    """  找到模块下面所有的模块名  """
    global MODULE
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == "__init__.py" and root.split("\\")[-2] == "src":
                name = root.split("\\")[-1]
                # print(name, dirs, files)
                if name not in MODULE:
                    MODULE.append(name)


def get_py_file(path):
    """  找到每个目录下面所有的 .py 文件并统计他所有的依赖"""
    py_file_map = {}
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                count += 1
                module = root.split("\\")[4]
                if module not in py_file_map:
                    py_file_map[module] = []
                py_file_map[module].append(root + '\\' + file)
                if DEBUG:
                    print(module, root + '\\' + file)
    if DEBUG:
        print(f"{path} 目录下总共找到 .py 文件 {count} 个.")
    return py_file_map


def get_per_file_rely_module_name(path):
    """ 获取单个 .py 文件的所有依赖模块名 """
    libs = []
    with open(path, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip(" ")
            if line.startswith("from "):
                rely = line.split(" ")[1].split(".")[0]
                # print(line, len(line), rely)
                if rely not in libs:
                    libs.append(rely)
    if DEBUG:
        print(f"{path} 文件里找到 {libs} 依赖")
    return libs


def get_module_rely_name(py_file_map):
    """ 遍历查找所有 .py 文件的依赖模块名 """
    ret = {}
    for module, files in py_file_map.items():
        all_libs = set()
        for file in files:
            libs = get_per_file_rely_module_name(file)
            for lib in libs:
                if lib not in MODULE:
                    continue
                all_libs.add(lib)
        ret[module] = list(all_libs)
        if DEBUG:
            print(f"{module} 模块总共依赖 {all_libs}")
    return ret


def run(search_path):
    """ 查找指定目录下的文件依赖关系 """
    py_file_map = get_py_file(search_path)
    result = get_module_rely_name(py_file_map)
    if DEBUG:
        print(f"{search_path} 模块下的所有依赖关系： {result}")
    title = search_path.split("\\")[-1]
    output = json.dumps(result)
    with open(title + ".json", "w") as f:
        f.write(output)





if __name__ == '__main__':
    """ 这是一个 windows 下的查找文件依赖关系的代码思路"""
    DEBUG = 0
    MODULE = ["freetime", "hall", "matchcomm", ""]
    absolute_path = r"D:\majiang\hall5"

    get_all_module_name(absolute_path + "\hall51")
    get_all_module_name(absolute_path + "\hall37")
    print(sorted(MODULE))

    run(absolute_path + "\hall51")
    run(absolute_path + "\hall37")



