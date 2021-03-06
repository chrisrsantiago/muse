[c entities="false"]csrf_token[/c]

[if condition="new_post" not="true"]
<fieldset> 
    <legend>[gettext]Delete Post?[/gettext]</legend>
    <p>[gettext]Deleting a post will remove its contents and all comments made associated with it.  It cannot be undone, so think about it before selecting.[/gettext]</p> 
    <p><label for="delete"><input type="checkbox" id="delete" name="delete"> [gettext]I don't need to think twice; get rid of this post![/gettext]</label></p> 
</fieldset>
[/if]

<fieldset id="title">
    <legend>[gettext]Title[/gettext]</legend>
    <p>[gettext]Obviously, enter the title you want to give your blog post.[/gettext]</p>

    <p><input name="title" size="30" type="text"[if condition="new_post" not="true"] value="[c]post.title[/c]"[/if]></p>
</fieldset>

<fieldset id="category">
    <legend>[gettext]Category[/gettext]</legend>
    <p>[gettext]What category does this post fall under?  The default is,[/gettext] <strong>[c]category_default.title[/c]</strong>.</p>

    <p><select name="category_id">
        [loop value="category" iterable="categories"]
        [if condition="new_post"]
            [replace what='value="[c]category_default.id[/c]"' with='value="[c]category_default.id[/c]" selected="true"']<option value="[c]category.id[/c]">[c]category.title[/c]</option>[/replace]
        [/if]
        [if condition="new_post" not="true"]
            [replace what='value="[c]post.category.id[/c]"' with='value="[c]post.category.id[/c]" selected="true"']<option value="[c]category.id[/c]">[c]category.title[/c]</option>[/replace]
        [/if]
        [/loop]
    </select></p>
    <p>[gettext]If you want to create a category, type in its name and it will automatically be associated with your blog post.     Entering a category name overrides the already chosen default.[/gettext]</p>
    <p><input name="category_title" size="30" type="text" placeholder="[gettext]Category Name[/gettext]"></p>
</fieldset>

<fieldset id="slug">
    <legend>[gettext]Slug[/gettext]</legend>
    <p>[gettext]Specify a slug.  A slug is a URL friendly version by which to access this blog post.  If the slug was, <em>my-new-blog</em>, the URL, upon viewing of your blog post, would be <em>/category/my-new-blog</em>.[/gettext]</p>
    <p>[gettext]If no slug is specified, then it'll just take your title, convert any special characters into dashes, and set it to lowercase.[/gettext]</p>
    <p><input name="slug" size="30" type="text"[if condition="new_post" not="true"] value="[c]post.slug[/c]"[/if]></p>
</fieldset>

<fieldset id="summary">
    <legend>[gettext]Summary[/gettext]</legend>
    <p>[gettext]If you want to provide a preamble, do so here.  Try to keep it brief, as this is included in the metatags.[/gettext]</p>
    <p><textarea name="summary" class="summary">[if condition="new_post" not="true"][c]post.summary[/c][/if]</textarea></p>
</fieldset>

<fieldset id="story">
    <legend>[gettext]The Story[/gettext]</legend>
    <p>It's game time.  Break out that keyboard and start writing your story.</p>
    <p><textarea name="content" rows="10" cols="30">[if condition="new_post" not="true"][c]post.content[/c][/if]</textarea></p>
</fieldset>

<fieldset id="submit">
    <legend>[gettext]When you're ready...[/gettext]</legend>
    [if condition="new_post"]
        <p><input type="submit" value="[gettext]Create Post[/gettext]"></p>
    [/if]
    [if condition="new_post" not="true"]
        <p><input type="submit" value="[gettext]Update Post[/gettext]"></p>
    [/if]
</fieldset>