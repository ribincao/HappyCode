import time
from importlib import reload

"""
1. 更新代码(class | function | method |  staticmethod)
2. 不更新数据对象
3. 复杂的改动最好还是重启进程
"""
# def reload(module):
#     """
#     Reload the module and return it.
# 
#     The module must have been successfully imported before.
# 
#     """
#     if not module or not isinstance(module, types.ModuleType):
#         raise TypeError("reload() argument must be a module")
#     try:
#         name = module.__spec__.name
#     except AttributeError:
#         name = module.__name__
# 
#     if sys.modules.get(name) is not module:
#         msg = "module {} not in sys.modules"
#         raise ImportError(msg.format(name), name=name)
#     if name in _RELOADING:
#         return _RELOADING[name]
#     _RELOADING[name] = module
#     try:
#         parent_name = name.rpartition('.')[0]
#         if parent_name:
#             try:
#                 parent = sys.modules[parent_name]
#             except KeyError:
#                 msg = "parent {!r} not in sys.modules"
#                 raise ImportError(msg.format(parent_name),
#                                   name=parent_name) from None
#             else:
#                 pkgpath = parent.__path__
#         else:
#             pkgpath = None
#         target = module
#         spec = module.__spec__ = _bootstrap._find_spec(name, pkgpath, target)
#         if spec is None:
#             raise ModuleNotFoundError(f"spec not found for the module {name!r}", name=name)
#         _bootstrap._exec(spec, module)
#         # The module may have replaced itself in sys.modules!
#         return sys.modules[name]
#     finally:
#         try:
#             del _RELOADING[name]
#         except KeyError:
#             pass
        
        
if __name__ == '__main__':
    while True:
        import test
        reload(test)
        t = test.Test("ribincao")
        print(test.a, test.incr(test.a))
        t.hello()
        t.hi()
        time.sleep(3)
