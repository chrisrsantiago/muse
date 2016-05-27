[trim]
[assign var="title"][gettext]Posts categorized under[/gettext] "[c]category.title[/c]"[/assign]
[transform function="base"]
    [if condition="editing"]
        <form action="[url current="true" /]" method="post">
        <fieldset>
            <legend>[gettext]Delete Category?[/gettext]</legend>
            <p>[gettext]Deleting a category will remove all of the associated posts and comments.  It cannot be undone, so think about it before selecting.[/gettext]</p>
            <p><label for="delete"><input type="checkbox" id="delete" name="delete"> [gettext]I don't want this category; delete it.[/gettext]</label></p>
        </fieldset>
        <p><label for="title">[gettext]Title[/gettext]<br><input name="title" type="text" value="[c]category.title[/c]">&nbsp;<input type="submit" value="[gettext]Save[/gettext]"></p>
    [/if]

    [if condition="editing" not="true"]
    <h1>[c]category.title[/c][if condition="user.admin"] (<a href="[url current="true" edit="true" /]">[gettext]edit[/gettext]</a>)[/if]</h1>
    [/if]

    [if condition="editing"]
        </form>
        [return /]
    [/if]
    [if condition="posts"]
        [assign var="row" json="true"]1[/assign]
        [loop value="post" iterable="posts"]
            [execute][template]_posts.tpl[/template][/execute]
        [/loop]
    [/if]
[/transform]
[/trim]