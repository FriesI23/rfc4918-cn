# 8. 一般请求与相应处理 (General Request and Response Handling)

## 8.1. 错误处理优先级 (Precedence in Error Handling)

服务器在处理请求时, **必须** (MUST) 优先返回授权错误 (authorization errors),
而不是其他类型的错误. 这样做可以避免泄露受保护资源的信息 (e.g.,
客户端通过匿名请求受保护资源返回的 423 锁定错误响应，从而发现隐藏资源的存在).

## 8.2. XML 的使用 (Use of XML)

在 HTTP/1.1 中，方法参数信息仅通过 HTTP 标头进行编码. 与 HTTP/1.1 不同，WebDAV 在 XML
请求实体主体（[REC-XML]）或 HTTP 标头中编码方法参数信息. 使用 XML
来编码方法参数的动机是为了能够向现有结构添加额外的 XML 元素以提供可扩展性；
以及 XML 能够通过以 ISO 10646 字符集编码信息来提供国际化支持.

除了编码方法参数, WebDAV 中还使用 XML 来编码方法响应, 为方法输出提供 XML
的可扩展性和国际化, 以及输入方面的优势。

当 XML 用于请求或响应主体时, `Content-Type` 类型**应该** \*(SHOULD) 为
`application/xml`. 实现**必须** (MUST) 在请求和响应主体中接受 `text/xml` 和
`application/xml`. 其中 `text/xml` 已被弃用。

所有符合 DAV 标准的客户端和资源必须使用符合 [REC-XML] 和 [REC-XML-NAMES] 标准的
XML 解析器. 所有在请求或响应中使用的 XML **必须** (MUST) 至少是结构正确 (well formed)
且正确使用命名空间的. 如果服务器接收到不良好结构 (not well-formed) 的 XML，
那么服务器**必须** (MUST) 返回 400（Bad Request）拒绝整个请求.
如果客户端在响应中收到了不良格式的 XML, 那么客户端**不能** (MUST NOT) 对执行的方法结果做出任何假设, 并且**应该** (SHOULD)将服务器视为故障.

注意, 处理不受信来源提交的 XML 可能会导致隐私, 安全和服务质量相关的风险(参考[第二十章]()).
服务器**可能** (MAY) 会拒绝可疑请求 (即使它们由良好格式的 XML 构成), 比如返回 400
(Bad Request) 状态代码和可选的响应主体来解释问题.

## 8.3. 处理 URL

URL 会出现在请求和响应的很多地方. 与 [RFC2518] 的互操作性经验显示许多解析多状态
(Multi-Status) 响应的客户端没有完全实现 [RFC3986#5] 中定义的完整引用解析. 因此，
服务器在处理响应中的 URL 时尤其需要小心, 要确保客户端具有足够的上下文来解释所有的 URL.
本章中的规则不仅适用于多状态响应 `href` 元素中的资源 URL, 也同样适用于目标 (Destination)
和条件 (If) 标头中的资源 URL.

发送者可以从两种方法中选择其中一种:

- 使用相对引用 (relative reference), 这个引用会根据请求 URI (Request-URI) 进行解析.
- 使用完整 URI (full URI) 进行解析.

服务器必须确保每个多状态响应中 `href` 的值使用相同格式.

WebDAV 仅在其扩展中使用了一种形式的相对引用, 即绝对路径.

```http
Simple-ref = absolute-URI | ( path-absolute [ "?" query ] )
```

其中，`absolute-URI`, `path-absolute` 和 `query` 规范分别在 [RFC3986#4.3]
[RFC3986#3.3] 和 [RFC3986#3.4] 中定义.

在 `Simple-ref` 规范中，发送者**不得** (MUST NOT):

- 使用点分段 (".", "..")

或者

- 具有与请求 URI 不匹配的前缀 (使用 [RFC2616#3.2.3] 中定义的比较规则).

集合的标识符应以 '/' 字符结尾.

### 8.3.1. 一个正确处理 URL 的实例 (Example - Correct URL Handling)

考虑集合 `http://example.com/sample/`, 其中包含内部成员 URL `http://example.com/sample/a%20test`, 以及以下 PROPFIND 请求:

```http
>>Request:

    PROPFIND /sample/ HTTP/1.1
    Host: example.com
    Depth: 1
```

在这种情况下, 服务器应返回两个包含 `href` 元素的内容中的任意一个:

- `http://example.com/sample/` 与 `http://example.com/sample/a%20test`

或者

- `/sample/` 与 `/sample/a%20test`

需要注意的是，尽管服务器内部可能将成员资源存储为 'a test', 但在 URI 引用中使用时,
它必须进行百分号编码 (percent-encoded), 以符合 [RFC3986#2.1] 中对 URI 的要求.
此外还要注意，一个合法的 URI 仍可能包含在 XML 字符集中需要转义的字符, 比如 `&` 字符.

## 8.4. 请求中必要的主体

一些新的方法没有定义请求主体. 服务器必须检查所有请求是否有主体, 即使这个主体不是期望的.
在存在请求主体但服务器将忽略它的情况下, 服务器必须返回 415 (不支持的媒体类型) 拒绝该请求.
这会通知可能正尝试使用扩展功能客户端, 既服务器无法按照客户端的意图处理请求主体.

## 8.5. 用于 WebDAV 的 HTTP 标头

HTTP 定义了许多可用于 WebDAV 请求和响应的标头. 这些标头并非所有情况下都适用,
其中某些交互可能未定义. 注意, HTTP 1.1 在如果可能的情况下会要求在所有响应中包含 `Date`
标头 (参见 [RFC2616#14.18]).

服务器**必须** (MUST) 在检查任何 HTTP 条件标头之前进行授权检查.

> 译者注: 参考["错误处理优先级"小节](#81-错误处理优先级-precedence-in-error-handling)

## 8.6. ETag

HTTP 1.1 建议在控制缓存时使用 `ETags` 而不是修改日期, 甚至有更强烈的理由在内容编写
(authoring) 时优先考虑 `ETags`. 正确使用 `ETags` 在分布式创作环境中更为重要，因为在避免丢失更新问题时，锁定与 `ETags` 必不可少. e.g.，当锁定超时时，客户端可能无法续订锁定
(renew a lock), 而且客户端有可能在锁定超时时意外离线或正在进行长时间上传. \
当客户端无法续订锁定时, 资源仍可以被重新锁定, 只要没有同有进行更改, 用户便可以继续编辑.
`ETag` 在客户端能够区分这种情况时是必须的.
否则客户端将被迫询问用户是否在没有办法判断资源被更改的情况下覆盖服务器上的资源.
时间戳并不能像 `ETags` 那样有效地解决这个问题.

`强ETags` 比 `弱ETags` 在内容编写时候更有用 (见[RFC2616#13.3.3]).
语义等价性可以是一个有用的概念, 但这取决于文档类型和应用类型，互操作性 (interoperability)
可能需要在本规范和 HTTP 范围之外达成一些协议或标准. 同时要注意的是, `弱ETags` 在 HTTP 中有一些限制，e.g., 在 `If-Match` 标头中无法使用它们.

需要注意的是，在 PUT 响应中 `ETag` 的含义在本文档或 [RFC2616] 中都没有明确定义 (i.e., `ETag` 是否表示资源与 PUT 请求主体等效;
或服务器是否可以在存储时对文档的格式或内容进行细微更改).
这不仅仅是 WebDAV, 而是 HTTP 的一个问题.

<!-- TODO -->