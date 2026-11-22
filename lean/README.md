# 乘法区间上带符号权的正定延拓

本库附属于同名中文研究论文。主问题是在给定的整数窗口内，把能取负值的权精确写成狄利克雷特征的非负线性组合，并计算正系数总量和素数加权和。库分为两个可分别重建的项目，均使用 Lean 4.13.0。

## 阅读入口

| 正文对象 | 模块及入口 |
| --- | --- |
| 素模数上全部复狄利克雷特征的正交性 | MathlibLibrary/Orthogonality.lean，Goldbach.PrimeCharacter.orthogonality |
| 逐点显式非负权以及质量公式 | MathlibLibrary/FourierWindow.lean，Goldbach.FourierWindow.dirichletCoeff 和 dirichlet_window_coefficients |
| 定理 1，包含整个窗口的零坐标及归一化总质量 | MathlibLibrary/PrimeWindow.lean，Goldbach.PrimeCharacter.positive_window 及 positive_window_sqrt |
| 主特征质量及参数最优化 | MathlibLibrary/PrincipalMass.lean，principal_mass 与 mass_lower_bound |
| 分块相加与系数界 | MathlibLibrary/Blocks.lean，Goldbach.PrimeCharacter.block_sum；以给定的各块为输入 |
| 命题 2 的有限矩阵下界与特征实例 | MathlibLibrary/RademacherBound.lean 中的 exists_signs_mass_lower_bound，及 CharacterLowerBound.lean |
| 定理 4，与实际冯·曼戈尔特权的恒等式 | MathlibLibrary/PrimeEndpoint.lean，Goldbach.PrimeEndpoint.vonMangoldt_endpoint |
| 单边函数上界对端点差分的局限 | MathlibLibrary/WindowObstruction.lean，nonpositive_large_endpoint |
| 引理 3，精确斜坡端点和对数中心化 | MathlibLibrary/PaperFourier.lean，PaperFourier.ramp_endpoint 和 centered_ramp_endpoint |
| 无需 Mathlib 的整数证书、正半定二次型及整数差分 | 根目录 Main.lean、GramCertificate.lean、PositiveWindow.lean、RampEndpoint.lean |
| 第 5 节的数值例子 | 根目录 verify.py，以整数和有理数独立复算全部 61 个窗口坐标、总质量及主特征系数 |

变量剖面与正文相同。X 表示窗口终点，q 是大于 X² 的素数，S 是给定的支撑，w 是给定实权。有限正交性在本库内对全部狄利克雷特征证明。对单位元的系数和可以直接读出，归一化采用任意 c>0。

## 复核

安装 lean-toolchain 指定版本，并让 lean、lake、Python 3 出现在命令路径中。源码索引工具单独要求 Python 3.11 或以上版本。各项目的 verification.json 是随包交付源码的实测编译及公理审计记录。编译脚本会把本地模块的 .olean 输出到新建的临时目录，记录源文件哈希并检查各入口的公理列表。

### 标准库证书与算例

进入解压目录运行：

    lake build
    python verify.py --out verification-local.json

### 全部狄利克雷特征、实权和精确对数

进入 MathlibLibrary 子目录运行下列命令。首次下载需具备 Git 和网络连接。

    lake update
    lake exe cache get
    lake build
    python verify_mathlib.py --out verification-local.json

Mathlib 固定为 d7317655e2826dc1f1de9a0c138db2775c4bb841，版本 v4.13.0。首次下载需要联网，缓存准备好后重复验证可离线进行。已有相同版本 Mathlib 工程和相应缓存时，也可以在子目录运行 python verify_mathlib.py --mathlib-project <已有工程路径>。验证输出如出现 sorryAx 或自定义公理，脚本会报告失败。

使用已有工程时，验证脚本会从 Lean 的搜索路径找到实际使用的 Mathlib，并将其 Git 提交与本论文的锁文件比对。

## 源码出处

survey/scan.json 记录启发本文的 Alpöge 作者归档指纹与静态索引汇总。survey/scan_source.py 可从同一份源码归档重新统计。该扫描按实际源码换行统计物理行，包括注释与空行。它不执行原库的 Lean 重编译。论文内新证书与原库的计算证明各自独立，可分别核验。

- 作者笔记：https://alpo.ge/remark.pdf
- 归档 SHA-256：9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc
- 原库入口：https://github.com/CocoSgt/riemann-hypothesis-lean
- 原库核验记录：https://math.mit.edu/~drew/grh/

哥德巴赫猜想所需的逐个偶数误差估计尚待证明。论文第 5 节说明该估计还需要控制哪个差分。
