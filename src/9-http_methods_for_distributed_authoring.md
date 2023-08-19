# 9. 用于分布式创作的 HTTP 方法 (HTTP Methods for Distributed Authoring)

## 9.1. PROPFIND 方法 (PROPFIND Method)

PROPFIND 方法用于检索在由请求 URI (Request-URI) 标识资源上定义的属性:

- 如果该资源没有任何内部成员, 则返回该资源上定义的属性;
- 如果该资源是一个集合并具有内部成员 URL, 则返回由请求 URI 标识资源及其可能的成员资源的属性.

所有符合 DAV 标准的资源都必须支持 PROPFIND 方法和 `propfind` XML 元素
([第十四章第二十小节]()) 以及与 `propfind` 元素一起使用的所有 XML 元素.

客户端在 PROPFIND 请求中必须提交一个值可以是 "0"、"1" 或者 "infinity" 的 Depth 标头.
服务器必须**支持** (MUST) 符合 WebDAV 的资源的 "0" 和 "1" 深度的请求，并**应该**
(SHOULD) 支持 "infinity" 请求. 实际上，由于与此行为相关的性能和安全问题, 对于无限深度
(infinite-depth) 请求的支持**可能** (MAY) 被禁用. 服务器**应该** (SHOULD) 将没有 Depth 标头的请求视为包含了 "Depth: infinity" 标头.

客户端可以在请求方法主体中提交 "propfind" XML 元素, 描述正在请求的信息. 这可能会:

- 通过在 "prop" 元素内命名想要的属性来请求特定的属性值 (服务器**可能** (MAY)
  忽略这里的属性排序).
- 使用 "allprop" 元素请求在此规范中(最小)定义的属性以及死属性的属性值 ("include"
  元素可以与 "allprop" 一起使用, 用来指示服务器 (包括在其他情况下可能不会)
  返回的附加活属性).
- 使用 'propname' 元素请求资源上所有定义属性的名称列表.

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

客户端可以选择不提交请求主体. 一个空的 PROPFIND 请求主体必须被视为 "allprop" 请求.

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
服务器存在越来越多地具有高昂计算成本或冗长的属性 (参见 [RFC3253] 和 [RFC3744]), 所以并不会返回所有属性. 相反, WebDAV 客户端可以使用 "propname" 来请求并发现存在哪些活属性,
并在需要检索值时请求特定的属性. 对于在其他地方定义的活属性，该定义
(_译者注: 指服务器可能不会返回所有的属性_) 可以指定是否会在 "allprop" 请求中返回该活属性.

所有服务器必须支持返回内容类型为 `text/xml` 或 `application/xml` 的响应, 其中包含一个描述检索各种属性尝试结果的 "multistatus" XML 元素。

如果在检索属性时出现错误, 那么响应中**必须** (MUST) 包含适当的错误结果. 对于尝试检索不存在的属性的请求是一种错误, 且必须使用包含 404 (Not Found) 状态值的 "response" XML 元素进行记录.

最后, 集合资源的 "multistatus" XML 元素在任何深度的请求中**必须** (MUST)
为集合的每个成员 URL 包含一个 "response" XML 元素. 其**不应该** (SHOULD NOT)
包含任何不符合 WebDAV 标准的资源的 'response' 元素. 每个 "response"
元素必须包含一个有 "prop" XML 元素中定义属性资源的 URL 的 'href' 元素.
集合资源的 PROPFIND 结果将以一个扁平列表 (flat list) 返回，其中条目的顺序并不重要.
需要注意的是，资源对于给定名称的属性可能只有一个值, 因此该属性可能仅在 PROPFIND 响应中出现一次.

属性可能受到访问控制的限制. 一种情况是在 "allprop" 和 "propname" 请求下, 如果一个主体)
(principal) 没有权限知道特定属性是否存在, 那么该属性**可能** (MAY) 会在响应中被静默排除.

