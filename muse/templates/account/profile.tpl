[trim]
[assign var="title"][gettext]Profile:[/gettext] [c]profile.name[/c][/assign]
[transform function="base"]

    [if condition="editing"]
    <form action="[url controller="account" action="profile" id="[c]profile.id[/c]" edit="true" /]" method="post">
        [if condition="user.admin"]
        <fieldset>
            <legend>[gettext]Delete User?[/gettext]</legend>
            <p>[gettext]Deleting a user will remove all of the user's comments, posts and other associated records from the system.  It cannot be undone, so think about it before selecting.[/gettext]</p>
            <p><label for="delete"><input type="checkbox" id="delete" name="delete"> [gettext]I don't care; delete this user.[/gettext]</label></p>
        </fieldset>
        [/if]
        <p><a href="[url controller="account" action="profile" id="[c]profile.id[/c]" /]">Back to Profile</a></p>
        <p><label for="name">[gettext]Name[/gettext]<br><input id="name" name="name" type="text" value="[c]profile.name[/c]"></label>&nbsp;<input type="submit" value="[gettext]Save[/gettext]"></p>
    [/if]

    [if condition="editing" not="true"]
    <h1>[c]profile.name[/c][if condition="canedit"] (<a href="[url controller="account" action="profile" id="[c]profile.id[/c]" edit="true" /]">[gettext]edit[/gettext]</a>)[/if]</h1>
    [/if]

    <div id="profile-details">
        <div class="column">
            [if condition="profile.email"]<p>[gravatar][c]profile.email[/c][/gravatar]</p>[/if]
            [if condition="profile.email" not="true"]<p>[gravatar][c]profile.ip[/c][/gravatar]</p>[/if]
        </div>

        <div class="column">
            <p><strong>[gettext]Comments[/gettext]</strong><br>[c]comments_count[/c]</p>
            <p><strong>[gettext]OpenID[/gettext]</strong><br>
                [if condition="editing"]<input name="identifier" type="text" value="[c]profile.identifier[/c]">[/if]
                [if condition="editing" not="true"][c]profile.identifier[/c][/if]
            </p>
        </div>

        <div class="column">
            <p><strong>[gettext]Posts[/gettext]</strong><br>[c]posts_count[/c]</p>
            <p><strong>[gettext]Email[/gettext]</strong><br>
                [if condition="editing"]<input name="email" type="text" value="[c]profile.email[/c]">[/if]
                [if condition="editing" not="true"][transform function="htmlencode"][c]profile.email[/c][/transform][/if]
            </p>
        </div>

        <div class="column">
            <p><strong>[gettext]Country[/gettext]</strong><br>
                [if condition="country"]<img src="/images/icons/country/[c]country[/c].png" alt="[c]country[/c]">[/if]
                [if condition="country" not="true"]Unknown[/if]
            </p>
            <p><strong>[gettext]Website[/gettext]</strong><br>
                [if condition="editing"]<input name="website" type="text" value="[c]profile.website[/c]">[/if]
                [if condition="editing" not="true"][c]profile.website[/c][/if]
            </p>
        </div>
    </div>
    [if condition="editing"]
    </form>
    [/if]
    <div class="clear"></div>
    [if condition="comments"]
        <h2>Recent Comments</h2>
        [loop value="comment" iterable="comments" join="<hr>"]
            <h3><a href="[url controller="blog" action="view" category="[c]comment.post.category.slug[/c]" slug="[c]comment.post.slug[/c]" /]#comment-[c]comment.id[/c]">[c]comment.post.title[/c]</a> @ [call function="convertdate" date="[c]comment.posted[/c]" format="%m/%d/%y" /]</h3>
            <p>[transform function="converttext" parser="markdown"][c]comment.content[/c][/transform]</p>
        [/loop]
    [/if]
[/transform]
[/trim]