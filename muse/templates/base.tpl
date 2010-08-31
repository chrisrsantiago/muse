[trim]
<!DOCTYPE HTML>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    [try]<meta name="description" content="[c]meta_description[/c]">[/try]

    <title>[c]title[/c] | That Faltzer Ain't One of Ours</title>
    <link rel="alternate" type="application/atom+xml" href="[url controller="blog" action="index" rss="true" /]">
    <link href="http://fonts.googleapis.com/css?family=Molengo" rel="stylesheet" type="text/css">
    <link rel="stylesheet" type="text/css" href="/css/style.css">
</head>
<body>
    <div id="header">
        <div id="logo"></div>
        <div id="login">
            [if condition="user.id" not="true"]
            <p><a href="[url controller="account" action="login" /]">[gettext]Login/Register[/gettext]</a></p>
            [/if]
            [if condition="user.id"]
                <p>[gettext]Hello,[/gettext] [c]user.name[/c]. (<a href="[url controller="account" action="logout" /]">[gettext]Logout[/gettext]</a>)</p>
                [if condition="user.admin"]
                    <p><a href="[url controller="blog" action="new_post" /]">[gettext]New Post[/gettext]</a></p>
                    <p><a href="[url controller="blog" action="new_category" /]">[gettext]New Category[/gettext]</a></p>
                [/if]
            [/if]
        </div>
        <div id="title"><a href="[url controller="blog" action="index" /]">That Faltzer Ain't One of Ours</a></div>
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
                <li><a href="http://mmbnonline.net/">MMBN Online</a></li>
                <li><a href="[url controller="blog" action="view" category="parasol-boards" /]">Parasol Boards</a></li>
                <li><a href="http://suitframework.com/">SUIT</a></li>
                <li><a href="http://pypi.python.org/pypi/suit-pylons/1.0.0">SUIT for Pylons</a></li>
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
        [c entities="false"]content[/c]
    </div>
    <div id="footer">
        <p>[gettext]All content is &copy; 2006-2010 Chris Santiago. Unless otherwise specified, all of the content here is available under the <a href="http://creativecommons.org/licenses/by/3.0/us/">Creative Commons 3.0</a> license.  <a href="http://github.com/faltzer/muse">Get the source for this website</a>.[/gettext]</p>
        <p><a href="http://www.suitframework.com/" title="FHQ uses SUIT for templating."><img src="/stuff/suit.png" alt="SLACKS"></a>&nbsp;<a href="http://www.suitframework.com/slacks/?referrer=true" title="Debug this page with SLACKS"><img src="/stuff/slacks.png" alt="SLACKS"></a></p>
    </div>
</body>
</html>
[/trim]