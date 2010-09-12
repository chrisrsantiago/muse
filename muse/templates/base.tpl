[trim]
[assign var="blog_title"]That Faltzer Ain't One of Ours[/assign]
[assign var="blog_index"][url controller="blog" action="index" /][/assign]
[call function="breadcrumbs" /]
<!DOCTYPE HTML>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    [try]<meta name="description" content="[c]meta_description[/c]">[/try]

    <title>[c]title[/c] | [c]blog_title[/c]</title>
    <link rel="alternate" type="application/atom+xml" href="[url controller="blog" action="index" rss="true" /]">
    <link rel="stylesheet" type="text/css" href="/css/style.css">
</head>
<body>
    <div id="header">
        <div id="logo"></div>
        <div id="login">
            <div id="feed">
                <a href="[url controller="blog" action="index" rss="true" /]" title="[gettext]RSS Feed[/gettext]"><img src="/images/icons/rss.png" alt="[gettext]RSS Feed[/gettext]"></a>
            </div>
            [if condition="user.id" not="true"]
            <p><a href="[url controller="account" action="login" /]">[gettext]Login/Register[/gettext]</a></p>
            [/if]
            [if condition="user.id"]
                <p>[gettext]Hello,[/gettext] <a href="[url controller="account" action="profile" id="[c]user.id[/c]" /]">[c]user.name[/c]</a>. (<a href="[url controller="account" action="logout" /]">[gettext]Logout[/gettext]</a>)</p>
                [if condition="user.admin"]
                    <p><a href="[url controller="blog" action="new_post" /]">[gettext]New Post[/gettext]</a></p>
                [/if]
            [/if]
        </div>
        <div id="title"><a href="[c]blog_index[/c]">[c]blog_title[/c]</a></div>
        <div id="slogan">If wishes grew on trees, then life would be a breeze.</div>
    </div>
    <div id="menu">
    <ul>
        <li><a href="[url controller="blog" action="index" /]">[gettext]Home[/gettext]</a></li>
        <li><a href="[url controller="blog" action="view" category="sites" /]">[gettext]Sites[/gettext]</a>
            <ul>
                <li><a href="http://smbz.faltzershq.com/">Super Mario Bros. Z</a></li>
            </ul>
        </li>
        <li><a href="[url controller="blog" action="view" category="projects" /]">[gettext]Projects[/gettext]</a>
            <ul>
                <li><a href="http://mmbnonline.net/">mmbnonline</a></li>
                <li><a href="http://github.com/faltzer/muse">muse</a></li>
                <li><a href="http://github.com/faltzer/phanpy">phanpy</a></li>
                <li><a href="[url controller="blog" action="view" category="parasol-boards" /]">parasol boards</a></li>
                <li><a href="http://github.com/faltzer/suit-pylons">suit-pylons</a></li>
            </ul>
        </li>

        <li><a href="#">[gettext]Interesting[/gettext]</a>
            <ul>
                <li><a href="http://pseudoroid.blogspot.com/">Pseudoroid</a></li>
            </ul>
        </li>

        <li><a href="#">[gettext]Categories[/gettext]</a>
            <ul>
                [loop value="category" iterable="categories"]
                    <li><a href="[url controller="blog" action="view" category="[c]category.slug[/c]" /]">[c]category.title[/c]</a></li>
                [/loop]
            </ul>
        </li>
    </ul>
    </div>
    <div class="clear"></div>
    <div id="content">
        <form action="[url controller="blog" action="search" /]" method="get">
            <div id="search">
                <p><input name="terms" type="text" placeholder="[gettext]Search[/gettext]"[try] value="[c]terms[/c]"[/try]></p>
            </div>
        </form>
        <div id="breadcrumb">
            <p>[loop value="crumb" iterable="breadcrumbs" join=" &raquo; "]
               [if condition="crumb.url"]<a href="[c]crumb.url[/c]">[/if][c]crumb.title[/c][if condition="crumb.url"]</a>[/if]
            [/loop]</p>
        </div>
        [call function="flash_pop" /]
        [if condition="_flash"]
            <div id="message">
                <div id="heading">[gettext]Notices[/gettext]</div>
                <ul>
                [loop value="message" key="index" iterable="_flash"]
                    <li class="[c]message.category[/c]">[c]message[/c]</li>
                [/loop]
                </ul>
            </div>
        [/if]
        [c entities="false"]content[/c]
    </div>
    <div id="footer">
        <p>All content is &copy; 2006-2010 Chris Santiago. Unless otherwise specified, all content here is available under the <a href="http://creativecommons.org/licenses/by/3.0/us/">Creative Commons 3.0</a> license.<br>Icons by <a href="http://www.famfamfam.com/">famfamfam</a> &mdash; Powered by <a href="http://github.com/faltzer/muse">Muse</a>.</p>
        <p><a href="http://www.suitframework.com/slacks/?referrer=true" title="Debug this page with SLACKS"><img src="/stuff/slacks.png" alt="SLACKS"></a></p>
    </div>
</body>
</html>
[/trim]