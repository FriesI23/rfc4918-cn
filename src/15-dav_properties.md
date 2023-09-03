# 15. DAV 属性

对于 DAV 属性，属性名称与包含其值的 XML 元素名称相同. 在下面的章节中,
每章的最后一行使用 [REC-XML] 中定义的格式给出了元素类型声明.
其中 "Value" 字段 (如果存在) 使用 BNF 指定对 XML 元素允许内容的进一步限制
(i.e., 进一步限制 PCDATA 元素的值).

受保护属性 (protected property) 是指不能通过 PROPPATCH 请求更改的属性.
可能还有其他请求会导致受保护属性发生更改
(例如, 当 LOCK 请求影响 DAV:lockdiscovery 的值时).
需要注意的是, 给定属性可以在一种类型的资源上被保护, 但在另一种类型的资源上不被保护.

可计算属性 (computed property) 是指其值基于计算定义的属性
(基于该资源, 甚至是其他资源的内容和其他属性). 可计算属性始终是一个受保护属性.

COPY 和 MOVE 行为指的是本地 COPY 和 MOVE 操作.

对于基于 HTTP GET 响应标头 (`DAV:get*`) 定义的属性,
标头值可以包含如 [RFC2616#4.2] 中定义的 LWS (线性空白, Linear White Space).
服务器实现者在使用这些值作为 WebDAV 属性值之前, **应该[SHOULD]**去除这些值中的 LWS.

## 15.1. creationdate 属性

- **名称**: creationdate
- **目的**: 记录资源创建的时间和日期
- **数值**: date-time (在 [RFC3339#5.6] 中关于 ABNF 的定义)
- **保护**: **可能[MAY]**是受保护的.
  某些服务器允许修改 DAV:creationdate 以反映文档创建的时间,
  如果这个时间对用户来说是更有意义的 (而不是使用上传的时间).
  因此, 客户端**不应[SHOULD_NOT]**在同步逻辑中使用这个属性 (应该使用 DAV:getetag).
- **COPY/MOVE 行为**: 此属性值**应该[SHOULD]**在 MOVE 操作期间保持不变,
  但该值通常在使用 COPY 创建资源时被重新初始化. 不应在使用 COPY 时设置它.
- **描述**: DAV:creationdate 属性应该在所有符合 DAV 规范的资源上定义. 如果该属性存在,
  应包含资源创建的时间戳. 无法持久记录创建日期的服务器**应该[SHOULD]**保留该值为未定义的
  (i.e., 回报为 "Not Found").

```bnf
<!ELEMENT creationdate (#PCDATA) >
```

## 15.2. displayname 属性

- **名称**: displayname
- **目的**: 为资源提供适合呈现给用户的名称.
- **数值**: 任意文本.
- **保护**: **不应[SHOULD_NOT]**受保护. 需要注意的是,
  实现 [RFC2518] 的服务器可能将此属性设置为受保护的, 由于这是一个新的要求.
- **COPY/MOVE 行为**: 在 COPY 和 MOVE 操作中**应该[SHOULD]**保留该属性值.
- **描述**: 包含适合展示给用户的资源描述. 此属性在资源上定义,
  并且因此**应该[SHOULD]** 具有独立于检索它的 Request-URI 的相同的值
  (因此, 基于 Request-URI 计算此属性的方式已被弃用).
  虽然那些通用客户端可能会向终端用户显示属性值, 但客户端 UI 设计师必须理解的是:
  用于标识资源的方法仍然是 URL. 对 DAV:displayname 的更改不会向服务器发出移动或复制请求,
  而只是在各个资源上更改元数据.
  即使在同一集合中，两个资源也可以具有相同的 "DAV:displayname" 值.

```bnf
<!ELEMENT displayname (#PCDATA) >
```

## 15.3. getcontentlanguage 属性

- **名称**: getcontentlanguage
- **目的**: 包含 Content-Language 标头值 (来自 [RFC2616#14.12]),
  就像在没有 accept 标头的情况下执行 GET 请求时返回时一样.
- **数值**: language-tag (language-tag 在 [RFC2616#3.10])
- **保护**: **不应[SHOULD_NOT]**受保护, 因此客户端可以重置该语言.
  需要注意的是, 实现 [RFC2518] 的服务器可能会将其作为受保护属性, 因为这是一个新的要求.
- **COPY/MOVE 行为**: 在 COPY 和 MOVE 操作中, **应该[SHOULD]**保留此属性值.
- **描述**: DAV:getcontentlanguage 属性**必须[MUST]**在 (任何返回 GET 请求中包含
  Content-Language 标头的) DAV 兼容资源上定义.

```bnf
<!ELEMENT getcontentlanguage (#PCDATA) >
```

## 15.4. getcontentlength 属性

- **名称**: getcontentlength
- **目的**: 包含通过 GET 请求 (不包含 accept 标头) 返回的 Content-Length 标头.
- **数值**: 参考 [RFC2616#14.13].
- **保护**: 该属性是经过计算得出的，因此受到保护.
- **描述**: DAV:getcontentlength 属性**必须[MUST]**定义在任何在 GET 请求中返回
  Content-Length 标头的 DAV 兼容的资源上.
- **COPY/MOVE 行为**: 此属性值取决于目标资源的大小, 而不是源资源上的属性值.

```bnf
<!ELEMENT getcontentlength (#PCDATA) >
```

## 15.5. getcontenttype 属性

- **名称**: getcontenttype
- **目的**: 包含通过 GET 请求 (不包含 accept 标头) 返回的 Content-Type 标头值
  (参见[RFC2616#14.17]).
- **数值**: media-type (在[RFC2616#3.7]中定义).
- **保护**: 如果服务器更倾向于自行分配内容类型, 则有可能受保护
  (见[第 9.7.1 章][SECTION#9.7.1]中的讨论).
- **COPY/MOVE 行为**: 属性值**应该[SHOULD]**在 COPY 和 MOVE 操作中保留.
- **描述**：此属性**必须[MUST]**在 (返回 GET 请求中包含 Content-Language 标头的)
  DAV 兼容资源上定义.

```bnf
<!ELEMENT getcontenttype (#PCDATA) >
```

## 15.6. getetag 属性

- **名称**: getetag
- **用途**: 包含 ETag 标头的值 (来自 [RFC2616#14.19]),
  就如返回一个没有 accept 标头的 GET 那样.
- **数值**: entity-tag (在 [RFC2616#3.11] 中定义)
- **保护**: **必须[MUST]**是受保护的, 因为该值由服务器创建和控制.
- **COPY/MOVE 行为**: 此属性值取决于目标资源的最终状态, 而不是源资源上属性的值.
  另需要注意[第 8.8 章][SECTION#8.8]中的考虑事项.
- **描述**: 在任何返回 Etag 标头的 DAV 兼容资源上都**必须[MUST]**定义 getetag 属性.
  请参阅 [RFC2616#3.11] 中有关 ETag 语义的完整定义,
  并参阅[第 8.6 章][SECTION#8.6]中关于 WebDAV 中 ETag 的讨论.

```bnf
<!ELEMENT getetag (#PCDATA) >
```

## 15.7. 15.7. getlastmodified 属性

- **名称**: getlastmodified
- **目的**: 包含 Last-Modified 标头的值 (来自 [RFC2616#14.19]), 就如返回一个没有
  accept 标头的 GET 那样.
- **数值**: rfc1123-date (在 [RFC2616#3.3.1] 中定义)
- **保护**: **应该[SHOULD]**受保护, 因为某些客户端可能依赖该值来进行适当的缓存行为,
  或依赖与此属性关联的 Last-Modified 标头的值.
- **COPY/MOVE 行为**: 此属性值依赖于目标资源的最后修改日期, 而不是源资源的属性值.
  需要注意的是, 某些服务器的实现是使用文件系统的修改日期值来设置 DAV:getlastmodified 值,
  并且可以在 MOVE 操作中保留该值, 即使 HTTP Last-Modified 值**应该[SHOULD]**被修改.
  主要注意的是, 由于 [RFC2616] 要求客户端使用服务器提供的 ETags,
  因此实现 ETags 的服务器可以依赖客户端使用比修改日期更好的机制进行离线同步或缓存控制.
  同时注意[第 8.8 章][SECTION#8.8]中的考虑事项.
- **描述**: 资源的最后修改日期**应该[SHOULD]**仅反映资源正文 (GET 响应) 的更改.
  仅更改属性**不应[SHOULD_NOT]**导致最后修改日期的更改,
  因为客户端可能依赖最后修改日期来知道何时覆盖现有正文.
  DAV:getlastmodified 属性**必须[MUST]**在任何 (支持在 GET 响应中返回
  Last-Modified 标头的) DAV 兼容资源中定义。

```bnf
<!ELEMENT getlastmodified (#PCDATA) >
```

## 15.8. lockdiscovery 属性

- **名称**: lockdiscovery
- **目的**: 描述资源上的活动锁 (active locks).
- **保护**: **必须[MUST]**受保护.
  客户端通过 LOCK 和 UNLOCK (而不是通过 PROPPATCH) 更改锁列表.
- **COPY/MOVE 行为**: 此属性的值取决于目标锁的状态, 而不取决于源资源锁的状态.
  需要注意的是, 锁不会在 MOVE 操作中发生移动.
- **描述**: 返回有关谁拥有锁, 拥有的锁的类型, 超时类型与超时剩余时间, 以及相关锁令牌的列表.
  所有者信息**可能[MAY]**由于考虑到敏感信息而被省略. 如果没有锁, 但服务器支持锁,
  那么属性将存在但包含零个 "activelock" 元素. 如果存在一或多个锁,
  将为资源上的每个锁显示一个 "activelock" 元素.
  此属性对于写锁[第 7 章][SECTION#7]而言**不可[NOT]**锁定.

```bnf
<!ELEMENT lockdiscovery (activelock)* >
```

## 15.8.1。示例 - 检索 DAV:lockdiscovery

```xml
>>Request

PROPFIND /container/ HTTP/1.1
Host: www.example.com
Content-Length: xxxx
Content-Type: application/xml; charset="utf-8"

<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D='DAV:'>
  <D:prop><D:lockdiscovery/></D:prop>
</D:propfind>

>>Response

HTTP/1.1 207 Multi-Status
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:multistatus xmlns:D='DAV:'>
  <D:response>
    <D:href>http://www.example.com/container/</D:href>
    <D:propstat>
      <D:prop>
        <D:lockdiscovery>
          <D:activelock>
            <D:locktype><D:write/></D:locktype>
            <D:lockscope><D:exclusive/></D:lockscope>
            <D:depth>0</D:depth>
            <D:owner>Jane Smith</D:owner>
            <D:timeout>Infinite</D:timeout>
            <D:locktoken>
              <D:href>urn:uuid:f81de2ad-7f3d-a1b2-4f3c-00a0c91a9d76</D:href>
            </D:locktoken>
            <D:lockroot>
              <D:href>http://www.example.com/container/</D:href>
            </D:lockroot>
          </D:activelock>
        </D:lockdiscovery>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
  </D:response>
</D:multistatus>
```

该资源具有一个带有无限超时的排他写锁 (exclusive write lock).

## 15.9. resourcetype 属性

- **名称**: resourcetype
- **目的**: 指定资源的性质
- **保护**: **应该[SHOULD]**受保护.
  通常资源类型是通过创建资源（MKCOL vs PUT）的操作 (而不是 PROPPATCH) 来确定的.
- **COPY/MOVE 行为**: 对资源的 COPY/MOVE 通常会导致在目标位置上有相同类型的资源.
- **描述**: **必须[MUST]**在所有符合 DAV 规范的资源上定义.
  每个子元素标识资源所属的特定类型, 例如 "collection",
  这是此规范中定义的唯一资源类型 (参考[第 14.3 章][SECTION#14.3]).
  如果元素包含 "collection" 子元素加上其他无法识别的元素, 通常应将其视为集合.
  如果元素不包含已识别的子元素, 则应将其视为非集合资源.
  默认值为空. 此元素**不得[MUST_NOT]**包含文本或混合内容.
  任何自定义子元素都会考虑被视为资源类型的标识符.
- **示例**: (虚构示例, 用于展示其可扩展性)

  ```xml
  <x:resourcetype xmlns:x="DAV:">
    <x:collection/>
    <f:search-results xmlns:f="http://www.example.com/ns"/>
  </x:resourcetype>
  ```

<!-- below are refs and links -->

## 15.10. supportedlock 属性

- **名称**: supportedlock
- **目的**: 提供资源支持的锁定功能列表.
- **保护**: **必须[MUST]**受保护. 服务器 (而不是客户端) 决定哪些锁机制收到支持.
- **COPY/MOVE 行为**: 该属性的值取决于目标支持的锁类型, 而不是源资源的属性值.
  因此, 服务器在 COPY 到目标位置时不应尝试设置此属性.
- **描述**: 返回一个列表组合, 其内包含在资源上可以指定的锁请求中可能出现的锁范围和访问类型.
  需要注意的是, 实际内容本身受限与访问控制, 因此服务器无需提供客户端无权查看的信息.
  此属性对于写锁[第 7 章][SECTION#7]而言**不可** (NOT) 锁定.

```bnf
<!ELEMENT supportedlock (lockentry)* >
```

## 15.10.1. 示例 - 检索 DAV:supportedlock

```xml
>>Request

PROPFIND /container/ HTTP/1.1
Host: www.example.com
Content-Length: xxxx
Content-Type: application/xml; charset="utf-8"

<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:">
  <D:prop><D:supportedlock/></D:prop>
</D:propfind>

>>Response

HTTP/1.1 207 Multi-Status
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:multistatus xmlns:D="DAV:">
  <D:response>
    <D:href>http://www.example.com/container/</D:href>
    <D:propstat>
      <D:prop>
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
