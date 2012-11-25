import markdown
import mdx_latex

class TestMkdn2Latex:

    mkdn_input = \
'''# Anna Karenina #

## A first section ##

A simple list:

  1. Item 1
  2. Item 2

An unordered list:

  * First bullet
  * Second bullet

Now we have a blockquote:

> A big quote that goes on, and on, and on, and on, and on, and on, and on, and
> on
>
> A big quote that goes on, and on, and on, and on, and on, and on, and on, and
> on
>
> A big quote that goes on, and on, and on, and on, and on, and on, and on, and
> on

Some mathematics inline, $$X$$, a $100 million, a %tage and then a formula:

$$ \\sum_{i}^{\\infty} x^{n} + y^{n} = \\alpha +  \\beta * z^{n} $$

A paragraph with a[^fn1] footnote in it[^fn1].

[^fn1]: a very dull footnote indeed
       
       but it does have mutiple paragraphs.

A table now (this is *really* complicated):

<table class="data">
    <caption>My Caption</caption>
    <thead>
        <tr>
            <th>Heading 1</th><th>Heading 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1.0%</td><td>2.0%</td>
        </tr>
        <tr>
            <td>1.0</td><td>2.0</td>
        </tr>
    </tbody>
</table>

Now let's try having an image:

<img src="blah.png" alt="abc abc" class="xyz" />

Stuff we should escape A&R, a %tage sign

    Now some preformatted text:
    
      $ sudo python ...
'''
    expected = \
'''\\title{Anna Karenina}

% ----------------------------------------------------------------
\maketitle
% ----------------------------------------------------------------


\\section{A first section}

A simple list:

\\begin{enumerate}
  \\item Item 1
  \\item Item 2
\\end{enumerate}

An unordered list:

\\begin{itemize}
  \\item First bullet
  \\item Second bullet
\\end{itemize}

Now we have a blockquote:

\\begin{quotation}
A big quote that goes on, and on, and on, and on, and on, and on, and on, and
on

A big quote that goes on, and on, and on, and on, and on, and on, and on, and
on

A big quote that goes on, and on, and on, and on, and on, and on, and on, and
on
\\end{quotation}

Some mathematics inline, $X$, a \\$100 million, a \\%tage and then a formula:

\\[ \\sum_{i}^{\\infty} x^{n} + y^{n} = \\alpha +  \\beta \cdot z^{n} \\]

A paragraph with a\\footnote{a very dull footnote indeed

but it does have mutiple paragraphs.} footnote in it\\footnote{a very dull footnote indeed

but it does have mutiple paragraphs.}.

A table now (this is \\emph{really} complicated):

\\begin{table}
\\begin{tabular}{|c|c|}
\\hline
\\textbf{Heading 1} & \\textbf{Heading 2} \\\\
\\hline
1.0\\% & 2.0\\% \\\\
\\hline
1.0 & 2.0 \\\\
\\hline
\\end{tabular}
\\\\[5pt]
\\caption{My Caption}
\\end{table}

Now let's try having an image:

\\begin{figure}
\\centering
\\includegraphics[width=\\textwidth]{blah.png}
\\caption{abc abc}
\\end{figure}

Stuff we should escape A\\&R, a \\%tage sign

\\begin{verbatim}
Now some preformatted text:

  \\$ sudo python ...
\\end{verbatim}'''
    md = markdown.Markdown(None)

    def test_1(self):
        ltx = mdx_latex.makeExtension()
        # or just mdx_latex.LaTeXExtension()
        ltx.extendMarkdown(self.md, markdown.__dict__)
        # self.footnoteExtension.extendMarkdown(self.mdx_latexer)
        out = self.md.convert(self.mkdn_input)
        outlines = out.split('\n')
        explines = self.expected.split('\n')
        # TODO: this misses stuff if out > exp
        print '******** EXPECTED *********'
        print self.expected
        print '******** ACTUAL *********'
        print out
        print '******** ANALYSIS *********'
        for ii in range(len(explines)):
            if outlines[ii] != explines[ii]:
                print ii
                print 'out:', '"%s"' % outlines[ii]
                print 'exp:', '"%s"' % explines[ii]
        if len(explines) < len(outlines):
            print 'Out longer than expected:'
            print outlines[len(explines):]
        # for ii in range(len(out)):
        #    if out[ii] != self.expected[ii]:
        #        print out[ii:ii+10]
        assert out == self.expected 

class TestEscapeLatexEntities:

    in1 = \
'''"Hello world". & C## Don't have 'another quote"

Now for "'Something a little' more complicated". "And again."
'''
    exp1 = \
'''``Hello world''. \\& C\#\# Don't have `another quote''

Now for ```Something a little' more complicated''. ``And again.''
'''

    def test_1(self):
        out = mdx_latex.escape_latex_entities(self.in1)
        print out
        assert out == self.exp1
        # for ii in range(len(out)):
        #    print ii
        #    assert out[ii] == self.exp1[ii]

class TestTable2Latex:

    intable1 = '''
<table>
    <caption>My Caption</caption>
    <thead>
        <tr>
            <th id="99" colspan="3">Heading 1</th><th>Heading 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1.0</td><td>2.0</td><td>1.0</td><td>2.0</td></tr>
        <tr>
            <td>1.0</td><td>2.0</td><td>1.0</td><td>2.0</td>
        </tr>
    </tbody>
</table>'''

    exp1 = u'''
\\begin{table}
\\begin{tabular}{|c|c|c|c|}
\\hline
\\multicolumn{3}{|c|}{\\textbf{Heading 1}} & \\textbf{Heading 2} \\\\
\\hline
1.0 & 2.0 & 1.0 & 2.0 \\\\
\\hline
1.0 & 2.0 & 1.0 & 2.0 \\\\
\hline
\\end{tabular}
\\\\[5pt]
\\caption{My Caption}
\\end{table}
'''

    def test_1(self):
        converter = mdx_latex.Table2Latex()
        out = converter.convert(self.intable1)
        ss = unicode(self.exp1)
        print out
        print ss
        assert out == ss

class TestMathConvert:

    intext = '''
$$ \\sum_{x=1} ... $$

Hello world, $$x$$. $100 million.

$$x=5$$, but then along comes the fox! $$y=6$$

$$
\begin{eqnarray}
W & = & y + z \\\\
  & = & 3x
\end{eqnarray}
$$
'''

    outtext = '''
\\[ \\sum_{x=1} ... \\]

Hello world, $x$. \$100 million.

$x=5$, but then along comes the fox! $y=6$

\\[
\begin{eqnarray}
W & = & y + z \\\\
  & = & 3x
\end{eqnarray}
\\]
'''

    def test_1(self):
        converter = mdx_latex.MathTextPostProcessor()
        out = converter.run(self.intext)
        print out
        assert out == self.outtext

class TestImgConvert:

    intext = '''
<img src="blah.png" alt="abc abc" class="xyz" />
'''

    exp1 = '''
\\begin{figure}
\\centering
\\includegraphics[width=\\textwidth]{blah.png}
\\caption{abc abc}
\\end{figure}
'''

    def test_1(self):
        converter = mdx_latex.Img2Latex()
        out = converter.convert(self.intext)
        print out
        assert out == self.exp1
