# 附录 A. 处理 XML 元素的注意事项

## A.1. 空 XML 元素的注意事项

XML 支持两种表明 XML 元素中没有内容的机制. 第一种是声明一个形式为 `<A></A>` 的 XML 元素.
第二种是声明一个形式为 `<A/>` 的 XML 元素. 这两种 XML 元素在语义上是相同的.

## A.2. 非法 XML 处理的注意事项

XML 是一种具有弹性的数据格式, 可以轻松提交看似合法但实际上不合法的数据.
"在接受时保持灵活, 在发送时保持严格" 的哲学仍然适用, 但不应不合时宜地使用.
XML 在处理空格, 元素顺序, 插入新元素等方面非常灵活. 这种灵活性, 尤其在元素含义方面不需要扩展.

接受不合法的 XML 元素组合是没有好处的. 最好情况是产生不希望的结果, 最坏则可能会造成实际损害.

## A.3. 示例 - XML 语法错误

以下的 PROPFIND 方法请求正文是非法的.

```xml
<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:">
    <D:allprop/>
    <D:propname/>
</D:propfind>
```

propfind 元素的定义仅允许 allprop 或 propname 元素, 而不允许两者同时存在.
因此, 上述情况是错误的, 必须响应 400 (Bad Request).

然而, 想象一下, 如果服务器希望 "友好" 一些, 并决定选择 allprop 元素作对其进行响应.
如果服务器将命令视为 allprop, 那么在带宽受限的链路上运行的客户端打算执行 propname 操作时,
将会 "大吃一惊".

此外, 如果服务器教委宽松并决定回应此请求, 那么结果将因服务器而异,
一些服务器执行 allprop 指令, 而另一些执行 propname 指令. 这会降低而不是增加互操作性.

## A.4. 示例 - 意料外的 XML 元素

上一节的示例是非法的, 因为其同时包含了两个明确禁止同时出现在 propfind 元素中的元素.
然而, XML 是一种可扩展的语言, 因此可以想象为 propfind 定义新的元素.
下面是一个 PROPFIND 的请求正文, 与之前的示例一样, 如果服务器不理解 expired-props 元素,
必须拒绝并返回 400 (Bad Request).

```xml
<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:"
            xmlns:E="http://www.example.com/standards/props/">
    <E:expired-props/>
</D:propfind>
```

为了理解为什么会返回 400 (Bad Request),
让我们观察服务器在不了解 expired-props 的情况下如何看待请求正文.

```xml
<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:"
            xmlns:E="http://www.example.com/standards/props/">
</D:propfind>
```

由于服务器不理解 "expired-props" 元素,
根据在[第 17 章][SECTION#17]中指定的 WebDAV 特定 XML 处理规则,
其必须将请求处理为该元素不存在一样. 因此, 服务器看到一个空的 propfind,
这在 propfind 元素的定义中是非法的.

需要注意的是, 如果扩展是可扩展的, 其不一定会导致 400 (Bad Request).
例如, 想象一个用于 PROPFIND 的请求正文:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:"
            xmlns:E="http://www.example.com/standards/props/">
    <D:propname/>
    <E:leave-out>*boss*</E:leave-out>
</D:propfind>
```

上述示例包含了虚构的元素 leave-out. 该元素目的是阻止返回与提交的模式匹配的任何属性.
如果将上述示例提交给不了解 "leave-out" 的服务器, 唯一的结果将是 "leave-out" 元素被忽略,
然后 propname 被执行.

<!-- refs -->

[SECTION#17]: 17-xml_extensibility_in_dav.md
