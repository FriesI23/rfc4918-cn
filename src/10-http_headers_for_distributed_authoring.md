# 10. 用于分布式创作的 HTTP 标头

所有的 DAV 标头都遵循与 HTTP 标头同样的基本格式规则. 其中包括一些规则,
像是行延续 (line continuation) 与 怎样使用逗号将多个具有相同标头的实例融合(或分离).

WebDAV 在 HTTP 定义集中添加了两个新的条件性标头: `If` 和 `Overwrite` 标头.

## 10.1. DAV 标头

```bnf
DAV              = "DAV" ":" #( compliance-class )
compliance-class = ( "1" | "2" | "3" | extend )
extend           = Coded-URL | token
                    ; token 在 RFC 2616 第 2.2 章定义
Coded-URL        = "<" absolute-URI ">"
                    ; Coded-URL 中允许非线性空白 (LAWS)
                    ; absolute-URI 在 RFC 3986, 第 4.3 章定义
```

响应中出现的这个通用标头指出: 资源支持按照规范指定的 DAV 模式和协议.
所有符合 DAV 规范的资源**必须[MUST]**在所有 OPTIONS 响应中返回带有
`compliance-class` 为 "1" 的 DAV 标头. 在服务器中只有一部分命名空间支持 WebDAV 的情况下,
对非 WebDAV 资源 (包括"/") 的 OPTIONS 请求**不应该[SHOULD_NOT]**宣称支持 WebDAV.

DAV 的值是资源支持的所有 `compliance-class` 标识符并使用逗号分隔的列表,
类标识符可以是 `Coded-URLs` 或 `token` (根据[RFC2616]定义). 标识符可以以任何顺序出现.
`token` 是通过 IETF RFC 过程标准化的标识符,
但其他标识符出于鼓励唯一性的目的**应该[SHOULD]**为 `Coded-URL`.

