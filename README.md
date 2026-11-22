# Positive-definite extensions of signed weights on multiplicative intervals and an endpoint formula for prime-weighted sums

**Zixu Zhao · Sichuan University**  
**赵子旭 · 四川大学**

[English paper (PDF)](papers/paper-en.pdf) · [中文论文（PDF）](papers/paper-zh.pdf) · [English LaTeX](papers/paper-en.tex) · [中文 Word 稿](papers/paper-zh.docx) · [Lean code and verification guide](lean/README.md)

Let a real weight $w$ be supported on a set $S$ of integers in $[2,X]$ with $a<2b$ for all $a,b$ in $S$. For each prime $q>X^2$, the paper constructs a nonnegative combination of all Dirichlet characters modulo $q$ that interpolates $w$ on the entire integer window, including the zeros outside $S$. Taking $c>0$, the coefficients have total mass $c+\sum_{n\in S}w(n)^2/c$. The paper also proves a worst-case lower bound on this mass and an exact adjacent-endpoint formula for the von Mangoldt weighted sum. Deriving bounds for each individual even integer would require an additional estimate.

对支撑于一个乘法区间的实权，本文在素模数上给出一组显式的非负狄利克雷特征系数。它们在指定窗口内逐点还原原权，并保留支撑外的零。论文证明了系数总质量的上界与最坏情形下界，给出相邻两个端点精确恢复冯·曼戈尔特加权和的公式，并用算例说明素数幂的贡献。逐个偶数的哥德巴赫误差估计仍待证明。

## Lean verification

The formalization uses Lean 4.13.0 and Mathlib at commit `d7317655e2826dc1f1de9a0c138db2775c4bb841`. The two projects together contain 14 proof modules and public-axiom audits for 36 declarations. The audit records include the SHA-256 digests of the source files used for the checks.

| Result | Lean source |
| --- | --- |
| Positive interpolation and total mass | [PrimeWindow.lean](lean/MathlibLibrary/PrimeWindow.lean) |
| Explicit coefficients and conjugation symmetry | [FourierWindow.lean](lean/MathlibLibrary/FourierWindow.lean) |
| Lower bound for some choice of signs | [CharacterLowerBound.lean](lean/MathlibLibrary/CharacterLowerBound.lean) |
| Endpoint identity for the von Mangoldt sum | [PrimeEndpoint.lean](lean/MathlibLibrary/PrimeEndpoint.lean) |
| Limits of a one-sided upper bound | [WindowObstruction.lean](lean/MathlibLibrary/WindowObstruction.lean) |

With the pinned Lean toolchain, Git, and Python 3 installed, run the following from the repository root. The Mathlib build requires network access to fetch dependencies on the first run.

```sh
cd lean
lake build
python verify.py --out verification-local.json
cd MathlibLibrary
lake update
lake exe cache get
lake build
python verify_mathlib.py --out verification-local.json
```

The Mathlib audit checks the Git revision of the library on Lean’s search path against the paper’s lock file. This also applies when you pass an existing project to `--mathlib-project`.

[Standard library audit](lean/verification.json) · [Mathlib audit](lean/MathlibLibrary/verification.json) · [中文复核说明](lean/README.md)

## AI assistance

Generative AI assisted in developing the arguments, drafting and translating the manuscript, and writing the Lean proofs. The proof statements and their axiom dependencies can be checked using the commands above. 生成式 AI 参与了推导、论文撰写与翻译以及 Lean 证明代码编写。仓库同时提供定理的精确表述和可复核的检验记录。
