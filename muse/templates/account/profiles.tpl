[trim]
[assign var="title"]Users List[/assign]
[transform function="base"]
<h1>Users List</h1>
[if condition="profiles"]
    <ul>
    [loop value="profile" iterable="profiles"]
        <li><a href="[url current="true" id="[c]profile.id[/c]" /]">[c]profile.name[/c]</a></li>
    [/loop]
    </ul>
[/if]
[/transform]
[/trim]