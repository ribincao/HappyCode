参考链接: https://www.ruanyifeng.com/blog/2017/09/flame-graph.html
- perf(performance)命令返回CPU正在执行的函数名及调用栈, 通常它的频率是99Hz(每秒统计99次)
    ```shell
    # record表示记录，-F 99表示每秒99次，-p 13204是进程号，-g表示记录调用栈，sleep 30则是持续30秒
    sudo perf record -F 99 -p 13204 -g -- sleep 30
    ```
- 火焰图是基于 perf 结果产生的 SVG 图片，用来展示 CPU 的调用栈
    - y 轴表示调用栈，每一层都是一个函数。调用栈越深，火焰就越高，顶部就是正在执行的函数，下方都是它的父函数
    - x 轴表示抽样数，如果一个函数在 x 轴占据的宽度越宽，就表示它被抽到的次数多，即执行的时间长。注意，x 轴不代表时间，而是所有的调用栈合并后，按字母顺序排列的
    - 火焰图就是看顶层的哪个函数占据的宽度最大。只要有"平顶"（plateaus），就表示该函数可能存在性能问题
    - 调用栈: 底层函数调用上层函数, 也就是说真正在执行的是上层函数, 顶部函数宽度越宽说明抽样调查的时候大部分都在执行它, 也就是说执行时间长一些
    - 局限情况
        - 调用栈不完整: 当调用栈过深时，某些系统只返回前面的一部分（比如前10层）
        - 函数名缺失: 有些函数没有名字，编译器只用内存地址来表示（比如匿名函数）
- 火焰图生成工具: https://github.com/brendangregg/FlameGraph
    ```shell
    yum -y install perf.x86_64
    git clone https://github.com/brendangregg/FlameGraph.git
    export PATH=xxx/FlameGraph:$PATH
    # 或cp -r xxx/FlameGraph/* ~/bin/

    # both user and kernel
    # perf record -F 99 -a -g -- sleep 60
    # only pid = 12345
    sudo perf record -F 99 -p 12345 -g -- sleep 60
    # perf script > out.perf

    perf script -i perf.data &> perf.unfold
    ./stackcollapse-perf.pl perf.unfold &> perf.folded
    ./flamegraph.pl perf.folded > perf.svg
    ```
    - 下载FlameGraph工具并添加环境变量 -> perf record 生成记录 -> perf script生成 unfold 文件 -> stackcollapse-perf.pl生成 fold文件 -> flamegraph.pl -> 生成svg文件 -> 浏览器打开perf.svg文件

一次测试
```shell
git clone https://github.com/brendangregg/FlameGraph.git
cd FlameGraph

sudo perf record -F 99 -p 12345 -g -- sleep 60
perf script -i perf.data &> perf.unfold
./stackcollapse-perf.pl perf.unfold &> perf.folded
./flamegraph.pl perf.folded > perf.svg
```