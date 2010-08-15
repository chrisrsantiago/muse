[trim]
[assign var="title"][gettext]Home[/gettext][/assign]
[transform function="base"]
    [if condition="posts" not="true"]
        <p>[gettext]There are no posts. That is unacceptable.[/gettext]</p>
        [return /]
    [/if]

    [assign var="row" json="true"]1[/assign]
    [loop value="post" iterable="posts"]
        [execute][template]_posts.tpl[/template][/execute]
    [/loop]
[/transform]
[/trim]