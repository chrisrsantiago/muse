[trim]
[assign var="title"][gettext]Search[/gettext][if condition="terms"] - [c]terms[/c][/if][/assign]
[transform function="base"]
    [if condition="results"]
        <p>[gettext]We have something, chief![/gettext]</p>
        <h2>[gettext]Search Results[/gettext]</h2>
        [assign var="row" json="true"]1[/assign]
        [loop value="result" iterable="results"]
            <h3><a href="[c]result.url[/c]">[c]result.title[/c]</a></h3>
            [if condition="result.summary"]
                <p>[c]result.summary[/c]</p>
            [/if]
            [if condition="result.summary" not="true"]
                <p>[gettext]No Summary[/gettext]</p>
            [/if]
            [if condition="result.highlights"]
                <p>[c entities="false"]result.highlights[/c]</p>
            [/if]
        [/loop]
    [/if]

    [if condition="results" not="true"]
        <p>[gettext]No results found for[/gettext] <strong>[c]terms[/c]</strong></p>
    [/if]
[/transform]
[/trim]