一些 PROPFIND 结果可能会被缓存, 但需要小心, 因为大多数属性没有缓存验证机制.
PROPFIND 方法是既安全又幂等的 (参见 [RFC2616#9.1]).

### 9.1.1. PROPFIND 响应码 (PROPFIND Status Codes)

这章与与其他方法的类似部分一样, 提供了关于错误代码和一些可能在 PROPFIND
中特别有用的前置或后置条件 (在[第十六章]()中定义) 的指导建议.

403 Forbidden - 服务器**可能** (MAY) 会拒绝具有 "Infinity" 深度标头集合上的 PROPFIND
请求. 在这种情况下, 服务器应使用这个错误, 并在错误主体中使用前置条件代码
"propfind-finite-depth".

### 9.1.2. 用于 "propstat" 元素的状态码

在 PROPFIND 响应中, 有关各个属性的信息返回在 "propstat" 元素内
(详见[第十四章二十二小节]()), 每个 "propstat" 元素包含一个 "status" 元素, 每个
"status" 元素都包含关于出现在该元素中属性的信息. 下述列表总结了在 "propstat" 内最常用的状态码; 然而客户端应该能很好的随时应对并处理其他 2/3/4/5xx 系列的状态码.

- 200 OK: 属性存在，且/或其值成功返回.
- 401 Unauthorized - 属性未经适当授权无法查看.
- 403 Forbidden - 属性不论授权与否, 都无法查看.
- 404 Not Found - 属性不存在.

### 9.1.3. 一个检索命名属性的例子 (Example - Retrieving Named Properties)

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
"propfind" XML 元素指定了正在请求的四个属性的名称. 在这个例子中, 只返回了两个属性，因为发出请求的主体没有足够的访问权限查看后两个个属性.

### 9.1.4. 一个使用 "propname" 检索所有属性名称的例子 (Example - Using 'propname' to Retrieve All Property Names)

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

在这个例子中, PROPFIND 在集合资源 "http://www.example.com/container/" 上调用,
"propfind" XML 元素包含 "propname" XML 元素, 表示应该返回所有属性的名称.
由于没有出现 Depth 标头，服务器假设其默认值为 "infinity", 意味着服务器应该返回集合及其所有后代的属性名称.

与前面的例子一样, 在资源 "http://www.example.com/container/" 定义了六属性:

- `bigbox` 和 `author` 在命名空间 "http://ns.example.com/boxschema/" 中定义;
- `creationdate`, `displayname`, `resourcetype` 和 `supportedlock` 在 "DAV:"
  命名空间中定义.

资源 "http://www.example.com/container/index.html" 是集合 `container`
上的一个成员, 里面定义了九个属性:

- `bigbox` 在命名空间 "http://ns.example.com/boxschema/" 中定义;
- `creationdate`, `displayname`, `getcontentlength`, `getcontenttype`,
  `getetag`, `getlastmodified`, `resourcetype` 和 `supportedlock` 在 "DAV:"
  命名空间中定义.

这个例子还演示了 XML 命名空间作用域 (XML namespace scoping) 和默认命名空间
(default namespace) 的使用方式. 由于 "xmlns" 属性没有包含前缀,
命名空间默认应用于所有包含的元素. 因此, 所有没有明确声明所属命名空间的元素都是 "DAV:"
命名空间的成员.

### 9.1.5. 使用所谓的 "allprop" (Example - Using So-called 'allprop')

需要注意的是, 尽管 "allprop" 的名字保持了向后兼容性, 但其并不返回所有属性,
而只返回死属性和在此规范中定义的活属性. (_译者注: 规范定义的属性在[第十五章]()_)

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

在这个例子中, PROPFIND 在集合资源 "http://www.example.com/container/"
上使用一个深度为 1 的标头进行调用, 该请求适用于资源及其子资源, 并且 "propfind" XML
元素包含 "allprop" XML 元素. 该请求表示应该返回在资源上定义的所有死属性的名称和值,
以及在本规范中定义的所有活属性的名称和值. 这个例子还演示了响应中 "href" 元素相对引用的使用.

资源 "http://www.example.com/container/" 上定义了六个属性:

- `bigbox` 和 `author` 属于命名空间 "http://ns.example.com/boxschema/"
- `creationdate`, `displayname`, `resourcetype` 和 `supportedlock` 在 `DAV:`
  上定义.

最后四个属性是 WebDAV 特有的的, 定义在[第十五章](). 由于此资源不支持 GET 请求, 因此
"get" 属性（e.g., DAV:getcontentlength）没有定义在此资源上.

在上面的 xml 实例中, "container" 容器拥有如下 WebDAV 特有的属性断言 (assert):

- 在 1997/12/01 5:42:21PM GMT-8 创建的 (`DAV:creationdate`),
- 名称为 "Example collection" (`DAV:displayname`),
- 是一个集合资源类型 (`DAV:resourcetype`),
- 支持独占写锁和共享写锁 (`DAV:supportedlock`).

资源 "http://www.example.com/container/front.html" 上定义了九个属性:

- `bigbox` 属于命名空间 "http://ns.example.com/boxschema/" (另一个 "bigbox"
  属性类型的实例 (区别于资源 "http://www.example.com/container/" 中的属性定义))
- `DAV:creationdate`, `DAV:displayname`, `DAV:getcontentlength`,
  `DAV:getcontenttype`, `DAV:getetag`, `DAV:getlastmodified`, `DAV:resourcetype` 和 `DAV:supportedlock`.

在上面的 xml 示例中, "front.html" 器拥有如下 WebDAV 特有的属性断言 (assert):

- 在 1997/12/01 6:27:21PM GMT-8 创建的 (`DAV:creationdate`),
- 名称为 "Example HTML resource" (`DAV:displayname`),
- 内容长度为 4525 字节 (`DAV:getcontentlength`),
- MIME 类型为 "text/html" (`DAV:getcontenttype`),
- 实体标记为 "zzyzx" (`DAV:getetag`).
- 在 1998/01/12 09:25:56AM GMT 进行最后修改 (`DAV:getlastmodified`),
- 该属性具有空的资源类型, 意味其不是一个集合 (`DAV:resourcetype`),
- 支持独占写锁和共享写锁 (`DAV:supportedlock`).

### 9.1.6. 一个使用 "allprop" 与 "include" 的示例 (Example - Using 'allprop' with 'include')

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

在这个示例中, PROPFIND 在资源 "http://www.example.com/mycol/" 及其内部成员资源上调用.
客户端请求获取在本规范中定义的所有活属性与死属性的值, 加上两个在 [RFC3253]
中额外定义的活属性. 该消息响应没有在示例中显示.
