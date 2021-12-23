Mkdocs Markdown Graphviz (for Python 3)
=======================================

⚠️ WARNING ⚠️ **This Page is OUTDATED, PLEASE DO NOT USE**: it has been preserved for archive purposes.

This Project Repository has been:

* moved to **GITLAB** : [rodrigo.schwencke/mkdocs-graphviz](https://gitlab.com/rodrigo.schwencke/mkdocs-graphviz/)
* renamed to the new name `mkdocs-graphviz`
* uploaded to PyPI: [mkdocs-graphviz](https://pypi.org/project/mkdocs-graphviz/)

Please refer to GITLAB instructions for install & configs.

-------

This is just a continuation of the great job of :

* Cesare Morel [cesaremorel/markdown-inline-graphviz](https://github.com/cesaremorel/markdown-inline-graphviz), and before him,
* Steffen Prince in [sprin/markdown-inline-graphviz](https://github.com/sprin/markdown-inline-graphviz), 
* Initially inspired by Jawher Moussa [jawher/markdown-dot](https://github.com/jawher/markdown-dot)

in order to get it work with pip for python 3 (pip3). If you use python 2, please use the original extension instead.

A Python Markdown extension for Mkdocs, that renders inline Graphviz definitions with inline SVGs or PNGs out of the box !

Why render the graphs inline? No configuration! Works with any
Python-Markdown-based static site generator, such as [MkDocs](http://www.mkdocs.org/), [Pelican](http://blog.getpelican.com/), and
[Nikola](https://getnikola.com/) out of the box without configuring an output directory.

# Installation

    $ pip install mkdocs-markdown-graphviz

# Usage

Activate the `mkdocs_markdown_graphviz` extension. For example, with Mkdocs, you add a
stanza to mkdocs.yml:

```yaml
markdown_extensions:
    - mkdocs_markdown_graphviz
```

To use it in your Markdown doc, 

with SVG output:

    ```graphviz dot attack_plan.svg
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
    ```

or with PNG:

    ```graphviz dot attack_plan.png
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
    ```

Supported Graphviz commands: dot, neato, fdp, sfdp, twopi, circo.

# Credits

Forked from [cesaremorel/markdown-inline-graphviz](https://github.com/cesaremorel/markdown-inline-graphviz)

Inspired by [jawher/markdown-dot](https://github.com/jawher/markdown-dot),
which renders the dot graph to a file instead of inline.

# License

[MIT License](http://www.opensource.org/licenses/mit-license.php)
