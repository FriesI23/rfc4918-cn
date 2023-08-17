# 5. 网络资源集合 (Collections of Web Resources)

本章提供了一种 Web 资源类型 -- 集合的描述, 并讨论了它与 HTTP URL 命名空间和 HTTP
方法的交互. 集合资源的目的是在服务器命名空间内为那些类似集合的对象提供建模 (model
collection-like objects) (e.g., 文件系统目录).

所有符合 DAV 标准的资源必须支持在此规范中指定的 HTTP URL 命名空间模型.

## 5.1. HTTP URL 命名空间模型 (HTTP URL Namespace Model)

HTTP URL 命名空间是一个层次结构的, 使用 `/` 分隔.

如果一个 HTTP URL 命名空间符合以下条件, 就称其为一致的:

- 对于 HTTP 层次结构中的每个 URL, 都存在一个包含该 URL 作为内部成员 URL 的合集.
- 根或顶级集合可以不受前面的规则的限制.

所考虑的命名空间的顶级集合不一定是由绝对路径 `/` 标识, 它可以由一个或多个路径段来标识
(e.g., `/servlets/webdav/...`).

HTTP/1.1 与 WebDAV 皆不要求整个 HTTP URL 命名空间必须一致. 符合 WebDAV
的资源可能没有父集合. 然而某些 WebDAV 方法会被禁止产生导致命名空间不一致的结果.

任何资源, 包括集合资源, 都**可能** (MAY) 由多个 URI 标识, 正如在 [RFC2616] 和
[RFC3986] 中所隐含的一样. e.g., 一个资源可以由多个 HTTP URL 标识.

## 5.2. 集合资源 (Collection Resources)

集合资源与其他资源的区别在于它们还充当了容器. 一些 HTTP 方法仅适用于集合,
但某些方法也适用于由集合定义的容器内的某些或所有资源. 当方法的作用范围不明确时,
客户端可以指定深度. 深度可以是:

- 0 级 (仅集合)
- 1 级 (集合和直接包含的资源)
- 无限制 (infinite levels) (集合和所有递归包含的资源)

集合状态至少包括一组路径段 (path segments) 和资源 (resource) 之间的映射及本身的一组属性.
在本文中, 如果存在一个映射的路径段与 `资源B` 相关, 且该映射包含在 `集合资源A` 中, 那么说
`资源B` 包含在 `集合资源A` 中. 一个集合**必须** (MUST) 最多可以包含一个给定的路径段映射,
换句话说, 将同一路径段映射到多个资源是非法的.

集合资源上定义的属性与非集合资源上的属性行为完全相同. 一个集合**可能** (MAY) 具有额外的状态,
e.g., 由 GET 返回的 Body.

对于所有符合 WebDAV 标准的 `资源A` 和 `资源B`，分别由 URL `U` 和 `V` 标识, 并使得 `V`
等于 `U/SEGMENT`, `资源A` **必须** (MUST) 是一个包含从 `SEGMENT` 到 `资源B`
的集合映射. 因此, 如果 URL `http://example.com/bar/blah` 的 `资源B` 符合 WebDAV
标准, 且 URL `http://example.com/bar/` 的 `资源A` 也符合 WebDAV 标准, 那么 `资源A`
**必须** (MUST) 是一个集合, 并且必须包含一个从 `blah` 到 `资源B` 的映射.

尽管映射通常由一个单独的段 (segment) 和一个资源 (resource) 组成. 但一般来说,
映射由一组段和一个资源组成. 这允许服务器将一组段视为等价的 (即所有段都映射到同一个资源,
或者没有分段映射到对应资源). e.g., 对段执行字符折叠(case-folding)的服务器将把分段 `ab`,
`Ab`, `aB`, `AB` 视为等价的, 客户端可以使用其中任何一个分段来标识资源. 需要注意的是
`PROPFIND` 返回的结果将选择其中一个等价的段来标识映射, 因此每个映射都会有一个 `PROPFIND`
响应元素 (response element), 而不是每个映射中的段都有一个.

集合资源**可能** (MAY) 在 HTTP URL 命名空间层次结构中映射到不符合 WebDAV 标准的资源,
但这不是必需的. e.g, 如果 URL `http://example.com/bar/blah` 上的 `资源X` 不符合
WebDAV 标准, URL `http://example.com/bar/` 上的 `资源A` 是 WebDAV 集合, 那么
`资源A` 不一定有从 `blah` 到 `资源X` 的映射.

如果一个符合 WebDAV 标准的 `资源Y` 在 HTTP URL 命名空间层次结构中没有符合 WebDAV
标准的内部成员, 那么 `资源Y` 不需要一定是一个集合.

