# 16. 前置条件/​​ 后置条件 XML 元素

正如[第 8.7 章][SECTION#8.7]中的介绍, 可以在很多状态响应正文中包含有关错误条件的额外信息.
本章对错误正文机制的使用提出要求, 并引入了一些前置条件和后置条件码.

方法的 "前置条件" 描述了要执行该方法必须满足的服务器状态.
方法的 "后置条件" 描述了该方法完成后必须为真的服务器状态.

每个前置条件和后置条件都有一个与之关联的唯一 XML 元素. 在 207 多状态响应中,
XML 元素必须出现在适当的 "propstat" 或 "response" 元素内的 "error" 元素中,
具体取决于该条件是否适用于一个或多个属性, 或整个资源中. 在使用此规范的其他所有错误响应中,
前置条件/后置条件 XML 元素**必须[MUST]**作为响应正文中顶级 "error" 元素的子元素返回,
除非请求另行协商, 同时伴有适当的响应状态. 如果请求不应重复,
最常见的响应状态码是 403 (Forbidden), 因为其将总是失败,
以及如如果预期用户能够解决冲突并重新提交请求, 则返回 409 (Conflict).
"error" 元素**可能[MAY]**是包含具体错误信息的子元素,
也**可能[MAY]**使用任何自定义子元素进行扩展.

该机制不能取代这里或 HTTP 中定义的正确数字状态码, 因为客户端必须始终能根据数字码采取合理行为.
然而, 它确实消除了定义新数字码的需求.
用于此目的的新的机器码被分类为前置条件和后置条件的 XML 元素, 因此,
任何定义新条件码的组都可以自然的使用自己的命名空间.
一如既往的, "DAV:" 命名空间被保留供 IETF 特许 (IETF-chartered) 的 WebDAV 工作组使用.

支持此规范的服务器在违反本文档中定义的前置条件或后置条件时, **应该[SHOULD]**使用 XML 错误.
对于本文档中未指定的错误条件, 服务器**可以[MAY]**简单选择适当的数字状态, 并保持响应正文为空.
然而, 服务器也**可能[MAY]**使用自定义条件代码和其他支持文本,
因为即使客户端不能自动识别条件代码，它们在互操作性的测试和调试中仍非常有用.

## 16.1. 示例 - 带前置条件码的响应

```xml
>>Response

HTTP/1.1 423 Locked
Content-Type: application/xml; charset="utf-8"
Content-Length: xxxx

<?xml version="1.0" encoding="utf-8" ?>
<D:error xmlns:D="DAV:">
    <D:lock-token-submitted>
        <D:href>/workspace/webdav/</D:href>
    </D:lock-token-submitted>
</D:error>
```

在该示例中, 一个不清楚父集合 `"/workspace/webdav/"` 上深度无限锁的客户端尝试修改集合成员
`"/workspace/webdav/proposal.doc"`.

一些其他有用的前置条件和后置条件已经在其扩展 WebDAV 规范中定义,
例如 [RFC3744] (特别是[RFC3744#7.1.1]), [RFC3253] 和 [RFC3648].

所有这些元素都位于 "DAV:" 命名空间中. 如果没有另行指定, 每个条件的 XML 元素的内容被定义为空.

## 16.2. 前置条件 - lock-token-matches-request-uri XML 元素

- **名称**: `lock-token-matches-request-uri`
- **配合使用**: 409 Conflict
- **条件**: 前置条件
- **目的**: 请求可以包括一个 Lock-Token 标头, 用于标识 UNLOCK 方法的一个锁.
  然而, 如果 Request-URI 不在令牌标识锁的范围内时, 服务器**应该[SHOULD]**使用此错误.
  锁的范围可能不包括 Request-URI, 或是锁可能已经不存在, 或是令牌可能无效.

## 16.3. 前置条件 - lock-token-submitted XML 元素

- **名称**: `lock-token-submitted`
- **配合使用**: 423 Locked
- **条件**: 前置条件
- **目的**: 请求无法成功, 因为应该提交一个锁令牌. 如果该元素存在,
  则**必须[MUST]**至少包含一个阻止请求的锁资源 URL.
  在涉及集合锁的 MOVE, COPY 和 DELETE 情况下,
  客户端可能很难找出哪个被锁定的资源导致请求失败 - 但服务器只负责返回一个这样的被锁定资源.
  如果服务器知道所有阻止请求成功的被锁定资源, 则**可以[MAY]**全部返回.

```bnf
<!ELEMENT lock-token-submitted (href+) >
```

## 16.4. 前置条件 - no-conflicting-lock XML 元素

- **名称**: `no-conflicting-lock`
- **配合使用**: 通常为 423 Locked
- **分类**: 前置条件
- **目的**: 一个 LOCK 请求由于存在冲突锁定从而导致请求失败. 需要注意的是,
  即使被请求的资源只是被间接锁定, 锁仍然可能存在冲突. 在这种情况下,
  前置条件码可以用于通知客户端有关导致冲突锁定的根资源, 避免单独查找 "lockdiscovery" 属性.

```bnf
<!ELEMENT no-conflicting-lock (href)* >
```

## 16.5. 前置条件 - no-external-entities XML 元素

- **名称**: `no-external-entities`
- **配合使用**: 403 Forbidden
- **分类**: 前置条件
- **目的**: 如果服务器因为请求正文包含外部实体而拒绝客户端请求,
  则服务器**应该[SHOULD]**使用此错误.

## 16.6. 后置条件 - preserved-live-properties XML 元素

- **名称**: `preserved-live-properties`
- **配合使用**: 409 Conflict
- **分类**: 后置条件
- **目的**: 服务器收到一个其他情况下有效的 MOVE 或 COPY 请求,
  但无法在目标位置保持活属性行为相同. 这可能是服务器只在部分存储库中支持一些活属性,
  或者仅仅是产生了一个内部错误.

## 16.7. 前置条件 - propfind-finite-depth XML 元素

- **名称**: `propfind-finite-depth`
- **配合使用**: 403 Forbidden
- **分类**: 前置条件
- **目的**: 此服务器不允许对集合进行无限深度的 PROPFIND 请求.

## 16.8. 前置条件 - cannot-modify-protected-property XML 元素

- **名称**: `cannot-modify-protected-property`
- **配合使用**: 403 Forbidden
- **分类**: 前置条件
- **目的**: 客户端尝试在 PROPPATCH 中设置受保护的属性 (比如 `DAV:getetag`).
  另请参见 [RFC3253#3.12].

<!-- refs -->

[SECTION#8.7]: 8-general_request_and_response_handling.md#87-包含错误响应的正文