当资源显示其遵守对 `class 2` 或 `class 3` 合规, 则其必须显示对 `class 1` 合规.
一般来说，对一个合规类的支持并不意味着对其他任何合规类也支持, 并且, 特别的,
支持对 `class 3` 合规并不需要支持对 `class 2` 合规.
有关此规范中定义中对合规类的更多详细信息, 请参考[第 18 章][SECTION#18].
需要注意的是，许多 WebDAV 服务器在 "OPTIONS \*" 的响应中不会宣称支持 WebDAV.

作为一个请求标头, 此标头允许客户端在服务器需要该信息时宣称其具对命名功能的合规性.
除非标准化进城规范 (standards track specification) 需要, 否则客户端**不应[SHOULD_NOT]**发送此标头.
任何使用此标头作为请求标头的扩展都需要仔细考虑缓存该请求带来的影响.

## 10.2. Depth 标头

```bnf
Depth = "Depth" ":" ("0" | "1" | "infinity")
```

Depth 请求标头与在那些可能具有内部成员的资源上执行的方法一起使用,
以指示方法是否仅应用于资源本身 ("Depth: 0"), 或是资源及其内部成员 ("Depth: 1"),
亦或是资源及其所有成员 ("Depth: infinity").

Depth 标头只支持一下情况: 如果方法的定义明确提供了此类支持.

以下规则是在任意方法中支持 Depth 标头的默认行为.
方法可以通过在其定义中定义不同的行为来覆盖这些默认值.

支持 Depth 标头的方法可能选择不支持所有的标头值,
并可能会逐一例定义 (case by case) 方法在没有 Depth 标头下的行为.
e.g., MOVE 方法仅支持 "Depth: infinity", 如果没有 Depth 标头,
该方法会表现得好像使用 "Depth: infinity" 标头一样.

除非特定方法明确提供此类保证,
客户端**不能[MUST_NOT]**依赖于以任何特定顺序在其层次结构的成员上执行的方法或是执行原子化行为.

在执行过程中，带有 Depth 标头的方法将尽可能执行其分配的任务,
并返回一个可以指定它能够/未能完成哪些事情的响应.

因此, e.g., 尝试 COPY 层次结构可能会导致一些成员会被复制，而另一些则不会.

默认情况下，Depth 标头不与其他标头相互影响. 也就是说,
带有 Depth 标头的请求上的每个标头**必须[MUST]**仅能(在其适用于任何资源时)应用于 Request-URI,
除非为该标头定义了特定的 Depth 行为.

> 译者注: 怎么理解这句话, 假设存在一个集合 "/example", 内部包含多个资源, 此时客户端发送
> PROPFIND 请求:
>
> ```http
> PROPFIND /documents HTTP/1.1
> Host: example.com
> Depth: infinity
> ; If-None-Match 是一个条件查询标头, 假设其只会被应用于 "/documents" 集合的直接子资源.
> ; 也就是说, 在服务器没有特别规定 If-None-Match 的行为时(比如允许其被 Depth 标头影响),
> ; 资源 /documents/foo/bar 不会受到该标头影响
> If-None-Match: "12345"
> ; If-None-Match-Recursive 也是一个条件查询标头, 但是假设其可以被 Depth 标头影响
> ; 那么, 在请求 Depth 为无限深度时, 资源 /documents/foo/bar 便会收到该标头影响.
> If-None-Match-Recursive: "abcdef"
> ```

如果 Depth 标头范围内的源资源或目标资源被锁定, 从而阻止该方法成功执行,
那么(如果想让方法成功执行则)**必须[MUST]**在请求中的 If 标头头中提交该资源的锁令牌.

Depth 标头只指定方法对于内部成员的行为.
如果这个资源没有内部成员，则**必须[MUST]**忽略 Depth 标头.

## 10.3. Destination 标头

Destination 请求标头指定了 URI, 其标识了那些采用两个 URI 作为参数的方法
(如 COPY 和 MOVE) 的目标资源.

```bnf
Destination = "Destination" ":" Simple-ref
```

如果 Destination 的值是 absolute-URI (参见[RFC3986#4.3]),
其值可能指向不同的服务器 (或不同的端口或方案). 如果源服务器无法尝试将资源复制到远程服务器,
其**必须[MUST]**失败该请求. 需要注意的是,
将资源复制和移动到远程服务器在本规范中并没有完全定义 (e.g. 特定错误条件).

如果 Destination 的值过长或其他原因导致不可接受,
服务器**应该[SHOULD]**返回 400 (Bad Request) 状态码,
理想情况下可以在错误消息体中提供有帮助的信息.

## 10.4. If 标头

If 请求标头可以的与[RFC2616#14.24]中定义的 `If-Match` 标头提供类似的功能.
然而，If 标头头处理任何状态令牌以及 ETags. 状态令牌的典型示例是锁令牌,
锁令牌也是本规范中定义的唯一状态令牌.

### 10.4.1. 目的

If 标头头有两个不同的目的:

- 第一个目的是通过提供一系列状态列表来使请求具有条件性, 其中包含与特定资源的令牌和 ETags 匹配的条件.
  如果此标头经过评估且所有状态列表都失败了,
  则请求**必须[MUST]**失败并使用 412 (Precondition Failed) 状态码.
  另一方面，仅当描述的状态列表之一成功时, 请求才能成功.
  状态列表和匹配函数的成功标准在[第 10.4.3 章][SECTION#10.4.3]和[第 10.4.4 章][SECTION10.4.4]中定义.

- 此外, 一个事实是, 当状态令牌出现在 If 标头中时, 意味着其已随请求 "提交". 一般来说，
  这用于指示客户端具有该状态令牌信息.
  提交状态令牌的语义取决于其类型 (对于锁令牌，请参考[第 6 章][SECTION#6]).

需要注意的是，这两个目的需要区别对待:
对于状态令牌而言, 无论服务器是否实际评估其出现在的状态列表, 还是其表达的条件是否为真,
(状态令牌)都被视为已提交.

### 10.4.2. 语法

```bnf
If = "If" ":" ( 1*No-tag-list | 1*Tagged-list )

No-tag-list = List
Tagged-list = Resource-Tag 1*List

List = "(" 1*Condition ")"
Condition = ["Not"] (State-token | "[" entity-tag "]")
; entity-tag: see Section 3.11 of [RFC2616]
; No LWS allowed between "[", entity-tag and "]"
State-token = Coded-URL

Resource-Tag = "<" Simple-ref ">"
; Simple-ref: see Section 8.3
; No LWS allowed in Resource-Tag
```

语法区分了无标记列表 ("No-tag-list") 和标记列表 ("Tagged-list").
无标记列表适用于由 Request-URI 标识的资源,
而标记列表适用于由前面的 `Resource-Tag` 标识的资源.

`Resource-Tag` 适用于所有后续的列表, 直到下一个 `Resource-Tag`.

注意，If 标头中不能混合使用这两种列表类型. 这不是功能限制, 因为 `No-tag-list` 语法只是带有
`Resource-Tag` 引用 Request-URI 的 `Tagged-list` 产生式的一种简写表示法.

> 译者注: 举个例子, 以下两者都是对 `/documents/file.txt` 资源尝试加锁, 两者是等价的:
>
> ```http
> ; No-tag-list
> LOCK /documents/file.txt HTTP/1.1
> Host: example.com
> Depth: 0
> If: (<opaquelocktoken:>)
>
> ; Equivalent Tagged-list
> LOCK /documents/file.txt HTTP/1.1
> Host: example.com
> Depth: 0
> If: (<opaquelocktoken:/documents/file.txt>)
> ```

每个列表由一个或多个条件组成. 每个条件根据实体标记或状态令牌定义,
且可以通过前缀 "Not" 表示否定. (_译者注: 参考[第 10.4.7 章][SECTION#10.4.7]_)

注意，If 标头语法不允许在单个请求中使用多个 If 标头实例.
然而，HTTP 标头语法允许通过插入换行符后跟空格 (参见 [RFC2616#4.2]) 将单个标头值扩展到多行.

> 译者注: 多行语法举例
>
> ```http
> COPY /documents/file.txt HTTP/1.1
> Host: example.com
> Destination: /backup/file.txt
> If: (<opaquelocktoken:xxxxxxxxx>)
>     [(<etag:"yyyyyy">)
>     (<prop:displayname>"Hello World")]
> ```

### 10.4.3. List 评估

一个由单个实体标签或状态令牌组成的条件，仅当资源与描述的状态匹配时评估为真
(各个匹配函数在[第 10.4.4 章][SECTION#10.4.4]中定义).
加上前缀 "Not" 将反转评估结果 (因此，"Not" 仅适用于后续的实体标签或状态令牌).

每个 List 生成并描述一系列条件. 整个列表仅在每个条件均为真时才为真
(即列表表示条件的逻辑合取 (logical conjunction)).

每个 `No-tag-list` 和 `Tagged-list` 语法中可以包含一个或多个 List.
当且仅当所包含的中的任何一个为真时，List 才为真
(即存在多个 List, 该 List 序列表示列表的逻辑析取 (logical disjunction)).

最后，If 标头仅在 `No-tag-list` 或 `Tagged-list` 内包含的语句中至少一个为真时才为真.
如果标头评估为假, 服务器**必须[MUST]**返回 412 (Precondition Failed) 状态并拒绝请求.
其他情况下, 服务器可以如同 If 标头不存在一样继续执行请求.

### 10.4.4. 匹配状态令牌和 ETag

在处理 If 标头时, 匹配状态令牌或实体标签的定义如下:

- 识别资源 (Identifying a resource): 资源由 URI 和在标记列表语法中的令牌一起标识,
  或由无标记列表语法中的 Request-URI 标识.

- 匹配实体标签 (Matching entity tag): 当实体标签与标识资源相关联的实体标签匹配时,
  服务器**必须[MUST]**使用 [RFC2616#13.3.3] 中定义的弱比较或强比较函数进行匹配.

- 匹配状态令牌 (Matching state token):
  当 If 标头中的状态令牌与标识资源上的任何状态令牌完全匹配时. 如果资源位于锁范围内的任意位置,
  则认为该锁状态令牌匹配.

- 处理未映射的 URL (Handling unmapped URLs:): 对于 ETags 和状态令牌,
  都将该 URL 视为标识存在但没有指定状态的资源。

### 10.4.5. If 标头与不支持 DAV 的代理

不支持 DAV 的代理服务器不会遵循 If 标头, 因为其无法理解 If 标头, 并且 HTTP 要求忽略未理解的标头.
在与 HTTP/1.1 代理通信时, 客户端**必须[MUST]**使用 "Cache-Control: no-cache" 请求标头,
以防止代理服务器错误地尝试从缓存中处理请求.
在处理 HTTP/1.0 代理时, 出于同样的原因, 必须使用 "Pragma: no-cache" 请求标头.

### 10.4.6. 示例 - No-tag 语法规则

```http
If: (<urn:uuid:181d4fae-7d8c-11d0-a765-00a0c91e6bf2>
    ["I am an ETag"])
    (["I am another ETag"])
```

前面的标头要求使用指定锁令牌对 Request-URI 中标识的资源进行锁定,
并且处于由 ETag "I am an ETag" 标识的状态,
或者处于由第二个 ETag "I am another ETag" 标识的状态.

为了更清楚的说明问题, 可以将前面的 If 标头表示为以下条件:

```bnf
(
    is-locked-with(urn:uuid:181d4fae-7d8c-11d0-a765-00a0c91e6bf2)
    AND
    matches-etag("I am an ETag")
)
OR
(
    matches-etag("I am another ETag")
)
```

### 10.4.7. 示例 - No-tag 语法规则中使用 "Not"

```http
If: (Not <urn:uuid:181d4fae-7d8c-11d0-a765-00a0c91e6bf2>
    <urn:uuid:58f202ac-22cf-11d1-b12d-002035b29092>)
```

这个 If 标头要求资源不能被一个具有锁令牌为
`urn:uuid:181d4fae-7d8c-11d0-a765-00a0c91e6bf2` 的锁锁定,
并且必须被一个具有锁令牌为 `urn:uuid:58f202ac-22cf-11d1-b12d-002035b29092` 的锁锁定.

### 10.4.8. 示例 - 使条件评估始终为真

可能存在这样的情况, 客户端希望提交状态令牌, 但不希望仅仅因为该状态令牌不再是当前状态而导致请求失败.
一种简单的方法是包含一个已知的始终评估为真的条件, 如下所示：

```http
If: (<urn:uuid:181d4fae-7d8c-11d0-a765-00a0c91e6bf2>)
    (Not <DAV:no-lock>)
```

"DAV:no-lock" 是一个已知的永远不会代表当前的锁令牌. 锁令牌由服务器分配,
并遵循[第 6.5 章][SECTION#6.5]中描述的唯一性要求, 因此不能使用 "DAV:" 方案.
那么通过将 "Not" 应用于已知的不是当前状态的状态令牌时, 条件将始终评估为真.
因此, 整个 If 标头将始终评估为真, 且在任何情况下都将提交锁令牌
`urn:uuid:181d4fae-7d8c-11d0-a765-00a0c91e6bf2`.

### 10.4.11. 示例 - 在没有映射的 URL 上匹配 ETag

考虑一个不包含成员 `"/specs/rfc2518.doc"` 的集合 `"/specs"`. 在这种情况下,
如下所示的 If 标头部可能将会评估为假
(由于 URI 没有映射, 因此由 URI 标识的资源没有与 ETag "4217" 匹配的实体).

```http
If: </specs/rfc2518.doc> (["4217"])
```

另一方面, 如下所示的 If 标头将评估为真.

```http
If: </specs/rfc2518.doc> (Not ["4217"])
```

需要注意的是, 正如在[第 10.4.4 章][SECTION#10.4.4]中所定义的, 匹配状态令牌也需要进行相同的考虑.

### 10.5. Lock-Token 标头

```bnf
Lock-Token = "Lock-Token" ":" Coded-URL
```

Lock-Token 请求标头用于 UNLOCK 方法, 以标识要移除的锁.
Lock-Token 请求标头中的锁令牌**必须[MUST]**标识一个包含由 Request-URI 标识资源作为成员的锁.

Lock-Token 响应标头用于 LOCK 方法, 以指示由成功的 LOCK 请求创建的新锁的锁令牌.

### 10.6. Overwrite 标头

```bnf
Overwrite = "Overwrite" ":" ("T" | "F")
```

Overwrite 请求标头用于指定服务器在进行 COPY 或 MOVE 操作期间是否应该覆盖目标 URL 映射的资源.
值为 "F" 表示如果目标 URL 已经映射到资源, 则服务器**不能[MUST_NOT]**执行 COPY 或 MOVE 操作.
如果在 COPY 或 MOVE 请求中未包括 overwrite 标头,
则资源**必须[MUST]**将请求视为具有值为 "T" 的 overwrite 标头.
虽然 Overwrite 标头似乎与 `"If-Match: *"` 标头的功能重复 (参见[RFC2616]),
但 If-Match 仅适用于 Request-URI, 而不适用于 COPY 或 MOVE 的目标.

如果由于 Overwrite 标头的值导致未执行 COPY 或 MOVE,
方法**必须[MUST]**失败并返回 412 (Precondition Failed) 状态码.
服务器在检查该标头或任何条件标头之前**必须[MUST]**执行授权检查。

所有符合 DAV 的资源必须支持 Overwrite 标头.

### 10.7. Timeout 请求标头

```bnf
TimeOut = "Timeout" ":" 1#TimeType
TimeType = ("Second-" DAVTimeOutVal | "Infinite")
            ; No LWS allowed within TimeType
DAVTimeOutVal = 1*DIGIT
```

客户端**可能[MAY]**在 LOCK 请求中包含 Timeout 请求标头头.
但是, 服务器没有必要遵守或甚至考虑这些请求.
客户端在除 LOCK 方法之外的任何方法中都**不得[MUST_NOT]**提交 Timeout 请求标头.

`"Second-"` TimeType 指定了在服务器上从授予锁到自动解锁之间经过的秒数.
TimeType 中 "Second-" 的超时值不能大于 `2^32-1`.

有关锁超时行为的说明, 请参见[第 6.6 章][SECTION#6.6].
