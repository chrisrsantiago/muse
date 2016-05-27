[trim]
[assign var="title"][gettext]Login/Register[/gettext][/assign]
[transform function="base"]

<form action="[url current="true" /]" method="post">
    <p><input id="openid_identifier" name="openid_identifier" type="text">&nbsp;<input type="submit" value="[gettext]Login[/gettext]"></p>
</form>

<h2>[gettext]What is OpenID?[/gettext]</h2>
    <p>[gettext]OpenID is a decentralized login system that allows users to use already existing accounts to log-in to websites that support it. In comparison to separate registration systems, users do not have to enter or re-supply redundant information such as passwords, because this is all handled by the OpenID providers.[/gettext]</p>

    <p>[gettext]For more information, please visit the official OpenID website[/gettext] <a href="http://openid.net/get/">[gettext]getting an OpenID[/gettext]</a>.</p>
[/transform]
[/trim]