[trim]
[assign var="title"][gettext]What is OpenID?[/gettext][/assign]
[transform function="base"]

<h2>[gettext]What is OpenID?[/gettext]</h2>
    <p>[gettext]OpenID is a decentralized login system that allows users to use already existing accounts to log-in to websites that support it. In comparison to separate registration systems, users do not have to enter or re-supply redundant information such as passwords, because this is all handled by the OpenID providers.[/gettext]</p>

<h2>[gettext]Logging in with your OpenID[/gettext]</h2>

<form action="[url controller="account" action="login" /]" method="post" id="openid_form">	

    <div id="openid_choice">
        <p>[gettext]If you already know your OpenID URL, then you may type it in.[/gettext]</p>
        <div id="openid_btns"></div>
    </div>

    <div id="openid_input_area">
        <input id="openid_identifier" name="openid_identifier" type="text" value="http://">
        <input id="openid_submit" type="submit" value="[gettext]Sign-In[/gettext]">
        <input type="hidden" name="action" value="verify">
    </div>
    <noscript>
        <p>[gettext]For more information, please visit the official OpenID website[/gettext] <a href="http://openid.net/get/">[gettext]getting an OpenID[/gettext]</a>.</p>
    </noscript>
</form>
[/transform]
[/trim]