有一个一般惯例, 当在没有尾部斜杠的情况下引用集合时, 服务器可以像尾部斜杠存在一样处理请求.
这种情况下, 应该在响应中返回一个指向以斜杠结尾的 URL 的 `Content-Location` 标头.
e.g., 如果客户端在 `http://example.com/blah` 上调用一个方法(没有尾部斜杠),
服务器可以像在该操作 `http://example.com/blah/` 一样响应调用, 并且应该返回一个值为 `http://example.com/blah/` 的 `Content-Location` 标头. 服务器不管在何处生成指向集合的 URL 时都**应该** (SHOULD) 包括尾部斜杠. 通常情况下，客户端应该使用尾部斜杠形式的集合名称.
如果客户端不使用尾部斜杠形式, 则需要准备好收到一个重定向响应 (redirect response).
客户端会发现 `DAV:resourcetype` 属性比 URL 可以更可靠地确定资源是否是集合.

客户端**必须** (MUST) 能够支持 WebDAV 资源被包含在非 WebDAV 资源内的情况. e.g.,
如果来自 `http://example.com/servlet/dav/collection` 的 `OPTIONS`
响应表示自己支持 WebDAV, 客户端不能假设 `http://example.com/servlet/dav/`
或其父级必然是 WebDAV 集合.

一个典型的情况是, 在服务器允许链接或重定向到非 WebDAV 资源时, 映射的 URL
通常不会显示为其父集合的成员. e.g., 尽管服务器对于对 `/col/link` 的 `GET`
请求会回应一个 302 状态, 且 `/col/link` 可能不会显示为 `/col/` 的成员,
然而 `/col/link` 的 URL 确实被映射了. 相似的, 一个动态生成的页面可能会有一个从
`/col/index.html` 映射的 URL, 这个资源并不会显示为 `/col/` 的成员,
但可能会对 GET 请求回应一个 200 OK.

> 译者注: 怎么理解这段话
>
> ```xml
> # 1. 客户端发出一个 GET 请求
> GET /col/link HTTP/1.1
> Host: example.com
>
> # 2. 服务器响应一个 302
> HTTP/1.1 302 Found
> Location: https://example.com/non-webdav-resource
>
> # 3. 请求 `/col` 的成员列表
> PROPFIND /col/ HTTP/1.1
> Host: example.com
> Depth: 1
> Content-Type: text/xml; charset="utf-8"
>
> <?xml version="1.0" encoding="utf-8" ?>
> <D:propfind xmlns:D="DAV:">
>   <D:prop>
>     <!-- 指定检索属性为资源类型 -->
>     <D:resourcetype />
>   </D:prop>
> </D:propfind>
>
> # 4. 得到的所有成员列表
> HTTP/1.1 207 Multi-Status
> Content-Type: text/xml; charset="utf-8"
>
> <?xml version="1.0" encoding="utf-8" ?>
> <D:multistatus xmlns:D="DAV:">
>   <!-- /col -->
>   <D:response>
>     <D:href>/col/</D:href>
>     <D:propstat>
>       <D:prop>
>         <D:resourcetype>
>           <D:collection />
>         </D:resourcetype>
>       </D:prop>
>       <D:status>HTTP/1.1 200 OK</D:status>
>     </D:propstat>
>   </D:response>
>   <!-- /col/link 不一定会被列出来, 需要看服务器具体实现  -->
>   <!-- <D:response>
>     <D:href>/col/link</D:href>
>     <D:propstat>
>       <D:prop>
>         <D:resourcetype />
>       </D:prop>
>       <D:status>HTTP/1.1 302 Found</D:status>
>     </D:propstat>
>   </D:response> -->
>  <!-- 资源 /col/index.html  -->
>  <D:response>
>    <D:href>/col/index.html</D:href>
>    <D:propstat>
>      <D:prop>
>        <D:resourcetype />
>      </D:prop>
>      <D:status>HTTP/1.1 200 OK</D:status>
>    </D:propstat>
>  </D:response>
> </D:multistatus>
> ```
>
> `https://example.com/non-webdav-resource` 可能不是一个 WebDAV 资源,
> 并且 `/col/link` 也可能不会出现在父集合 (`/col/`) 成员列表中
> (`/col/address`, `/col/index.html`, ...)

即使是对于符合 WebDAV 标准的资源, 有些映射可能也不会显示在父集合中. 一个例子是为每个 WebDAV
兼容资源提供多个别名 URL 的服务器. 服务器可能实现了大小写不敏感的 URL, 因此 `/col/a` 和
`/col/A` 会标识为相同的资源，但是在列出 `/col` 的成员时只会返回 `a` 或 `A` 中的一个.
在服务器将一组段视为等效的情况下, 服务器**必须** (MUST) 在 `PROPFIND`
响应中为每个映射仅公开一个一致选择 (consistently chosen) 的首选段 (preferred segment).
