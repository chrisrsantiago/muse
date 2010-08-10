[trim]
[call function="post" /]
[assign var="title"][c]post.title[/c][/assign]
[if condition="post.summary"]
    [assign var="meta_description"][c]post.summary[/c][/assign]
[/if]
[transform function="base"]
    <h2>[c]post.title[/c] </h2>
    <div class="info">
        <span class="date">[gettext]Posted on[/gettext] <strong>[c]post.posted[/c]</strong></span>
        <span class="author">[c]post.author.name[/c]</span>
        <span class="comment">[c]post.comments_count[/c] Comments</span>
    </div>

    <div class="text">
        [transform function="convert_text"][c]post.contents[/c][/transform]
    </div>

    <h3 class="comments-header">[gettext]Their two-cents[/gettext]</h3>

    <div id="comments">
        [if condition="comments"]
            [loop value="comment" iterable="comments"]
                [assign var="comment_gravatar"]
                    [if condition="comment.user"][gravatar size="40"][c]comment.user.email[/c][/gravatar][/if]
                    [if condition="comment.user" not="true"][gravatar size="40"][c]comment.email[/c][/gravatar][/if]
                [/assign]

                [assign var="comment_user"]
                    [if condition="comment.user"]<a href="[c]comment.user.identifier[/c]">[c]comment.user.name[/c]</a>[/if]
                    [if condition="comment.user" not="true"]
                        [if condition="comment.url"]<a href="[c]comment.url[/c]">[c]comment.name[/c]</a>[/if]
                        [if condition="comment.url" not="true"][c]comment.name[/c][/if]
                    [/if]
                [/assign]

                <div class="comment">
                    <h4>[c entities='false']comment_gravatar[/c][c entities='false']comment_user[/c] says:</h4>
                    <div class="contents">
                        [transform function="convert_text" parser="markdown"][c]comment.content[/c][/transform]
                    </div>
                    <div class="posted">Posted on <strong>[c]comment.posted[/c]</strong></div>
                </div>
            [/loop]
        [/if]
        [if condition="comments" not="true"]
            <p class="nocomments">[gettext]There were no comments made for this post.  Be a leader and make one![/gettext]</p>
        [/if]

        <h3 class="comments-header">[gettext]Add Yours[/gettext]</h3>
        [if condition="recaptcha_error"]
            <div class="error">[gettext]reCaptcha input invalid.[/gettext]</div>
        [/if]
        <form action="[url controller="blog" action="view" id="[c]post.slug[/c]" category="[c]post.category.slug[/c]" /]#respond" method="post">
            [assign var="comment_textbox"]<p><textarea name="comment" id="comment" rows="10" cols="60"></textarea></p>[/assign]
            [if condition="user.id"]
                <p>[gettext]Current Alias:[/gettext] <strong>[c]user.name[/c]</strong></p>
                [c entities="false"]comment_textbox[/c]
            [/if]
            [if condition="user.id" not="true"]
                <p><input type="text" name="name" id="name" size="22">
                    <label for="name" class="name">[gettext]Name[/gettext]</label></p>
                <p><input type="text" name="url" id="url" value="" size="22">
                    <label for="url" class="url">[gettext]Website[/gettext]</label></p>
                <p><input type="text" name="email" id="email" size="22">
                    <label for="email" class="email">[gettext]Email[/gettext]</label></p>
                <p class="openid-prompt"></p>
                [c entities="false"]comment_textbox[/c]
                [c entities="false"]recaptcha[/c]
            [/if]
            <p><input type="submit" name="comment_add" value="[gettext]Add Comment[/gettext]"></p>
        </form>
    </div>
[/transform]
[/trim]