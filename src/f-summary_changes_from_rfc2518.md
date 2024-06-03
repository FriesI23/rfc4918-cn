# 与 RFC2518 的总体变更

本章列出了本文档与 [RFC2518] 之间的主要变更, 首要的便是可能导致实施发生变化的变更.
服务器将通过在 `DAV` 响应标头中返回合规类 `3` 来宣城对本规范中所有变更的支持
(请参阅[第 10.1 节][SECTION#10.1]和[第 18.3 节][SECTION#18.3]).

## F.1. 客户端与服务器实现的变更

### F.1.1. 集合和命名空间操作

- PROPFIND 方法中 `allprop` ([第 9.1 节][SECTION#9.1]) 的语义已被放宽,
  现在服务器的返回结果至少包括本规范中定义的活属性, 但不一定包含其他活属性.
  因此, `allprop` 现在更像 "返回请求 `allprop` 时应该返回的所有属性",
  这组属性可能包含自定义属性与其他规范中定义的属性 (这些规范有此要求).
  与此相关的是, 现在可以使用 `include` 语法扩展 `allprop` 请求, 以包含特定名称的属性,
  从而避免由于 `allprop` 语义变化而导致的额外请求.

- 服务器现在可以拒绝 带有 `Depth: Infinity` 的PROPFIND 请求.
  使用此选项的客户端需要改为执行一系列 `Depth:1` 的请求.

- `Multi-Status` 响应体现在可以在新的 `location` 元素中传输 HTTP 的 `Location` 响应标头的值.
  客户端可以利用这一点来避免在处理带有 3xx 状态的 `response` 元素时需要进行额外的请求
  (见[第 14.24 节][SECTION#14.24]).

- COPY 的定义已被放宽, 现在不再要求服务器先删除目标资源 (这在[RFC3253]中是已知的不兼容性).
  见[第 9.8 节][SECTION#9.8]).

### F.1.2. 标头和封装

- 除完整的URI外, `Destination` 和 `If` 请求标头现在允许使用绝对路径 (见[第 8.3 节][SECTION#8.3]).
  这对于通过反向代理操作的客户端可能很有用, 这些代理会重写 `Host` 请求标头, 但不会重写 WebDAV 特有的标头.

- 本规范采用了 [RFC3253] 中定义的错误扩展和 "前置条件/后置条件" 术语 (见[第 16 节][SECTION#16]).
  与此相关的是, 在多状态响应正文中添加了 `error` XML元素
  (见[第 14.5 节][SECTION#14.5]，但注意其格式不同于 [RFC3253] 中推荐的格式).

- 发送与接收方现在必须支持 XML 消息这种中的 UTF-16 字符编码 (见[第 19 节][SECTION#19]).

- 客户端现在要求在 PROPFIND 请求中发送 `Depth` 标头, 尽管标准仍鼓励服务器支持那些未发送该标头的客户端.

### F.1.3. 锁定

- [RFC2518] 的 "锁空资源"（LNRs）概念已被简化为 "空锁定资源" (见[第 7.3 节][SECTION#7.3]).
  客户端不能再依赖某些 LNRs 的功能,
  即 "使用 LOCK 创建锁定集合, 或在未发出 PUT 或 MKCOL 请求时, 资源会在 UNLOCK 后消失" 这一事实.
  请注意，服务器仍然可以按照 [RFC2518] 实现 LNRs.

- 锁不再隐式刷新, 而是仅在明确请求时刷新 (见[第 9.10.2 节][SECTION#9.10.2]).

- 明确规定在 LOCK 请求中提供的 `DAV` 值必须像死属性一样由服务器永久保存 (见[第 14.17 节][SECTION#14.17]).
  还添加了 `DAV:lockroot` 元素 (见[第 14.12 节][SECTION#14.12]), 该元素允许客户端发现锁根目录.

## F.2. 服务器实现的变更

### F.2.1. 集合和命名空间操作

- 由于互操作性问题, 多状态响应中 `href` 元素锁内容的允许格式已被限制 (见[第 8.3 节][SECTION#8.3]).

- 由于实现缺乏, COPY 和 MOVE 请求正文中的 `propertybehavior` 已被删除.
  取而代之的是明确了属性保留的要求 (见[第 9.8 和 9.9 节][SECTION#9.8]).

### F.2.2. 属性

- 增强对服务器存储的属性值, 特别是对语言信息 (`xml:lang`), 空格和 XML 命名空间信息的持久性
  (见[第 4.3 节][SECTION#4.3]).

- 明确了哪些属性应可由客户端写入;特别是，服务器应支持设置 `DAV:displayname` (见[第 15 节][SECTION#15]).

- 只有 [`rfc1123-date`](z-typedefs.md#rfc1123-date) 格式的值才是 `DAV:getlastmodified` 的合法值
  (见[第 15.7 节][SECTION#15.7]).

### F.2.3. 标头和封装

- 服务器现在必须在处理条件标头前进行授权检查 (见[第 8.5 节][SECTION#8.5]).

### F.2.4. 锁定

- 增强访问被锁定资源时检查锁创建者身份这一要求 (见[第 6.4 节][SECTION#6.4]).
  客户端需要注意, 返回给其他主体的锁令牌只能用于解除锁定 (如果可以的话).

## F.3. 其他变更

集合状态的定义已被修正, 不再根据 `Reqeust-URI` 变化 (见[第 5.2 节][SECTION#5.2]).

由于缺乏实现实践, 已删除了在[RFC2518#6.4]中引入的 `DAV:source` 属性.

现在 DAV 标头, 除兼容性类标记外, 允许通过 URI 使用非 IETF 扩展. DAV 标头现在也可以用于请求,
尽管本规范未定义 (此处定义的) 兼容性类的相关语义 (见[第 10.1 节][SECTION#10.1]).

[RFC2518#9.2] 中的 `Depth` 标头的定义要求: 在默认情况下, 请求标头将应用于范围内的每个资源.
根据实践经验, 现已将默认设置反转（见[第 10.2 节][SECTION#10.2]).

由于缺乏实践, HTTP 状态码 102（[RFC2518#10.1]）和 `Status-URI` 响应标头 ([RFC2518#9.7]) 的定义已被删除.

`Timeout` 请求标头中使用的 [`TimeType`](z-typedefs.md#timeout) 格式和 `timeout` XML元素曾经是可扩展的.
现在只允许使用此规范中定义的两种格式 (见[第 10.7 节][SECTION#10.7]).

<!-- refs -->

[SECTION#4.3]: 4-data_model_for_resource_properties.md#43-属性值
[SECTION#5.2]: 5-collection_of_web_resources.md#52-集合资源
[SECTION#6.4]: 6-locking#64-锁创建者和权限
[SECTION#7.3]: 7-write_lock.md#73-写锁与未映射-url
[SECTION#8.3]: 8-general_request_and_response_handling.md#83-处理-url
[SECTION#8.5]: 8-general_request_and_response_handling.md#85-用于-webdav-的-http-标头
[SECTION#9.1]: 9-http_methods_for_distributed_authoring.md#91-propfind-方法
[SECTION#9.8]: 9-http_methods_for_distributed_authoring.md#98-copy-方法
[SECTION#9.10.2]: 9-http_methods_for_distributed_authoring.md#9102-刷新锁
[SECTION#10.1]: 10-http_headers_for_distributed_authoring.md#101-dav-标头
[SECTION#10.2]: 10-http_headers_for_distributed_authoring.md#102-depth-标头
[SECTION#10.7]: 10-http_headers_for_distributed_authoring.md#107-timeout-请求标头
[SECTION#14.5]: 14-xml_element_definitions.md#145-error-xml-元素
[SECTION#14.12]: 14-xml_element_definitions.md#142-allprop-xml-元素
[SECTION#14.17]: 14-xml_element_definitions.md#147-href-xml-元素
[SECTION#14.24]: 14-xml_element_definitions.md#1424-response-xml-元素
[SECTION#15]: 15-dav_properties.md
[SECTION#15.7]: 15-dav_properties.md#157-157-getlastmodified-属性
[SECTION#16]: 16-precondition_postcondition_xml_elements.md
[SECTION#18.3]: 18-dav_compliance_classes.md#183-class-3类别-3
[SECTION#19]: 19-internationalization_considerations.md
