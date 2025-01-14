"""
Graphviz extensions for Markdown (e.g. for mkdocs)
Renders the output inline, eliminating the need to configure an output
directory.

Supports outputs types of SVG and PNG. The output will be taken from the
filename specified in the tag. Example:

in SVG:

```dot
digraph G {
    rankdir=LR
    Earth [peripheries=2]
    Mars
    Earth -> Mars
}
```

```graphviz dot attack_plan.svg
digraph G {
    rankdir=LR
    Earth [peripheries=2]
    Mars
    Earth -> Mars
}
```

in PNG:

```graphviz dot attack_plan.png
digraph G {
    rankdir=LR
    Earth [peripheries=2]
    Mars
    Earth -> Mars
}
```

Requires the graphviz library (http://www.graphviz.org/) and python 3

Inspired by jawher/markdown-dot (https://github.com/jawher/markdown-dot)
Forked from  cesaremorel/markdown-inline-graphviz (https://github.com/cesaremorel/markdown-inline-graphviz)
"""

import re
import markdown
import subprocess
import base64

# Global vars
BLOCK_RE_GRAVE_ACCENT = re.compile(
        r'^[ ]*```graphviz[ ]* (?P<command>\w+)\s+(?P<filename>[^\s]+)\s*\n(?P<content>.*?)```\s*$',
    re.MULTILINE | re.DOTALL)

BLOCK_RE_GRAVE_ACCENT_DOT = re.compile(
        r'^[ ]*```dot.(?P<content>.*?)```\s*$',
    re.MULTILINE | re.DOTALL)

GRAPHVIZ_COMMAND = 0

# Command whitelist
SUPPORTED_COMMAMDS = ['dot', 'neato', 'fdp', 'sfdp', 'twopi', 'circo']


class MkdocsMardownGraphvizExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add MkdocsMarkdownGraphvizPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('graphviz_block',
                             MkdocsMarkdownGraphvizPreprocessor(md),
                             "_begin")


class MkdocsMarkdownGraphvizPreprocessor(markdown.preprocessors.Preprocessor):

    def __init__(self, md):
        super(MkdocsMarkdownGraphvizPreprocessor, self).__init__(md)

    def repair_broken_svg_in(self, output):
        """Returns a repaired svg output. Indeed:
        The Original svg ouput is broken in two places:
        - in the DOCTYPE, after "\\EN". Does not break the code, but still
        - in the svg tag, after the 'height' attribute; THIS BREAKS THE CODE AND HAD TO BE REPAIRED
        """
        encoding='utf-8'
        output = output.decode(encoding)
        lines = output.split("\n")
        newLines = []
        searchText = "Generated by graphviz"
        for i in range(len(lines)):
            if i+3 <= len(lines)-1 and ( (searchText in lines[i+1]) or (searchText in lines[i+2]) or (searchText in lines[i+3]) ) :
                continue
            if i>=3 and ("<svg" in lines[i-1] and searchText in lines[i-4]):
                continue
            if i>=3 and ("<svg" in lines[i] and searchText in lines[i-3]):
                newLines.append(lines[i]+lines[i+1])
            else:
                newLines.append(lines[i])
        newOutput = "\n".join(newLines)
        xmlHeaders = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n"""
        newOutput = xmlHeaders + newOutput
        return newOutput

    def read_block(self, text:str)->(str, int) or (None, -1):
        """Returns a tuple:
        - the graphviz or dot block, if exists, and
        - a code integer to caracterize the command : 
            0 for a'grapvhiz' command, 
            1 if 'dot' command)  
        or (None, None), if not a graphviz or dot command block"""
        blocks = [BLOCK_RE_GRAVE_ACCENT.search(text),
                  BLOCK_RE_GRAVE_ACCENT_DOT.search(text)]
        for i in range(len(blocks)):
            if blocks[i] is not None:
                return blocks[i], i
        return None, -1

    def get_decalage(self, command:str, text:str)->int:
        """Renvoie le décalage (nombre d'espaces) où commencent les ``` dans la ligne ```command ...
        Cela suppose que le 'text' réellement la commande, ce qui est censé être le cas lros de l'utilisation de cette fonction
        """
        # command = 'dot' or 'graphviz dot' or 'graphviz neato' or etc..
        i_command = text.find(command)-3
        i_previous_linefeed = text[:i_command].rfind("\n")
        decalage = i_command - i_previous_linefeed-1
        return decalage

    def run(self, lines):
        """ Match and generate dot code blocks."""

        text = "\n".join(lines)
        while 1:
            m, block_type = self.read_block(text)
            if not m:
                break
            else:
                if block_type == GRAPHVIZ_COMMAND: # General Graphviz command
                    command = m.group('command')
                     # Whitelist command, prevent command injection.
                    if command not in SUPPORTED_COMMAMDS:
                        raise Exception('Command not supported: %s' % command)
                    filename = m.group('filename')
                    decalage = self.get_decalage("graphviz "+command, text)
                else: # DOT command
                    filename = "test.svg"
                    command = "dot"
                    decalage = self.get_decalage(command, text)
                filetype = filename[filename.rfind('.')+1:]
                args = [command, '-T'+filetype]
                content = m.group('content')

                try:
                    proc = subprocess.Popen(
                        args,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE)
                    proc.stdin.write(content.encode('utf-8'))
                    output, err = proc.communicate()

                    if filetype == 'svg':
                        output = self.repair_broken_svg_in(output)
                        encoding = 'base64'
                        output = output.encode('utf-8')
                        output = base64.b64encode(output).decode('utf-8')
                        data_url_filetype = 'svg+xml'
                        data_path = "data:image/%s;%s,%s" % (
                            data_url_filetype,
                            encoding,
                            output)
                        img = " "*decalage+"![" + filename + "](" + data_path + ")"
                    
                    if filetype == 'png':
                        data_url_filetype = 'png'
                        encoding = 'base64'
                        output = base64.b64encode(output).decode('utf-8')
                        data_path = "data:image/%s;%s,%s" % (
                            data_url_filetype,
                            encoding,
                            output)
                        img = " "*decalage+"![" + filename + "](" + data_path + ")"

                    text = '%s\n%s\n%s' % (
                        text[:m.start()], img, text[m.end():])

                except Exception as e:
                        err = str(e) + ' : ' + str(args)
                        return (
                            '<pre>Error : ' + err + '</pre>'
                            '<pre>' + content + '</pre>').split('\n')

        return text.split("\n")

def makeExtension(*args, **kwargs):
    return MkdocsMardownGraphvizExtension(*args, **kwargs)
