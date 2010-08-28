    [assign var="row" json="true"]
        [if condition="row"]0[/if]
        [if condition="row" not="true"]1[/if]
    [/assign]
    <div class="entries row[c]row[/c]">
        <h2><a href="[url controller="blog" action="view" category="[c]post.category.slug[/c]" id="[c]post.slug[/c]" /]">[c]post.title[/c]</a> ([c]post.comments_count[/c])</h2>
            <p class="summary">
                [if condition="post.summary"]
                    [c]post.summary[/c]
                [/if]
            </p>
            <p class="posted">Posted on [call function="convertdate" date="[c]post.posted[/c]" /]</p>
    </div>