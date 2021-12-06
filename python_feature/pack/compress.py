import zlib, base64
import json

def compress(obj):
    """ obj -> str """
    a = json.dumps(obj)                     # str: "obj..."
    b = zlib.compress(a.encode("utf-8"))    # str: x\x9c\x8b\x8e\x05\x00\x01\x15\x00\xb9...
    c = base64.urlsafe_b64encode(b)         # str: eJyLjgUAARUAuQ==...
    return c

def decompress(s):
    """ str/unicode -> obj """
    # if isinstance(s, unicode):  # python2 里面的 Unicode -> str
    #     s = s.encode("utf-8")
    a = base64.urlsafe_b64decode(s)         # str: x\x9c\x8b\x8e\x05\x00\x01\x15\x00\xb9...
    b = zlib.decompress(a)                  # str: "obj..."
    c = json.loads(b)                       # obj: obj
    return c


if __name__ == "__main__":
    print()
    st = u"eJzVUrtuwzAM_BXDUwp40IuU1LlLgE7taGfwQ0kNpHHR2FOQf-8paV5tEqCvoRosHo-UTvTlq7RqZw9d9zxu0ttESZbCZEnahL5s53dhWd-3yx5MnqfF4GQoi4GNdaNiIK88UiLIDLkgqBhMEAIpZVW2AeCZvUWt0lV23A_gKbhtI4B1XB8Oo7JBT7BlPIWaTCHntL9JoczHBVaIBlBKb8RmgdrdSVXF4FSstFmST7IEtMC2eQQuGZ1VfFkR6br-8JZPIgGsCfhOlThRbNnt9SI-UVvt1YL5gtQzw_3mPKUkdTROUhf0RepIIPa07_py_lh3rwEGkdrx_k_07Twsx4tpB2K1RdFDseklLGa7uH5qd-GsfE-vY3uslqydJVbSIPXPbUra-F-zKTc2ag0eBGuC5diK61J_5F9Jmg8OAbjkEFDXHEIkFP-FQxyvJ2-Mq09b"
    r = decompress(st)
    print(type(r), r)

    print()
    o = {"bigRoomId": 216201, "playMode": "xueliuhongzhong"}
    zo = compress(o)
    print(type(zo), zo)