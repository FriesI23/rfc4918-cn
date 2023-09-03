# 15. DAV 属性

对于 DAV 属性，属性名称与包含其值的 XML 元素名称相同. 在下面的章节中, 每章的最后一行使用
[REC-XML] 中定义的格式给出了元素类型声明. 其中 "Value" 字段 (如果存在) 使用 BNF 指定对
XML 元素允许内容的进一步限制 (i.e., 进一步限制 PCDATA 元素的值).

受保护属性 (protected property) 是指不能通过 PROPPATCH 请求更改的属性.
可能还有其他请求会导致受保护属性发生更改 (例如, 当 LOCK 请求影响 DAV:lockdiscovery
的值时). 需要注意的是, 给定属性可以在一种类型的资源上被保护, 但在另一种类型的资源上不被保护.

可计算属性 (computed property) 是指其值基于计算定义的属性 (基于该资源,
甚至是其他资源的内容和其他属性). 可计算属性始终是一个受保护属性.

COPY 和 MOVE 行为指的是本地 COPY 和 MOVE 操作.

对于基于 HTTP GET 响应标头 (`DAV:get*`) 定义的属性, 标头值可以包含如 [RFC2616#4.2]
中定义的 LWS (线性空白, Linear White Space). 服务器实现者在使用这些值作为 WebDAV
属性值之前, **应该** (SHOULD) 去除这些值中的 LWS.

## 15.1. creationdate 属性

- **名称**: creationdate
- **目的**: 记录资源创建的时间和日期
- **数值**: date-time (在 [RFC3339#5.6] 中关于 ABNF 的定义)
- **保护**: **可能** (MAY) 是受保护的. 某些服务器允许修改 DAV:creationdate
  以反映文档创建的时间, 如果这个时间对用户来说是更有意义的 (而不是使用上传的时间). 因此,
  客户端**不应** (SHOULD NOT) 在同步逻辑中使用这个属性 (应该使用 DAV:getetag).
- **COPY/MOVE 行为**: 此属性值**应该** (SHOULD) 在 MOVE 操作期间保持不变,
  但该值通常在使用 COPY 创建资源时被重新初始化. 不应在使用 COPY 时设置它.
- **描述**: DAV:creationdate 属性应该在所有符合 DAV 规范的资源上定义. 如果该属性存在,
  应包含资源创建的时间戳. 无法持久记录创建日期的服务器**应该** (SHOULD) 保留该值为未定义的
  (i.e., 回报为 "Not Found").

```xml
<!ELEMENT creationdate (#PCDATA) >
```

## 15.2. displayname 属性

- **名称**: displayname
- **目的**: 为资源提供适合呈现给用户的名称.
- **数值**: 任意文本.
- **保护**: **不应** (SHOULD NOT) 受保护. 需要注意的是, 实现 [RFC2518]
  的服务器可能将此属性设置为受保护的, 由于这是一个新的要求.
- **COPY/MOVE 行为**: 在 COPY 和 MOVE 操作中**应该** (SHOULD) 保留该属性值.
- **描述**: 包含适合展示给用户的资源描述. 此属性在资源上定义, 并且因此**应该** (SHOULD)
  具有独立于检索它的 Request-URI 的相同的值 (因此, 基于 Request-URI
  计算此属性的方式已被弃用). 虽然那些通用客户端可能会向终端用户显示属性值, 但客户端 UI
  设计师必须理解的是: 用于标识资源的方法仍然是 URL. 对 DAV:displayname
  的更改不会向服务器发出移动或复制请求, 而只是在各个资源上更改元数据. 即使在同一集合中，
  两个资源也可以具有相同的 DAV:displayname 值.

```xml
<!ELEMENT displayname (#PCDATA) >
```

## 15.3. getcontentlanguage 属性

- **名称**: getcontentlanguage
- **目的**: 包含 Content-Language 标头值 (来自[RFC2616#14.12])，就像在没有 accept
  标头的情况下执行 GET 请求时返回时一样.
- **数值**: language-tag (language-tag 在[RFC2616#3.10])
- **保护**: **不应** (SHOULD NOT) 受保护, 因此客户端可以重置该语言. 需要注意的是,
  实现 [RFC2518] 的服务器可能会将其作为受保护属性, 因为这是一个新的要求.
- **COPY/MOVE 行为**: 在 COPY 和 MOVE 操作中, **应该** (SHOULD) 保留此属性值.
- **描述**: DAV:getcontentlanguage 属性**必须** (MUST) 在 (任何返回 GET 请求中包含
  Content-Language 标头的) DAV 兼容资源上定义.

```xml
<!ELEMENT getcontentlanguage (#PCDATA) >
```

## 15.4. getcontentlength 属性

- **名称**: getcontentlength
- **目的**: 包含通过 GET 请求 (不包含 accept 标头) 返回的 Content-Length 标头.
- **数值**: 参考[RFC2616#14.13].
- **保护**: 该属性是经过计算得出的，因此受到保护.
- **描述**: DAV:getcontentlength 属性**必须** (MUST) 定义在任何在 GET 请求中返回
  Content-Length 标头的 DAV 兼容的资源上.
- **COPY/MOVE 行为**: 此属性值取决于目标资源的大小, 而不是源资源上的属性值.

```xml
<!ELEMENT getcontentlength (#PCDATA) >
```

## 15.5. getcontenttype 属性

- **名称**: getcontenttype
- **目的**: 包含通过 GET 请求 (不包含 accept 标头) 返回的 Content-Type 标头值
  (参见[RFC2616#14.17]).
- **数值**: media-type (在[RFC2616#3.7]中定义).
- **保护**: 如果服务器更倾向于自行分配内容类型, 则有可能受保护 (见[第 9.7.1 章]中的讨论).
- **COPY/MOVE 行为**: 属性值**应该** (SHOULD) 在 COPY 和 MOVE 操作中保留.
- **描述**：此属性**必须** (MUST) 在 (返回 GET 请求中包含 Content-Language 标头的)
  DAV 兼容资源上定义.

```xml
<!ELEMENT getcontenttype (#PCDATA) >
```

## 15.6. getetag 属性

- **名称**: getetag
- **用途**: 包含 ETag 标头的值 (来自[RFC2616#14.19]), 就如返回一个没有 accept 标头的
  GET 那样.
- **数值**: entity-tag (在[RFC2616#3.11]中定义)
- **保护**: **必须** (MUST) 是受保护的, 因为该值由服务器创建和控制.
- **COPY/MOVE 行为**: 此属性值取决于目标资源的最终状态, 而不是源资源上属性的值.
  另需要注意[第 8.8 章]()中的考虑事项.
- **描述**: 在任何返回 Etag 标头的 DAV 兼容资源上都**必须** (MUST) 定义 getetag 属性.
  请参阅 [RFC2616#3.11] 中有关 ETag 语义的完整定义, 并参阅[第 8.6 章]()中关于 WebDAV
  中 ETag 的讨论.

```xml
<!ELEMENT getetag (#PCDATA) >
```
