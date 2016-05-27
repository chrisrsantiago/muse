[trim]
[assign var="title"][c]post.title[/c][/assign]
[if condition="post.summary"]
    [assign var="meta_description"][c]post.summary[/c][/assign]
[/if]

[transform function="base"]
    <h2>[c]post.title[/c]</h2>
    <div class="info">
        <span class="date">[gettext]Posted on[/gettext] <strong>[call function="convertdate" date="[c]post.posted[/c]" /]</strong></span>
        <span class="author"><a href="[url controller="account" action="profile" id="[c]post.user.id[/c]" /]">[c]post.user.name[/c]</a></span>
        <span class="comment"><a href="[c]post_url[/c]#comments">[c]post.comments_count[/c] [gettext]Comments[/gettext]</a></span>
        [if condition="post_canedit"]
            [if condition="editing_post" not="true"]
                <span class="edit"><a href="[url current="true" edit="true" /]">[gettext]Edit[/gettext]</a></span>
            [/if]
            [if condition="editing_post"]
                <span class="edit"><a href="[url current="true" edit="true" /]">[gettext]Edit[/gettext]</a></span>
            [/if]
        [/if]
    </div>

    <div class="text">
        [if condition="editing_post"]
        <form action="[url current="true" /]" method="post">
            [assign var="new_post" json="true"]false[/assign]
            [execute][template]post_form.tpl[/template][/execute]
        </form>
        [/if]
        [if condition="editing_post" not="true"]
            [transform function="converttext"][c]post.content[/c][/transform]
        [/if]
    </div>

    <h3 class="comments-header">[gettext]Their two-cents[/gettext]</h3>

    <div id="comments">
        [if condition="comments"]
            [loop value="comment" iterable="comments"]
                [assign var="comment_canedit" json="true"][call function="comment_canedit" user_id="[c]comment.user_id[/c]" /][/assign]
                [assign var="comment_editing" json="true"][call function="comment_editing" comment_id="[c]comment.id[/c]" /][/assign]

                [assign var="comment_editurl"]
                    [url controller="blog" action="view" category="[c]post.category.slug[/c]" slug="[c]post.slug[/c]" edit_comment="[c]comment.id[/c]" /]#comment-[c]comment.id[/c]
                [/assign]

                [assign var="comment_gravatar_hash"]
                    [if condition="comment.user"]
                        [if condition="comment.user.email"][c]comment.user.email[/c][/if]
                        [if condition="comment.user.email" not="true"][c]comment.user.ip[/c][/if]
                    [/if]
                [/assign]

                [assign var="comment_gravatar"]
                    [if condition="comment.user"]
                        [if condition="comment.user.email"]
                            [gravatar size="40"][c]comment.user.email[/c][/gravatar]
                        [/if]
                        [if condition="comment.user.email" not="true"]
                            [gravatar size="40"][c]comment.user.ip[/c][/gravatar]
                        [/if]
                    [/if]
                    [if condition="comment.user" not="true"][gravatar size="40"][c]comment.email[/c][/gravatar][/if]
                [/assign]

                [assign var="comment_user"]
                    [if condition="comment.user"]<a href="[url controller="account" action="profile" id="[c]comment.user.id[/c]" /]">[c]comment.user.name[/c]</a>[/if]
                    [if condition="comment.user" not="true"]
                        [if condition="comment.url"]<a href="[c]comment.url[/c]">[c]comment.name[/c]</a>[/if]
                        [if condition="comment.url" not="true"][c]comment.name[/c][/if]
                    [/if]
                [/assign]

                <div class="comment" id="comment-[c]comment.id[/c]">
                    <h4>[c entities="false"]comment_gravatar[/c][c entities="false"]comment_user[/c] [gettext]says:[/gettext]</h4>
                    <div class="contents">
                        [if condition="comment_editing"]
                        <form action="[c]comment_editurl[/c]" method="post">
                            [c entities="false"]csrf_token[/c]
                            <p><textarea name="comment">[c]comment.content[/c]</textarea></p>
                            <p><input type="submit" value="[gettext]Save Changes[/gettext]"></p>
                            <p><label for="delete"><input id="delete" name="delete" type="checkbox"> [gettext]Delete this comment?[/gettext]</label></p>
                        </form>
                        [/if]
                        [if condition="comment_editing" not="true"]
                        [transform function="converttext" parser="markdown"][c]comment.content[/c][/transform]
                        [/if]
                    </div>
                    <div class="posted">[gettext]Posted on[/gettext] <strong>[call function="convertdate" date="[c]comment.posted[/c]" /]</strong></div>
                    [if condition="comment_editing" not="true"]
                        [if condition="comment_canedit"]
                        <div class="options"><a href="[c]comment_editurl[/c]">[gettext]Edit/Delete[/gettext]</a></div>
                        [/if]
                    [/if]
                </div>
            [/loop]
        [/if]

        [if condition="editing_comment"]
            [return /]
        [/if]


        [if condition="comments" not="true"]
        <p class="nocomments">[gettext]There were no comments made for this post.  Be a leader and make one![/gettext]</p>
        [/if]

        
        [if condition="editing_post" not="true"]
            <h3 class="comments-header" id="respond">[gettext]Add Yours[/gettext]</h3>
            <form action="[c]post_url[/c]#respond" method="post">
                [c entities="false"]csrf_token[/c]
                [if condition="user.id"]
                    <p>[gettext]Current Alias:[/gettext] <strong>[c]user.name[/c]</strong></p>
                [/if]
                [if condition="user.id" not="true"]
                    <p><input type="text" name="name" id="name" size="22">
                        <label for="name" class="name">[gettext]Name[/gettext]</label></p>
                    <p><input type="text" name="url" id="url" value="" size="22">
                        <label for="url" class="url">[gettext]Website[/gettext]</label></p>
                    <p><input type="text" name="email" id="email" size="22">
                        <label for="email" class="email">[gettext]Email[/gettext]</label></p>
                [/if]
                <p><textarea name="comment" id="comment" rows="10" cols="60"></textarea></p>
                <p><input type="submit" name="comment_add" value="[gettext]Add Comment[/gettext]"></p>
            </form>
        [/if]
    </div>
[/transform]
[/trim]