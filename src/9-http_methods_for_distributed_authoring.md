# 9. 用于分布式创作的 HTTP 方法

## 9.1. PROPFIND 方法

PROPFIND 方法用于检索在由请求 URI (Request-URI) 标识资源上定义的属性:

- 如果该资源没有任何内部成员, 则返回该资源上定义的属性;
- 如果该资源是一个集合并具有内部成员 URL, 则返回由请求 URI 标识资源及其可能的成员资源的属性.

所有符合 DAV 标准的资源都必须支持 PROPFIND 方法和 `propfind` XML 元素
([第 14.20 章][SECTION#14.20]) 以及与 `propfind` 元素一起使用的所有 XML 元素.

客户端在 PROPFIND 请求中必须提交一个值可以是 "0"、"1" 或者 "infinity" 的 Depth 标头.
服务器必须**支持[MUST]**符合 WebDAV 的资源的 "0" 和 "1" 深度的请求，
并**应该[SHOULD]**支持 "infinity" 请求. 实际上，由于与此行为相关的性能和安全问题,
对于无限深度 (infinite-depth) 请求的支持**可能[MAY]**被禁用.
服务器**应该[SHOULD]**将没有 Depth 标头的请求视为包含了 `"Depth: infinity"` 标头.

客户端可以在请求方法正文中提交 "propfind" XML 元素, 描述正在请求的信息. 这可能会:

- 通过在 "prop" 元素内命名想要的属性来请求特定的属性值
  (服务器**可能[MAY]**忽略这里的属性排序).
- 使用 "allprop" 元素请求在此规范中(最小)定义的属性以及死属性的属性值 ("include"
  元素可以与 "allprop" 一起使用, 用来指示服务器 (包括在其他情况下可能不会)
  返回的附加活属性).
- 使用 "propname" 元素请求资源上所有定义属性的名称列表.

> 译者注: 有些属性可能是动态生成的 (比如我们假设有一个服务器实时计算的 `custom-size`
> 属性), 正常请求属性时可能不会返回, 而使用 "include" 与 "allprop" 元素则可以返回.
>
> ```xml
> # 1. 正常的 PROPFIND 请求
> PROPFIND /file.txt HTTP/1.1
> Host: example.com
> Depth: 0
> Content-Type: text/xml; charset="utf-8"
>
> <?xml version="1.0" encoding="utf-8"?>
> <D:propfind xmlns:D="DAV:">
>   <D:prop>
>     <D:getetag />
>     <D:getlastmodified />
>     <D:custom-size />
>   </D:prop>
> </D:propfind>
>
> # 响应
> HTTP/1.1 207 Multi-Status
> Content-Type: text/xml; charset="utf-8"
>
> <?xml version="1.0" encoding="utf-8"?>
> <D:multistatus xmlns:D="DAV:">
>   <D:response>
>     <D:href>/file.txt</D:href>
>     <D:propstat>
>       <D:prop>
>         <D:getetag>"123456789"</D:getetag>
>         <D:getlastmodified>Tue, 10 Aug 2023 14:30:00 GMT</D:getlastmodified>
>         <!-- 'custom-size' 不会包含在响应体的xml中 -->
>       </D:prop>
>       <D:status>HTTP/1.1 200 OK</D:status>
>     </D:propstat>
>   </D:response>
> </D:multistatus>
> ```
>
> ```xml
> # 2. 使用包含 `include` 与 `allprops` 元素的 PROPFIND 请求
> PROPFIND /file.txt HTTP/1.1
> Host: example.com
> Depth: 0
> Content-Type: text/xml; charset="utf-8"
>
> <?xml version="1.0" encoding="utf-8"?>
> <D:propfind xmlns:D="DAV:">
>   <D:prop>
>     <D:include>
>       <D:allprop />
>     </D:include>
>   </D:prop>
> </D:propfind>
>
> # 响应
> HTTP/1.1 207 Multi-Status
> Content-Type: text/xml; charset="utf-8"
>
> <?xml version="1.0" encoding="utf-8"?>
> <D:multistatus xmlns:D="DAV:">
>   <D:response>
>     <D:href>/file.txt</D:href>
>     <D:propstat>
>       <D:prop>
>         <D:getetag>"123456789"</D:getetag>
>         <D:getlastmodified>Tue, 10 Aug 2023 14:30:00 GMT</D:getlastmodified>
>         <D:custom-size>1024</D:custom-size>
>       </D:prop>
>       <D:status>HTTP/1.1 200 OK</D:status>
>     </D:propstat>
>   </D:response>
> </D:multistatus>
> ```

客户端可以选择不提交请求正文. 一个空的 PROPFIND 请求正文必须被视为 "allprop" 请求.

> 译者注: 补充一个简单的例子
>
> ```xml
> # 一个空的 PROPFIND 请求
> PROPFIND /file.txt HTTP/1.1
> Host: example.com
> Depth: 0
> Content-Type: text/xml; charset="utf-8"
>
> <?xml version="1.0" encoding="utf-8"?>
> <D:propfind xmlns:D="DAV:">
>   <D:prop />
> </D:propfind>
>
> # 等价
> PROPFIND /file.txt HTTP/1.1
> Host: example.com
> Depth: 0
> Content-Type: text/xml; charset="utf-8"
>
> <?xml version="1.0" encoding="utf-8"?>
> <D:propfind xmlns:D="DAV:">
>   <D:prop>
>     <D:allprop />
>   </D:prop>
> </D:propfind>
> ```

请注意, "allprop" 并不返回所有活属性的值. 如今 WebDAV
服务器存在越来越多地具有高昂计算成本或冗长的属性 (参见 [RFC3253] 和 [RFC3744]),
所以并不会返回所有属性. 相反, WebDAV 客户端可以使用 "propname" 来请求并发现存在哪些活属性,
并在需要检索值时请求特定的属性. 对于在其他地方定义的活属性，该定义
(_译者注: 指服务器可能不会返回所有的属性_) 可以指定是否会在 "allprop" 请求中返回该活属性.

所有服务器必须支持返回内容类型为 `text/xml` 或 `application/xml` 的响应,
其中包含一个描述检索各种属性尝试结果的 "multistatus" XML 元素。

如果在检索属性时出现错误, 那么响应中**必须[MUST]**包含适当的错误结果.
对于尝试检索不存在的属性的请求是一种错误,
且必须使用包含 404 (Not Found) 状态值的 "response" XML 元素进行记录.

最后, 集合资源的 "multistatus" XML 元素在任何深度的请求中**必须[MUST]**为集合的每个成员
URL 包含一个 "response" XML 元素. 其**不应该[SHOULD_NOT]**包含任何不符合 WebDAV
标准的资源的 "response" 元素.
每个 "response" 元素必须包含一个有 "prop" XML 元素中定义属性资源的 URL 的 "href" 元素.
集合资源的 PROPFIND 结果将以一个扁平列表 (flat list) 返回，其中条目的顺序并不重要.
需要注意的是，资源对于给定名称的属性可能只有一个值,
因此该属性可能仅在 PROPFIND 响应中出现一次.

属性可能受到访问控制的限制. 一种情况是在 "allprop" 和 "propname" 请求下, 如果一个主体
(principal) 没有权限知道特定属性是否存在, 那么该属性**可能[MAY]**会在响应中被静默排除.

一些 PROPFIND 结果可能会被缓存, 但需要小心, 因为大多数属性没有缓存验证机制.
PROPFIND 方法是既安全又幂等的 (参见 [RFC2616#9.1]).

### 9.1.1. PROPFIND 响应码

这章与与其他方法的类似部分一样, 提供了关于错误代码和一些可能在 PROPFIND
中特别有用的前置或后置条件 (在[第 16 章][SECTION#16]中定义) 的指导建议.

403 Forbidden - 服务器**可能[MAY]**会拒绝具有 "Infinity" 深度标头集合上的 PROPFIND
请求. 在这种情况下, 服务器应使用这个错误, 并在错误主体中使用前置条件代码
`"propfind-finite-depth"`.

### 9.1.2. 用于 "propstat" 元素的状态码

在 PROPFIND 响应中,
有关各个属性的信息返回在 "propstat" 元素内 (详见[第 14.22 章][SECTION#14.22]),
每个 "propstat" 元素包含一个 "status" 元素,
每个 "status" 元素都包含关于出现在该元素中属性的信息.
下述列表总结了在 "propstat" 内最常用的状态码;
同时客户端应该能随时应对并处理其他 2/3/4/5xx 系列的状态码.

- 200 (OK): 属性存在，且/或其值成功返回.
- 401 (Unauthorized): 属性未经适当授权无法查看.
- 403 (Forbidden): 属性不论授权与否, 都无法查看.
- 404 (Not Found): 属性不存在.

### 9.1.3. 示例 - 检索命名属性

```xml
>>Request

PROPFIND /file HTTP/1.1
Host: www.example.com
Content-type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:">
    <D:prop xmlns:R="http://ns.example.com/boxschema/">
        <R:bigbox/>
        <R:author/>
        <R:DingALing/>
        <R:Random/>
    </D:prop>
</D:propfind>


>>Response

HTTP/1.1 207 Multi-Status
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:multistatus xmlns:D="DAV:">
    <D:response xmlns:R="http://ns.example.com/boxschema/">
        <D:href>http://www.example.com/file</D:href>
        <!-- propstat 1 -->
        <D:propstat>
            <D:prop>
                <R:bigbox>
                <R:BoxType>Box type A</R:BoxType>
                </R:bigbox>
                <R:author>
                <R:Name>J.J. Johnson</R:Name>
                </R:author>
            </D:prop>
            <D:status>HTTP/1.1 200 OK</D:status>
        </D:propstat>

        <!-- propstat 2 -->
        <D:propstat>
            <D:prop>
                <R:DingALing/>
                <R:Random/>
            </D:prop>
            <D:status>HTTP/1.1 403 Forbidden</D:status>
            <D:responsedescription> The user does not have access to the
DingALing property.
            </D:responsedescription>
        </D:propstat>
    </D:response>

    <D:responsedescription> There has been an access violation error.
    </D:responsedescription>
</D:multistatus>
```

在这个例子中, PROPFIND 执行在一个非集合资源 `http://www.example.com/file` 上.
"propfind" XML 元素指定了正在请求的四个属性的名称. 在这个例子中, 只返回了两个属性，
因为发出请求的正文没有足够的访问权限查看后两个个属性.

### 9.1.4. 示例 - 使用 "propname" 检索所有属性名的

```xml
>>Request

PROPFIND /container/ HTTP/1.1
Host: www.example.com
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<propfind xmlns="DAV:">
    <propname/>
</propfind>


>>Response

HTTP/1.1 207 Multi-Status
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<!-- default namespace: "DAV:" -->
<multistatus xmlns="DAV:">
    <response>
        <href>http://www.example.com/container/</href>
        <propstat>
            <!-- XML namespace scoping -->
            <prop xmlns:R="http://ns.example.com/boxschema/">
                <R:bigbox/>
                <R:author/>
                <creationdate/>
                <displayname/>
                <resourcetype/>
                <supportedlock/>
            </prop>
            <status>HTTP/1.1 200 OK</status>
        </propstat>
    </response>
    <response>
        <href>http://www.example.com/container/front.html</href>
        <propstat>
            <!-- XML namespace scoping -->
            <prop xmlns:R="http://ns.example.com/boxschema/">
                <R:bigbox/>
                <creationdate/>
                <displayname/>
                <getcontentlength/>
                <getcontenttype/>
                <getetag/>
                <getlastmodified/>
                <resourcetype/>
                <supportedlock/>
            </prop>
            <status>HTTP/1.1 200 OK</status>
        </propstat>
    </response>
</multistatus>
```

在这个例子中, PROPFIND 在集合资源 `"http://www.example.com/container/"` 上调用,
"propfind" XML 元素包含 "propname" XML 元素, 表示应该返回所有属性的名称.
由于没有出现 Depth 标头，服务器假设其默认值为 "infinity",
意味着服务器应该返回集合及其所有后代的属性名.

与前面的例子一样, 在资源 `"http://www.example.com/container/"` 定义了六属性:

- `bigbox` 和 `author` 在命名空间 `"http://ns.example.com/boxschema/"` 中定义;
- `creationdate`, `displayname`, `resourcetype` 和 `supportedlock` 在 "DAV:"
  命名空间中定义.

资源 `"http://www.example.com/container/index.html"` 是集合 `container`
上的一个成员, 里面定义了九个属性:

- `bigbox` 在命名空间 `"http://ns.example.com/boxschema/"` 中定义;
- `creationdate`, `displayname`, `getcontentlength`, `getcontenttype`,
  `getetag`, `getlastmodified`, `resourcetype` 和 `supportedlock` 在 "DAV:"
  命名空间中定义.

这个例子还演示了 XML 命名空间作用域 (XML namespace scoping) 和默认命名空间
(default namespace) 的使用方式. 由于 "xmlns" 属性没有包含前缀,
命名空间默认应用于所有包含的元素.
因此, 所有没有明确声明所属命名空间的元素都是 "DAV:" 命名空间的成员.

### 9.1.5. 示例 - 使用所谓的 "allprop"

需要注意的是, 尽管 "allprop" 的名字保持了向后兼容性, 但其并不返回所有属性,
而只返回死属性和在此规范中定义的活属性. (_译者注: 规范定义的属性在[第 15 章][SECTION#15]_)

```xml
>>Request

PROPFIND /container/ HTTP/1.1
Host: www.example.com
Depth: 1
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:">
    <D:allprop/>
</D:propfind>

>>Response

HTTP/1.1 207 Multi-Status
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:multistatus xmlns:D="DAV:">
    <D:response>
        <D:href>/container/</D:href>
        <D:propstat>
            <D:prop xmlns:R="http://ns.example.com/boxschema/">
                <R:bigbox><R:BoxType>Box type A</R:BoxType></R:bigbox>
                <R:author><R:Name>Hadrian</R:Name></R:author>
                <!-- WebDAV 特有 -->
                <D:creationdate>1997-12-01T17:42:21-08:00</D:creationdate>
                <D:displayname>Example collection</D:displayname>
                <D:resourcetype><D:collection/></D:resourcetype>
                <D:supportedlock>
                    <D:lockentry>
                        <D:lockscope><D:exclusive/></D:lockscope>
                        <D:locktype><D:write/></D:locktype>
                    </D:lockentry>
                    <D:lockentry>
                        <D:lockscope><D:shared/></D:lockscope>
                        <D:locktype><D:write/></D:locktype>
                    </D:lockentry>
                </D:supportedlock>
            </D:prop>
            <D:status>HTTP/1.1 200 OK</D:status>
        </D:propstat>
    </D:response>

    <D:response>
        <D:href>/container/front.html</D:href>
        <D:propstat>
            <D:prop xmlns:R="http://ns.example.com/boxschema/">
                <R:bigbox><R:BoxType>Box type B</R:BoxType></R:bigbox>
                <D:creationdate>1997-12-01T18:27:21-08:00</D:creationdate>
                <D:displayname>Example HTML resource</D:displayname>
                <D:getcontentlength>4525</D:getcontentlength>
                <D:getcontenttype>text/html</D:getcontenttype>
                <D:getetag>"zzyzx"</D:getetag>
                <D:getlastmodified
                >Mon, 12 Jan 1998 09:25:56 GMT</D:getlastmodified>
                <D:resourcetype/>
                <D:supportedlock>
                    <D:lockentry>
                        <D:lockscope><D:exclusive/></D:lockscope>
                        <D:locktype><D:write/></D:locktype>
                    </D:lockentry>
                    <D:lockentry>
                        <D:lockscope><D:shared/></D:lockscope>
                        <D:locktype><D:write/></D:locktype>
                    </D:lockentry>
                </D:supportedlock>
            </D:prop>
            <D:status>HTTP/1.1 200 OK</D:status>
        </D:propstat>
    </D:response>
</D:multistatus>
```

在这个例子中, PROPFIND 在集合资源 `"http://www.example.com/container/"`
上使用一个深度为 1 的标头进行调用, 该请求适用于资源及其子资源,
并且 "propfind" XML 元素包含 "allprop" XML 元素.
该请求表示应该返回在资源上定义的所有死属性的名称和值,
以及在本规范中定义的所有活属性的名称和值. 这个例子还演示了响应中 "href" 元素相对引用的使用.

资源 `"http://www.example.com/container/"` 上定义了六个属性:

- `bigbox` 和 `author` 属于命名空间 `"http://ns.example.com/boxschema/"`
- `creationdate`, `displayname`, `resourcetype` 和 `supportedlock` 在 `DAV:`
  上定义.

最后四个属性是 WebDAV 特有的的, 定义在[第 15 章][SECTION#15]. 由于此资源不支持 GET 请求,
因此 "get" 属性（e.g., DAV:getcontentlength）没有定义在此资源上.

在上面的 xml 实例中, "container" 容器拥有如下 WebDAV 特有的属性断言:

- 在 1997/12/01 5:42:21PM GMT-8 创建的 (`DAV:creationdate`),
- 名称为 "Example collection" (`DAV:displayname`),
- 是一个集合资源类型 (`DAV:resourcetype`),
- 支持互斥写锁和共享写锁 (`DAV:supportedlock`).

资源 `"http://www.example.com/container/front.html"` 上定义了九个属性:

- `bigbox` 属于命名空间 `"http://ns.example.com/boxschema/"` (另一个 "bigbox"
  属性类型的实例 (区别于资源 `"http://www.example.com/container/"` 中的属性定义))
- `DAV:creationdate`, `DAV:displayname`, `DAV:getcontentlength`,
  `DAV:getcontenttype`, `DAV:getetag`, `DAV:getlastmodified`,
  `DAV:resourcetype` 和 `DAV:supportedlock`.

在上面的 xml 示例中, "front.html" 器拥有如下 WebDAV 特有的属性断言:

- 在 1997/12/01 6:27:21PM GMT-8 创建的 (`DAV:creationdate`),
- 名称为 "Example HTML resource" (`DAV:displayname`),
- 内容长度为 4525 字节 (`DAV:getcontentlength`),
- MIME 类型为 "text/html" (`DAV:getcontenttype`),
- 实体标记为 "zzyzx" (`DAV:getetag`).
- 在 1998/01/12 09:25:56AM GMT 进行最后修改 (`DAV:getlastmodified`),
- 该属性具有空的资源类型, 意味其不是一个集合 (`DAV:resourcetype`),
- 支持互斥写锁和共享写锁 (`DAV:supportedlock`).

### 9.1.6. 示例 - 使用 "allprop" 与 "include"

```xml
>>Request

PROPFIND /mycol/ HTTP/1.1
Host: www.example.com
Depth: 1
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:">
    <D:allprop/>
    <D:include>
        <D:supported-live-property-set/>
        <D:supported-report-set/>
    </D:include>
</D:propfind>
```

在这个示例中, PROPFIND 在资源 `"http://www.example.com/mycol/"`
及其内部成员资源上调用. 客户端请求获取在本规范中定义的所有活属性与死属性的值,
加上两个在 [RFC3253] 中额外定义的活属性. 该消息响应没有在示例中显示.

### 9.2. PROPPATCH 方法

PROPPATCH 方法处理在请求正文中的指定指令, 用于设置和/或移除由请求 URI 标识资源上定义的属性.

所有符合 DAV 标准的资源都**必须[MUST]**支持 PROPPATCH
方法并且**必须[MUST]**处理那些使用 "propertyupdate", "set" 和 "remove" XML
元素指定的指令. 此方法中指令的执行显然会受访问控制约束.
符合 DAV 标准的资源**应该[SHOULD]**支持设置任意死属性.

PROPPATCH 方法的请求消息正文**必须[MUST]**包含 "ropertyupdate" XML 元素.

服务器**必须[MUST]**按照文档顺序 (document order) 处理 PROPPATCH 指令
(例外与正常规则的是, 顺序是无关紧要的). 指令**必须[MUST]**全部执行或全部不执行。
因此, 如果在处理过程中发生任何错误,
服务器则**必须[MUST]**撤消所有已执行指令并返回适当的错误结果.
指令处理的详细信息可以在[第 14.23 章][SECTION#14.23]和[第 14.26 章][SECTION#14.26]中关于
`set` 和 `remove` 指令的定义里找到.

如果服务器尝试在 PROPPATCH 请求中修改任意属性 (i.e., 在处理正文前请求不会因高级错误被拒绝),
响应必须是一个多状态响应, 如[第 9.2.1 章][SECTION#9.2.1]中所述.

该方法幂等但不安全 (请参阅 [RFC2616#9.1]). 不能缓存此方法的响应.

### 9.2.1. "propstat" 元素中使用的状态代码

在 PROPPATCH 响应中, 单个属性的信息被包含在 "propstat" 元素内
(参见[第 14.22 章][SECTION#14.22]), 每个 "propstat" 元素都包含一个 "status" 元素,
其中包含出现的相关属性信息. 下面列出了 "propstat" 内部最常用的状态代码;
同时客户端应该能随时应对并处理其他 2/3/4/5xx 系列的状态码.

- 200 (OK)：属性设置或修改成功. 需要注意的是, 由于 PROPPATCH 的原子性,
  如果某个属性的状态为 200, 那么响应中的每个属性的状态是 200.

- 403 (Forbidden): 由于一个服务器选择不明确的原因, 客户端无法修改其中一个属性.

- 403 (Forbidden): 客户端尝试设置如 `DAV:getetag` 这种受保护的属性. 如果返回此错误,
  服务器应该在响应正文中使用 "cannot-modify-protected-property" 前置条件码.

- 409 (Conflict): 客户端提供了一个语义不符合该属性的值.

- 424 (Failed Dependency): 由于其他某个属性修改失败, 无法修改当前属性.

- 507 (Insufficient Storage): 服务器没有足够的空间记录属性.

### 9.2.2. 示例 - PROPPATCH

```xml
>>Request

PROPPATCH /bar.html HTTP/1.1
Host: www.example.com
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:propertyupdate xmlns:D="DAV:"
        xmlns:Z="http://ns.example.com/standards/z39.50/">
    <D:set>
        <D:prop>
            <Z:Authors>
                <Z:Author>Jim Whitehead</Z:Author>
                <Z:Author>Roy Fielding</Z:Author>
            </Z:Authors>
        </D:prop>
    </D:set>
    <D:remove>
        <D:prop>
            <Z:Copyright-Owner/>
        </D:prop>
    </D:remove>
</D:propertyupdate>

>>Response

HTTP/1.1 207 Multi-Status
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:multistatus xmlns:D="DAV:"
        xmlns:Z="http://ns.example.com/standards/z39.50/">
    <D:response>
        <D:href>http://www.example.com/bar.html</D:href>
        <D:propstat>
            <D:prop><Z:Authors/></D:prop>
            <D:status>HTTP/1.1 424 Failed Dependency</D:status>
        </D:propstat>
        <D:propstat>
            <D:prop><Z:Copyright-Owner/></D:prop>
            <D:status>HTTP/1.1 409 Conflict</D:status>
        </D:propstat>
        <D:responsedescription> Copyright Owner cannot be deleted or
        altered.</D:responsedescription>
    </D:response>
</D:multistatus>
```

在该示例中, 客户端请求服务器设置 `"http://ns.example.com/standards/z39.50/"`
命名空间中的 "Authors" 属性的值，并删除同一命名空间中的 "Copyright-Owner" 属性.
由于 "Copyright-Owner" 属性无法被移除, 因此没有修改任何属性. 对于 "Authors" 属性,
状态码 424 (Failed Dependency) 表示, 这个操作如果不是因为与移除 "Copyright-Owner"
属性冲突的话应该可以成功.

## 9.3. MKCOL 方法

MKCOL 方法在由 Request-URI 指定的位置创建一个新的集合资源. 如果 Request-URI
已经映射到一个资源, 那么 MKCOL 方法**必须[MUST]**失败. 在 MKCOL 处理过程中,
服务器**必须[MUST]**将 Request-URI 设置为其父集合的内部成员, 除非这个 Request-URI
是 "/". 如果不存在这样的祖先, 该方法**必须[MUST]**失败. 当 MKCOL 操作创建一个新的集合资源时,
所有的祖先集合**必须[MUST]**已经存在, 否则方法必须失败并返回 409 (Conflict) 状态码.
e.g., 如果发出一个请求创建集合 `/a/b/c/d/`, 而 `/a/b/c/` 不存在, 那么该请求必须失败.

当在没有请求正文的情况下调用 MKCOL 时, 新创建的集合**应该[SHOULD]**没有成员.

MKCOL 请求消息可能包含一个消息体. 当消息体存在时, MKCOL 请求的精确行为是未定义的,
但这一情况仅限制于创建集合/集合的成员/成员正文/集合或成员的属性时.
如果服务器收到一种不支持或不理解的 MKCOL 请求实体类型, 必须响应 415 (Unsupported Media
Type) 状态码. 如果服务器决定基于实体存在或实体类型拒绝请求, 则应该响应 415 (Unsupported
Media Type) 状态码.

该方法幂等但不安全 (请参阅 [RFC2616#9.1]). 不能缓存此方法的响应.

### 9.3.1. MKCOL 响应码

除了可能的一般状态码外, 以下状态码对于 MKCOL 方法具有特定的适用性:

- 201 (Created): 集合已创建
- 403 (Forbidden): 这表示至少有存在两种情况之一:
  1. 服务器不允许在给定的 URL 命名空间位置创建集合.
  2. Request-URI 的父集合存在, 但无法接受成员.
- 405 (Method Not Allowed): MKCOL 只能在未映射的 URL 上执行.
- 409 (Conflict): 在 Request-URI 处创建集合前, 必须先创建一个或多个中间集合.
  服务器**不能[MUST_NOT]**自动创建这些中间集合.
- 415 (Unsupported Media Type): 服务器不支持的请求体类型
  (尽管在 MKCOL 请求中可以使用请求正文 (bodies on requests)，
  但由于本规范没有定义任何请求正文类型, 因此服务器可能不会支持任何给定的请求正文类型).
- 507 (Insufficient Storage): 该资源没有足够的空间来记录执行此方法后资源状态.

### 9.3.2. 示例 - MKCOL

此示例在 `www.example.com` 服务器中创建了一个 `/webdisc/xfiles/` 集合.

```http
>>Request

MKCOL /webdisc/xfiles/ HTTP/1.1
Host: www.example.com


>>Response

HTTP/1.1 201 Created
```

## 9.4. 集合中的 GET 和 HEAD

HTTP 方法 GET 的语义在集合(目录)资源中并没有改变.
GET 方法被定义为 "检索由请求 URI 标识的任何信息 (以实体的形式)" [RFC2616].
当应用于集合时, GET 方法可能会返回 "index.html" 资源的内容，
其中包含人类可读的集合内容, 或者其他一些内容.
因此, GET 在集合上的结果可能与集合的成员关系之间没有任何相关性.

类似地, 由于 HEAD 方法的定义是一个没有响应消息正文的 GET,
HEAD 方法的语义在应用于集合资源时也没有改变.

## 9.5. 集合中的 POST

根据定义, POST 方法执行的实际功能由服务器决定, 且通常取决于特定的资源.
因为 POST 方法的行为在很大程度上是未定义的, 所以无法有意义的修改该方法应用于集合时的行为.
因此, POST 方法在应用于集合时其语义保持不变.

## 9.6. DELETE 要求

DELETE 方法在 [RFC2616#9.7] 中被定义为 "删除由 Request-URI 标识的资源".
然而, WebDAV 修改了一些 DELETE 处理要求.

一个服务器在成功处理一个 DELETE 请求时:

- **必须[MUST]**销毁根据已删除的资源设置的锁.
- **必须[MUST]**移除从 Request-URI 到任何资源的映射.

因此，在成功进行 DELETE 操作之后 (并且没有其他操作的情况下),
对目标 Request-URI 的后续 GET/HEAD/PROPFIND 请求必须返回 404（Not Found）状态.

### 9.6.1. 集合中的 DELETE

DELETE 方法对集合的行为**必须[MUST]**如同在请求上使用 "Depth: infinity" 标头一样.
客户端在对集合进行 DELETE 操作时,
**不得[MUST_NOT]**提交带有除了 infinity 之外的任何值的 Depth 标头.

DELETE 指示删除 Request-URI 中指定的集合以及其内部成员 URL 标识的所有资源.

如果任何由成员 URL 标识的资源无法被删除, 那么所有的成员祖先都**不得[MUST_NOT]**被删除,
以维护 URL 命名空间的一致性.

DELETE 中包含的任何标头**必须** (MUST) 应用于处理要删除的每个资源.

> 译者注: 怎么理解这句话, 假设发送了一个 DELETE 请求
>
> ```http
> DELETE /files/file.txt HTTP/1.1
> Host: example.com
> Authorization: Bearer your-access-token
> X-Custom-Header: SomeValue
> ```
>
> 服务器在处理上面请求时, 需要处理标头中的所有信息, 比如存在 `Authorization`,
> 表示需要验证访问令牌.

当 DELETE 方法完成处理时, 结果**必须** (MUST) 在一个一致的 URL 命名空间内.

如果在删除成员资源 (与 Request-URI 标识的资源不同的资源) 时出现错误, 响应可以是 207 (Multi-Status).
Multi-Status 用来指示哪些内部资源无法删除, 包括错误代码,
这将帮助客户端理解哪些资源导致请求失败.
e.g., 如果内部资源被锁定, Multi-Status 正文可以包括一个状态为 423（Locked）的响应.

如果请求完全失败, 服务器可以返回 4xx 状态响应, 而不是 207.

DELETE 方法中, 207（Multi-Status）响应中**不应[SHOULD_NOT]**包含 424 (Failed
Dependency) 状态码. 当客户端为祖先的后代收到错误时, 客户端会知道祖先资源无法被删除,
因此该状态码可以被安全地省略.
此外, 207（Multi-Status）中**不应[SHOULD_NOT]**返回 204（No Content）错误.
被禁止的原因是 204（No Content）是默认的成功代码.

### 9.6.2. 示例 - DELETE

```xml
>>Request

DELETE  /container/ HTTP/1.1
Host: www.example.com

>>Response

HTTP/1.1 207 Multi-Status
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<d:multistatus xmlns:d="DAV:">
    <d:response>
        <d:href>http://www.example.com/container/resource3</d:href>
        <d:status>HTTP/1.1 423 Locked</d:status>
        <d:error>
            <d:lock-token-submitted/>
        </d:error>
    </d:response>
</d:multistatus>
```

在这个例子中, 由于 `"http://www.example.com/container/resource3"`
被锁定且没有锁令牌与请求一起提交, 尝试删除该资源会失败.
由此可知, 尝试删除 `"http://www.example.com/container/"` 也会失败.
因此, 客户端知道尝试删除 `"http://www.example.com/container/"` 也必然会失败,
因为除非子项也被删除，否则父项不能被删除. 由于方法是在一个集合上, 即使没有包含 Depth 标头,
也会假设其深度为 infinity.

## 9.7. PUT 要求

### 9.7.1. 非集合资源中的 PUT

对现有资源执行的 PUT 操作将替换该资源的 GET 响应实体.
在 PUT 处理过程中, 可能会重新计算在资源上定义的属性, 但其他属性不会受到影响.
e.g., 如果服务器识别到请求正文的内容类型, 其可能能够自动提取并作为属性进行有益地展示.

如果 PUT 导致创建一个资源, 而该资源没有适当作用域的父集时,
这个操作**必须[MUST]**失败并返回 409 (Conflict) 状态码.

PUT 请求允许客户端指示实体正文的媒体类型, 以及是否在被覆盖时进行更改.
因此, 客户端**应该[SHOULD]**为新资源提供一个 Content-Type (如果有的话).
如果客户端没有为新资源提供 Content-Type, 服务器**可能[MAY]**创建一个没有分配
Content-Type 的资源, 或者**可能[MAY]**尝试分配一个 Content-Type。

需要注意的是, 尽管接收方通常应该将 HTTP 请求中提供的元数据视为权威,
但实际上并不能保证服务器会接受客户端提供的元数据（e.g., 任何以 "Content-" 开头的请求标头).
首先许多服务器不允许在每个资源上配置 Content-Type.
因此, 客户端并不总是能通过包含 Content-Type 请求标头来直接影响内容类型.

### 9.7.2. 集合中的 PUT

本规范未定义对已存在集合的 PUT 方法行为.
对现有集合的 PUT 请求可能会被视为错误 (405 Method Not Allowed).

[MKCOL 方法][SECTION#9.3])被定义用于创建集合.

## 9.8. COPY 方法

COPY 方法创建由 Request-URI 标识的源资源的副本, 源资源由请求 URI 标识,
目标资源由 Destination 标头中的 URI 标识. Destination 标头**必须[MUST]**存在.
COPY 方法的具体行为取决于源资源类型.

所有符合 WebDAV 规范的资源都**必须[MUST]**支持 COPY 方法.
但是对 COPY 方法的支持并不保证能够复制资源. e.g., 不同的程序可能控制同一服务器上的资源.
最终服务器可能无法将资源复制到看起来在同一服务器上的位置.

该方法幂等但不安全 (请参阅 [RFC2616#9.1]). 不能缓存此方法的响应.

### 9.8.1. 非集合资源中的 COPY

当源资源不是集合时, COPY 方法最终会在目标位置创建一个新资源, 其状态和行为尽可能与源资源匹配.
由于目标位置的环境可能由于服务器掌控外的因素而与源位置不同, 例如缺乏正确操作所需的资源,
因此服务器可能无法完全将资源复制到目标位置. 对目标资源的后续更改将不会修改源资源.
对源资源的后续更改也将不会修改目标资源.

### 9.8.2. 属性中的 COPY

成功执行 COPY 操作后, 源资源上的所有死属性**应该[SHOULD]**都应该复制到目标资源上.
在本文档中描述的活属性**应该[SHOULD]**复制为目标资源上具有相同行为的活属性,
但不一定具有相同的值. 服务器**不应该[SHOULD_NOT]**将活属性在目标资源上的转化为死属性,
因为客户端可能会对资源的状态或功能得出错误的结论. 需要注意的是,
某些活属性定义使得该属性的缺失是有特定含义的 (e,g., 一个标志如果存在则有一种含义，
缺失则有相反的含义), 这些情况下成功的 COPY 操作可能会导致后续请求中报告该属性为 "Not Found".

当目标是一个未映射的 URL 时, COPY 操作会创建一个新的资源, 这种行为类似于 PUT 操作.
相应的, 应当设置与资源创建相关的活属性 (e,g, `DAV:creationdate`) 的值.

### 9.8.3. 集合中的 COPY

对于在集合上且没有 Depth 标头的 COPY 方法,
其行为**必须[MUST]**与包括了值为 "infinity"的 Depth 标头一致.
客户端可能在对集合进行 COPY 时提交一个值为 "0" 或 "infinity"的 Depth 标头.
服务器**必须[MUST]**在兼容 WebDAV 的资源上支持 "0" 和 "infinity" Depth 标头.

无限深度的 COPY 操作指出: 该操作将由 Request-URI 标识的集合资源复制到由目标头中的 URI
标识的位置, 并且将通过递归地遍历集合层次结构的所有级别的方式,
将所有内部成员资源都复制到与其相关的位置. 注意, 以无限深度 COPY 的方式将 `/A/` 复制到
`/A/B/` 中时, 如果没有进行正确处理, 则可能会导致无限递归.

"Depth: 0" 的 COPY 仅仅指出将集合及其属性进行复制, 而不复制由其内部成员 URL 标识的资源.

COPY 中包含的任何标头除 `Destination` 外, 都必须应用于处理要复制的每个资源.

`Destination` 标头仅仅为 Request-URI 指定目标 URI.
当应用于由 Request-URI 标识的集合成员时,
`Destination` 的值将被修改以反映当前的层次结构位置.
因此, 如果 Request-URI 为 `/a/`, Host 标头为 `http://example.com/`,
且 Destination 为 `http://example.com/b/`,
那么在处理 `http://example.com/a/c/d` 时,
Destination 的值必须为 `http://example.com/b/c/d`.

当 COPY 方法完成处理后, 其**必须[MUST]**在目标处创建一个一致的 URL 命名空间
(请参见[第 5.1 章][SECTION#5.1]中有关命名空间一致性的定义).
然而，如果在复制内部集合时出现错误, 服务器**不得[MUST_NOT]**复制该集合成员中的资源
(i.e., 服务器必须跳过这个子树), 因为这会创建一个不一致的命名空间.
检测到错误后, COPY 操作**应该[SHOULD]**尽可能尝试完成原先的复制操作
(i.e., 服务器仍应尝试复制那些 (不是错误导致的) 集合后代的子树及其成员).

举个例子: 如果在集合 `/a/` 上执行无限深度复制操作, 该集合包含集合 `/a/b/` 和`/a/c/`,
并且在复制 `/a/b/` 时发生错误, 服务器仍应该尝试继续复制 `/a/c/`.
同样, 在以无限深度复制非集合资源时其中一部分遇到错误后,
服务器**应该[SHOULD]**尽可能尝试完成原始的复制操作.

如果在执行 COPY 方法时发生错误, 且资源与 Request-URI 中标识的不同,
则服务器**必须[MUST]**响应 207 (Multi-Status),
而且导致失败的资源 URL**必须[MUST]**显示具体的错误.

424 (Failed Dependency) 状态代码**不应该[SHOULD_NOT]**在 207 (Multi-Status)
响应中返回. 这些响应可以被安全地省略, 因为客户端会知道当接收到父级错误时, 后代资源也无法复制.
此外, 201 (Created) / 204 (No Content) 状态代码**不应[SHOULD_NOT]**包含在 COPY 方法
207 (Multi-Status) 响应的值中. 它们也可以被安全地省略, 因为它们是默认的成功代码.

### 9.8.4. COPY 并覆盖目标资源

如果该 COPY 请求具有值为 "F" 的 "Overwrite" 标头, 并且在目标 URL 上存在资源,
name 服务器**必须[MUST]**拒绝该请求.

当服务器执行 COPY 请求并覆盖目标资源时, 实际行为可能会依赖于很多因素,
包括 WebDAV 扩展功能 (详见[RFC3253]). e.g., 当普通资源被覆盖时,
服务器可以在进行复制操作之前删除目标资源, 也可以进行原地覆盖以保留其活属性.

当集合被覆盖时, 成功 COPY 请求后的目标集合成员**必须[MUST]**与 COPY 之前的源集合成员相同.
因此, 在目标中将源集合与目标集合的成员进行合并是不合规行为.

一般来说, 如果客户端要求在 COPY 之前清除目标 URL 的状态 (e.g., 强制重置其活属性),
客户端可以在 COPY 请求之前向目标发送 DELETE 请求, 以确保此重置操作.

### 9.8.5. 状态码

除了可能出现的常规状态码外, 以下状态码特别适用于 COPY 操作:

- 201 (Created): 源资源被成功复制. COPY 操作会导致创建一个新资源.
- 204 (No Content): 源资源成功复制到了一个预先存在的目标资源上。
- 207 (Multi-Status): 多个资源受到 COPY 的影响, 但其中一些资源的错误阻止了该操作继续进行.
  具体的错误消息以及最合适的源 URL 和目标 URL 将出现在多状态响应的正文里.
  e.g., 如果目标资源被锁定且无法被覆盖, 则目标资源的 URL 将显示为 423 (Locked) 状态.
- 403 (Forbidden): 操作被禁止. 一个 COPY 中的特殊情况为: 源资源和目标资源是同一个资源.
- 409 (Conflict): 直到已经创建一个或多个中间集合前, 不能在目标位置创建资源.
  服务器**不得[MUST]**自动创建这些中间集合.
- 412 (Precondition Failed): 前置条件标头检查失败, e.g., "Overwrite" 标头为 “F”,
  而目标 URL 已被映射到一个资源.
- 423 (Locked): 目标资源或目标集合中的资源已被锁定.
  此响应**应该[SHOULD]**包含 "lock-token-submitted" 前置条件元素.
- 502 (Bad Gateway): 当目标位于另一个服务器, 存储库或 URL 命名空间时可能发生该错误.
  要么源命名空间不支持复制到目标命名空间, 要么目标命名空间拒绝接受资源.
  客户端可能希望尝试 GET/PUT 和 PROPFIND/PROPPATCH.
- 507 (Insufficient Storage); 目标资源没有足够的空间来记录执行此方法后的资源状态.

### 9.8.6. 示例 - 覆盖的 COPY

这个示例展示了将资源 `http://www.example.com/~fielding/index.html`
复制到位置 `http://www.example.com/users/f/fielding/index.html`.
204 (No Content) 状态码表示目标位置上的现有资源被覆盖。

```http
>>Request

COPY /~fielding/index.html HTTP/1.1
Host: www.example.com
Destination: http://www.example.com/users/f/fielding/index.html

>>Response

HTTP/1.1 204 No Content
```

### 9.8.7. 示例 - 不覆盖的 COPY

以下示例展示了执行相同的复制操作, 但将 Overwrite 标头设置为"F".
该操作返回了一个 412（Precondition Failed) 响应, 因为目标 URL 已经映射到一个资源上。

```http
>>Request

COPY /~fielding/index.html HTTP/1.1
Host: www.example.com
Destination: http://www.example.com/users/f/fielding/index.html
Overwrite: F

>>Response

HTTP/1.1 412 Precondition Failed
```

### 9.8.8. 示例 - COPY 集合

```xml
>>Request

COPY /container/ HTTP/1.1
Host: www.example.com
Destination: http://www.example.com/othercontainer/
Depth: infinity

>>Response

HTTP/1.1 207 Multi-Status
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<d:multistatus xmlns:d="DAV:">
    <d:response>
        <d:href>http://www.example.com/othercontainer/R2/</d:href>
        <d:status>HTTP/1.1 423 Locked</d:status>
        <d:error><d:lock-token-submitted/></d:error>
    </d:response>
</d:multistatus>
```

该例中, Depth 标头是不必要的, 因为对集合执行 COPY 的默认行为已经是如同已提交
"Depth: infinity" 头部一样. 在此例中, 大多数资源与集合都已被成功复制.
然而，集合 `R2` 由于目标资源 `R2` 被锁定复制失败.
由于在复制 `R2` 时出现错误, `R2` 的所有成员也没有被复制.
然而, 由于错误最小化规则，对于这些成员的错误没有被列出.

## 9.9. MOVE 方法

在非集合资源上执行的 MOVE 操作在逻辑上与下面的方式等价:

- 一个复制 (COPY) 操作
- 进行一致性维护处理
- 删除源资源

在这个三个动作在一个操作中完成. 一致性维护步骤允许服务器执行由移动引起的更新,
比如将除了标识源资源的请求 URI 外的所有 URL 都指向新的目标资源.

MOVE 方法经常被客户端用于在不改变其父集合的前提下重命名文件,
因此重置于资源创建时所设置的所有活属性是不合适的. e.g., "DAV:creationdate"
属性值应该在移动后保持不变.

死属性必须与资源一起移动.

### 9.9.2. 集合中的 MOVE

带有 "Depth: infinity" 的 MOVE 操作表示将位于 Request-URI 标识的集合移动到
Destination 标头所指定的地址, 且所有由其内部成员 URL 标识的资源将
(递归地通过集合层次结构的所有级别) 移动到与其相关的位置.

对于集合上的 MOVE 方法**必须[MUST]**得如同使用 "Depth: infinity" 标头一样.
客户端在集合上 MOVE 时候不能在 Depth 标头中提交除 "infinity" 以外其他任何值.

包含在 MOVE 请求中的任何标头部**必须[MUST]**在处理应用于除了 Destination
标头外的每个要移动的资源. Destination 标头的行为与集合上的 COPY 方法中给出的相同.

当 MOVE 方法完成处理后，其**必须[MUST]**在源位置和目标位置创建一个一致的 URL 命名空间
(有关命名空间一致性的定义，请参[见第 5.1 章][SECTION#5.1]).
不过在移动内部集合时出现错误时, 服务器不能移动由失败集合的成员标识的任何资源
(i.e., 服务器必须跳过引起错误的子树), 因为这将创建一个不一致的命名空间.
这种情况下, 检测到错误后， 移动操作**应该[SHOULD]**尽可能多地尝试完成原始移动
(i.e., 服务器仍应尝试移动其他子树以及由其成员标识的 (不是导致错误的) 集合后代的资源).
例如, 如果在集合 `/a/` 上执行了无限深度移动操作, 该集合包含集合 `/a/b/` 和 `/a/c/`,
且在移动 `/a/b/` 时出现错误时, 则仍应尝试继续移动 `/a/c/`,
类似地, 在无限深度移动操作中移动一部分非集合资源时遇到错误后,
服务器**应该[SHOULD]**尽可能多地尝试完成原始移动.

如果在 Request-URI 中标识资源外的资源发生错误时, **必须[MUST]**响应 207 (Multi-Status),
并且**必须[MUST]**在具体错误的位置标明错误资源的 URL.

MOVE 方法的 207 (Multi-Status) 响应中, 不应返回 424（Failed Dependency）状态码.
这些错误可以被安全地省略, 因为客户端会在为收到父资源错误时了解到不能移动资源的后代.
此外, 不应将 201 (Created) /204 (No Content) 响应作为 207 (Multi-Status)
响应中的返回值. 这些响应可以被安全地省略, 因为它们是默认的成功代码.

### 9.9.3. MOVE 与 Overwrite 标头

如果目标位置存在资源, 且 Overwrite 标头值为 "T", 则在执行移动操作之前,
服务器**必须[MUST]**对目标资源执行一个带有 "Depth: infinity" 的 DELETE 操作;
如果 Overwrite 标头值为 "F", 那么操作将失败.

### 9.9.4. 状态码

除了可能出现的常规状态码外, 以下状态码特别适用于 MOVE 操作:

- 201 (Created): 源资源已成功移动, 并在目标位置创建了一个新的 URL 映射.
- 204 (No Content): 源资源已成功移动到一个已被映射的 URL 上.
- 207 (Multi-Status): 多个资源受到 MOVE 操作的影响, 但其中一些资源的错误导致操作中断.
  具体的错误消息以及最合适的源 URL 和目标 URL 将出现在多状态响应的正文里.
  e.g., 如果源资源被锁定且无法移动, 那么该源资源 URL 将显示为状态码 423 (Locked).
- 403 (Forbidden): 在禁止 MOVE 操作的多重可能原因中,
  建议在源资源和目标资源相同时使用此状态码.
- 409 (Conflict): 直到已经创建一个或多个中间集合前, 目标位置无法创建资源.
  服务器**不能[MUST]**自动创建这些中间集合. 或服务器无法保留活性属性行为,
  并仍将资源移动到目标位置 (请参阅 "preserved-live-properties" 后置条件).
- 412 (Precondition Failed): 一个条件标头失败. 对于 MOVE 操作来说,
  这可能意味着 Overwrite 头部的值是 "F"，且目标 URL 已经并被映射到一个资源.
- 423 (Locked): 源资源, 目标资源, 源资源或目标资源的父级,
  或源资源或目标资源集合中的某些资源被锁定. 这个响应应包含 "lock-token-submitted"
  前置条件元素.
- 502 (Bad Gateway): 这可能发生在目标位于另一个服务器且目标服务器拒绝接受资源这一情况下,
  也可能发生在目标位于相同服务器命名空间下的另一个子部分上时.

### 9.9.5. 示例 - 非集合的 MOVE

这个示例展示了资源 `http://www.example.com/~fielding/index.html` 被移动到位置
`http://www.example.com/users/f/fielding/index.html`.
如果目标 URL 已经映射到一个资源, 目标资源的内容将被覆盖. 在这个例子中,
由于目标资源上没有任何内容，所以响应码是 201 (Created).

```http
>>Request

MOVE /~fielding/index.html HTTP/1.1
Host: www.example.com
Destination: http://www.example/users/f/fielding/index.html

>>Response

HTTP/1.1 201 Created
Location: http://www.example.com/users/f/fielding/index.html
```

### 9.9.6. 示例 - 集合的 MOVE

```xml
>>Request

MOVE /container/ HTTP/1.1
Host: www.example.com
Destination: http://www.example.com/othercontainer/
Overwrite: F
If: (<urn:uuid:fe184f2e-6eec-41d0-c765-01adc56e6bb4>)
    (<urn:uuid:e454f3f3-acdc-452a-56c7-00a5c91e4b77>)

>>Response

HTTP/1.1 207 Multi-Status
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<d:multistatus xmlns:d='DAV:'>
    <d:response>
        <d:href>http://www.example.com/othercontainer/C2/</d:href>
        <d:status>HTTP/1.1 423 Locked</d:status>
        <d:error><d:lock-token-submitted/></d:error>
    </d:response>
</d:multistatus>
```

在这个示例中, 客户端已经与请求一起提交了几个锁令牌（lock tokens). 在方法的作用域中,
无论是源资源还是目标资源, 对于任何已锁定的资源都需要提交相应的锁令牌. 在这个例子中,
请求没有为目标资源 `http://www.example.com/othercontainer/C2/` 提交正确的锁令牌.
这意味着资源 `/container/C2/` 无法被移动. 由于移动 `/container/C2/` 时出现错误, 因此
`/container/C2` 的所有成员也没有被移动. 但由于错误最小化规则, 这些成员的移动错误没有列出.
用户代理身份验证之前已经通过 HTTP 协议范围之外的底层传输层机制处理.

## 9.10. LOCK 方法

以下各节用于描述 LOCK 方法, 该方法用于获取任何访问类型的锁, 并刷新现有锁.
以下章节有关 LOCK 方法仅描述于特定 LOCK 方法的语义, 并与所请求锁的访问类型无关.

任何支持 LOCK 方法的资源**必须[MUST]**至少支持本文中定义的 XML 请求和响应格式.

此方法既不幂等也不安全 (参阅[RFC2616#9.1]). 不得缓存此方法的响应.

### 9.10.1. 在现有资源上创建锁

对于现有资源的 LOCK 请求将在 Request-URI 标识的资源上创建一个锁,
前提是该资源未使用相冲突. Request-URI 中标识的资源成为锁根.
用于创建新锁的 LOCK 方法请求**必须[MUST]**具有一个 XML 请求正文.
服务器**必须[MUST]**保留 LOCK 请求中客户端在 "owner" 元素中提供的信息.
LOCK 请求**可能[MAY]**含有 Timeout 标头.

当新锁创建时, LOCK 响应:

- **必须[MUST]**包含一个在 prop XML 元素中的 `DAV:lockdiscovery` 属性值的正文.
  这**必须[MUST]**包含有关刚授予的锁的完整信息, 而有关其他 (共享) 锁的信息是可选的.
- **必须[MUST]**包括 Lock-Token 响应标头, 其中包含与新锁关联的令牌.

### 9.10.2. 刷新锁

要刷新一个锁, 需要向该锁范围内资源的 URL 发送一个 LOCK 请求.
此请求**不能[MUST_NOT]**具有正文，且**必须[MUST]**使用 "If" 标头指定要刷新的锁,
只能一次刷新一个锁. 请求**可能[MAY]**包含 Timeout 标头,
服务器**可以[MAY]**接受以将锁上剩余的持续时间更改为新值.
服务器**必须[MUST]**忽略 LOCK 刷新上的 Depth 标头.

如果资源有其他 (共享) 锁, 则这些锁不受锁刷新的影响. 此外, 这些锁不会阻止刷新指定的锁.

对于一个成功的刷新 LOCK 请求, 响应中不会返回 Lock-Token 标头,
但 LOCK 响应正文必须包含 `DAV:lockdiscovery` 属性的新值.

### 9.10.3 深度与锁定

Depth 标头可能与 LOCK 方法一起使用. 除了 0 或无穷大之外的值都**不能[MUST_NOT]**与
LOCK 方法的 Depth 标头一起使用. 所有支持 LOCK 方法的资源必须支持 Depth 标头.

值为 0 的 Depth 标头意味着只锁定 Request-URI 中指定的资源.

如果 Depth 标头设置为无穷大, 那么 Request-URI 中指定的资源及其所有成员,
直到整个层次结构最底部，都将被锁定. 该成功结果**必须[MUST]**返回一个单一的锁令牌.
类似地, 如果使用此令牌成功执行 UNLOCK, 则所有关联资源都将被解锁.
因此, LOCK 或 UNLOCK 不会部分锁定成功. 要么整个层次结构被锁定, 要么不锁定任何资源.

如果无法将锁授权给所有资源, 服务器**必须[MUST]**返回多状态响应,
其中至少包含一个阻止授权锁定对应资源的 "response" 元素, 以及适当的状态码用来指示了失败
(例如, 403 (Forbidden) 或 423 (Locked)). 此外, 如果导致失败的资源不是请求资源,
服务器也**应该[SHOULD]**为 Request-URI 包含一个 "response" 元素,
包含一个含有 424 (Failed Dependency) 的 "status" 元素.

如果在 LOCK 请求上未提交任何 Depth 标头, 则该请求必须被视为已提交 "Depth:infinity".

### 9.10.4. 锁定未映射 URL

当 URL 之前不存在资源时, 对其成功的 LOCK 请求**必须[MUST]**最终创建一个已锁定的空资源
(且不是集合). 随后, 锁可以消失, 但空资源仍然存在.
空资源**必须[MUST]**出现在 PROPFIND 响应中, 并包括响应范围中的该 URL.
服务器**必须[MUST]**对空资源的 GET 请求做出成功响应, 可以使用 204 (No Content) 响应,
也可以使用 200 (OK) 响应 (包含带有指示零长度的 Content-Length 标头).

### 9.10.5. 锁兼容性表格

下表描述了在资源上进行锁定请求时的行为.

| 当前状态 | 共享锁允许 | 互斥锁允许 |
| -------- | ---------- | ---------- |
| 无锁     | True       | True       |
| 共享锁   | True       | False      |
| 互斥锁   | False      | False\*    |

> 图例：True = 可以授予锁. False = **必须[MUST_NOT]**不授予锁.
> "\*" = 主体请求相同的锁两次是非法的.

资源的当前锁状态在最左边列中给出, 锁请求在第一行中给出. 行和列的交点给出了锁请求的结果.
例如, 如果在资源上持有共享锁, 并且请求互斥锁, 则表格中的条目为 "false", 既表明不能授予锁.

### 9.10.6. LOCK 响应

除了一般可能出现的状态码外, 以下状态码对于 LOCK 具有特定适应性:

- 200 (OK): LOCK 请求成功, 并且 "DAV:lockdiscovery" 属性的值包含在响应正文中.
- 201 (Created): 对未映射的 URL 的 LOCK 请求, 该请求成功并导致创建新资源,
  并且 "DAV：lockdiscovery" 属性值包含在响应正文中.
- 409 (Conflict): 直到创建一个或多个中间集合前, 无法在目标位置创建资源.
  服务器**不得[MUST_NOT]**自动创建这些中间集合.
- 423 (Locked), 并带有 "no-conflicting-lock" 前置条件码:
  资源上已存在一个与请求的锁不兼容的锁 (请参阅上面的[锁兼容性表格][SECTION#9.10.5]).
- 412 (Precondition Failed)，带有 "lock-token-matches-request-uri" 前置条件码:
  LOCK 请求带有 If 标头, 表示客户端希望刷新其指定的锁.
  但是 Request-URI 不在由标记标识的锁的范围内. 锁的范围可能不包括该 Request-URI,
  或是锁可能已消失, 或是令牌可能无效.

### 9.10.7. 示例 - 简单的锁请求

```xml
>>Request

LOCK /workspace/webdav/proposal.doc HTTP/1.1
Host: example.com
Timeout: Infinite, Second-4100000000
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx
Authorization: Digest username="ejw",
realm="ejw@example.com", nonce="...",
uri="/workspace/webdav/proposal.doc",
response="...", opaque="..."

<?xml version="1.0" encoding="utf-8" ?>
<D:lockinfo xmlns:D='DAV:'>
    <D:lockscope><D:exclusive/></D:lockscope>
    <D:locktype><D:write/></D:locktype>
    <D:owner>
        <D:href>http://example.org/~ejw/contact.html</D:href>
    </D:owner>
</D:lockinfo>

>>Response

HTTP/1.1 200 OK
Lock-Token: <urn:uuid:e71d4fae-5dec-22d6-fea5-00a0c91e6be4>
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:prop xmlns:D="DAV:">
    <D:lockdiscovery>
        <D:activelock>
            <D:locktype><D:write/></D:locktype>
            <D:lockscope><D:exclusive/></D:lockscope>
            <D:depth>infinity</D:depth>
            <D:owner>
                <D:href>http://example.org/~ejw/contact.html</D:href>
            </D:owner>
            <D:timeout>Second-604800</D:timeout>
            <D:locktoken>
                <D:href>urn:uuid:e71d4fae-5dec-22d6-fea5-00a0c91e6be4</D:href>
            </D:locktoken>
            <D:lockroot>
                <D:href
                >http://example.com/workspace/webdav/proposal.doc</D:href>
            </D:lockroot>
        </D:activelock>
    </D:lockdiscovery>
</D:prop>
```

这个例子演示了在资源 "http://example.com/workspace/webdav/proposal.doc"
上成功创建一个互斥写锁.
资源 "http://example.org/~ejw/contact.html" 包含了锁创建者的联系信息.
服务器在这个资源上使用了基于活动 (activity-based) 的超时策略,
这会导致锁在 1 周后 (604800 秒) 被自动移除. 需要注意的是,
Authorization 请求标头中的 `nonce`, `response` 和 `opaque` 字段未被计算生成.

> 译者注: 这些字段尚未被填充, 因为在该示例中关注的重点是 UNLOCK 操作,
> 而这些字段牵扯到服务器认证机制, 该示例中并不需要关注这些认证细节.

### 9.10.8. 示例 - 刷新一个写锁

```xml
>>Request

LOCK /workspace/webdav/proposal.doc HTTP/1.1
Host: example.com
Timeout: Infinite, Second-4100000000
If: (<urn:uuid:e71d4fae-5dec-22d6-fea5-00a0c91e6be4>)
Authorization: Digest username="ejw",
realm="ejw@example.com", nonce="...",
uri="/workspace/webdav/proposal.doc",
response="...", opaque="..."

>>Response

HTTP/1.1 200 OK
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:prop xmlns:D="DAV:">
<D:lockdiscovery>
    <D:activelock>
        <D:locktype><D:write/></D:locktype>
        <D:lockscope><D:exclusive/></D:lockscope>
        <D:depth>infinity</D:depth>
        <D:owner>
            <D:href>http://example.org/~ejw/contact.html</D:href>
        </D:owner>
        <D:timeout>Second-604800</D:timeout>
        <D:locktoken>
            <D:href
            >urn:uuid:e71d4fae-5dec-22d6-fea5-00a0c91e6be4</D:href>
        </D:locktoken>
        <D:lockroot>
            <D:href
            >http://example.com/workspace/webdav/proposal.doc</D:href>
        </D:lockroot>
    </D:activelock>
</D:lockdiscovery>
</D:prop>
```

此请求将刷新锁, 尝试将超时时间重置为 timeout 标头中指定的新值.
需要注意的是,客户端请求了一个无限超时, 但服务器选择忽略该请求.
在该例中, Authorization 请求标头中的 `nonce`, `response` 和 `opaque` 字段未被计算生成.

### 9.10.9. 示例 - 多资源锁请求

```xml
>>Request

LOCK /webdav/ HTTP/1.1
Host: example.com
Timeout: Infinite, Second-4100000000
Depth: infinity
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx
Authorization: Digest username="ejw",
realm="ejw@example.com", nonce="...",
uri="/workspace/webdav/proposal.doc",
response="...", opaque="..."

<?xml version="1.0" encoding="utf-8" ?>
<D:lockinfo xmlns:D="DAV:">
    <D:locktype><D:write/></D:locktype>
    <D:lockscope><D:exclusive/></D:lockscope>
    <D:owner>
        <D:href>http://example.org/~ejw/contact.html</D:href>
    </D:owner>
</D:lockinfo>

>>Response

HTTP/1.1 207 Multi-Status
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:multistatus xmlns:D="DAV:">
    <D:response>
        <D:href>http://example.com/webdav/secret</D:href>
        <D:status>HTTP/1.1 403 Forbidden</D:status>
    </D:response>
    <D:response>
        <D:href>http://example.com/webdav/</D:href>
        <D:status>HTTP/1.1 424 Failed Dependency</D:status>
    </D:response>
</D:multistatus>
```

这个例子展示了对集合及其所有子集合请求互斥写锁的情况. 此请求中, 客户端指出其希望获得无限期的锁,
否则希望设置 41 亿秒的超时. 请求实体正文包含了取得锁主体的联系信息,
该例中是一个 Web 页面的 URL.

错误是对资源 "http://example.com/webdav/secret" 上的 403 (Forbidden) 响应.
因为无法锁定此资源, 没有资源被锁定. 还需要注意的是,
Request-URI 本身的 "response" 元素已按要求包含在内.

在该例中, Authorization 请求标头中的 `nonce`, `response` 和 `opaque` 字段未被计算生成.

## 9.11. UNLOCK 方法

UNLOCK 方法会移除由 Lock-Token 请求标头中的锁定牌标识的锁.
请求 URI **必须[MUST]**标识锁范围内的资源.

需要注意的是, 使用 Lock-Token 标头来提供锁令牌的方式与其他更改状态的方法不一致,
其他方法都需要带有锁令牌的 If 标头. 因此, 不需要 If 标头来提供锁令牌.
一般当 If 标头存在时, 其具有正常条件标头的含义.

如果此方法成功响应, 服务器必须完全删除锁.

如果所有根据提交的锁令牌而被锁定的资源都无法被解锁, 则 UNLOCK 请求**必须[MUST]**失败.

对 UNLOCK 方法的成功响应并不意味着资源一定已解锁. 该情况只表示指定令牌对应的特定锁不再存在.

任何支持 LOCK 方法的 DAV 兼容资源**必须[MUST]**支持 UNLOCK 方法.

该方法幂等但不安全 (参见[RFC2616#9.1]). 不得缓存此方法的响应.

### 9.11.1. 状态码

除了可能的通用状态码外, 以下状态码在特定情况适用:

- 204 (No Content): 正常的成功响应 (与 200 OK 响应不同,
  因为 200 OK 将意味着存在响应正文, 而 UNLOCK 成功响应通常不包含正文).
- 400 (Bad Request): 未提供锁令牌.
- 403 (Forbidden): 当前经过身份验证的主体没有删除该锁的权限.
- 409 (Conflict), 并带有 "lock-token-matches-request-uri" 前置条件: 该资源未被锁定,
  或请求针对不在锁定范围内的 Request-URI.

### 9.11.2. 示例 - UNLOCK

```http
>>Request

UNLOCK /workspace/webdav/info.doc HTTP/1.1
Host: example.com
Lock-Token: <urn:uuid:a515cfa4-5da4-22e1-f5b5-00a0451e6bf7>
Authorization: Digest username="ejw"
realm="ejw@example.com", nonce="...",
uri="/workspace/webdav/proposal.doc",
response="...", opaque="..."

>>Response

HTTP/1.1 204 No Content
```

该示例中, 由锁令牌 "urn:uuid:a515cfa4-5da4-22e1-f5b5-00a0451e6bf7"
标识的锁已成功从资源 `http://example.com/workspace/webdav/info.doc` 中移除.
如果此锁包括不止一个资源, 则将从包括在该锁中的所有资源中移除该锁.

在该示例中, Authorization 请求标头中的 `nonce`, `response` 和 `opaque`
字段未被计算生成.
