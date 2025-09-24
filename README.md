# rbf-lang

[![PyPI version](https://badge.fury.io/py/rbf-lang.svg)](https://pypi.org/project/rbf-lang/)
[![publish](https://github.com/MarcinKonowalczyk/rbf-lang/actions/workflows/publish.yml/badge.svg)](https://github.com/MarcinKonowalczyk/rbf-lang/actions/workflows/publish.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Python versions](https://img.shields.io/badge/python-3.9%20~%203.14-blue)
[![Snapcraft](https://img.shields.io/badge/Snapcraft-e95420?logo=snapcraft&logoColor=fff)](#)

[Reversible BitFuck](https://esolangs.org/wiki/Reversible_Bitfuck) (RBF) is a [reversible Turing tarpit](https://cstheory.stackexchange.com/questions/22128/reversible-turing-tarpits). It is based on a tape of bits and has 5 commands:

 - `*` Toggle the current bit
 - `>` Shift the tape head right
 - `<` Shift the tape head left
 - `(` If the current bit is zero, jump past matching `)`
 - `)` If the current bit is zero, jump to just after matching `(`

Here is an example program operating on 3 bits. Bit 0 is the source bit (`x`), bit 1 is the target bit (`y`) and bit 2 is the temporary bit (`f`). Here the value of `x` is being moved to `y`.

```
# x=?, y=0, f=0
(>>*<<)        # set f if x is set
>>(            # if f is set
    <(>*<)*    # set y
    <*(>>*<<)  # unset x
>>)
<(>*<)         # if y is set, unset f
```

we can run the above program on an example tape (`100`) with rbf cli:

```sh
rbf run -t 100 "(>>*<<)>>(<(>*<)*<*(>>*<<)>>)<(>*<)"  # outputs 010
```

Since RBF is reversible, we can easily create a move left program:

```sh
rbf reverse "(>>*<<)>>(<(>*<)*<*(>>*<<)>>)<(>*<)"  # outputs (>*<)>(<<(>>*<<)*>*(>*<)>)<<(>>*<<)
```

## installation

RBF can be installed from source with

```sh
pip install .
```

or from pypi with

```sh
pip install rbf-lang
```


## links

_(as of yet uncategorised links to related topics. Will be sorted and expanded in the future)_

- https://en.wikipedia.org/wiki/Toffoli_gate
- https://arxiv.org/abs/1110.2574
- https://www.sciencedirect.com/science/article/abs/pii/016727899090185R?via%3Dihub
- http://weblog.raganwald.com/2004/10/beware-of-turing-tar-pit.html
