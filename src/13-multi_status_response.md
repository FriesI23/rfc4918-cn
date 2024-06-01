# 13. 多状态响应

> [原文](https://datatracker.ietf.org/doc/html/rfc4918#section-13)

一个多状态响应用于在多个资源中可能适用多个状态码的情况下传递信息. 默认的多状态响应正文是一个带有
`multistatus` 根元素的 `text/xml` 或 `application/xml` HTTP 实体.
其他包含 `200`, `300`, `400` 和 `500` 系列状态码的元素在方法调用期间生成.
`100` 系列状态码**不应[SHOULD_NOT]**记录在 `response` XML 元素里.

尽管 `207` 被用作整体的响应状态码, 接收者仍需参考多状态响应正文内容以获取方法执行成功或失败的进一步信息.
该响应**可能[MAY]**用于成功、部分成功以及失败的情况.

`multistatus` 根元素以任意顺序包含零或多个 `response` 元素, 每个元素都包含与之相关的信息.
每个 `response` 元素**必须[MUST]**有一个标识该资源的 `href` 元素.

多状态响应有两种不同的格式来表示状态:

1. `status` 元素作为 `response` 元素的子元素, 表示所识别资源的消息执行的整体状态
   (具体参见[第 9.6.2 章][SECTION#9.6.2]. 一些方法定义提供了有关客户端应准备接收的特定状态码信息.
   然而, 客户端**必须[MUST]**能够使用 [RFC2616#10] 中定义的通用规则处理其他状态码.
2. 对于 PROPFIND 和 PROPPATCH, 格式扩展使用 `propstat` 元素 (而不是 `status` 元素)
   来提供有关资源中各个属性的信息. 此格式只针对 PROPFIND 和 PROPPATCH,
   并在[第 9.1 章][SECTION#9.1]]和[第 9.2 章][SECTION#9.2]中进行详细描述.

## 13.1. 响应标头

> [原文](https://datatracker.ietf.org/doc/html/rfc4918#section-13.1)

HTTP 定义了 `Location` 标头, 用于指示 `Request-URI` 中寻址资源的首选 URL
(e.g., 在 PUT 请求的成功响应或重定向响应中).
然而, 当响应正文中存在 URL 时 (例如在多状态响应中), 使用该标头会产生歧义.
因此，多状态响应的 `Location` 标头是故意未定义的.

## 13.2. 处理重定向的子资源

> [原文](https://datatracker.ietf.org/doc/html/rfc4918#section-13.2)

HTTP 1.1 中定义的重定向响应 (`300-303`, `305` 和 `307`) 通常使用 `Location` 标头来指示从
`Request-URI` 重定向的单个资源的新 URI. 多状态响包含许多资源地址,
但 [RFC2518] 中的原始定义没有任何地方让服务器为重定向资源提供新的 URI.
该规范为此信息明确定义了一个 `location` 元素 (见[第 14.9 章][SECTION#14.9]).
服务器**必须[MUST]**在多状态的重定向响应中使用这个新元素.

客户端在多状态中遇到重定向资源时**不能[MUST_NOT]**依赖 `location` 元素是否存在于新的 URI 中.
如果该元素不存在, 客户端**可能[MAY]**需要向单独的重定向资源重新发出请求,
因为对该请求的响应可以使用包含新 URI 的 Location 标头进行重定向.

## 13.3. 内部状态码

> [原文](https://datatracker.ietf.org/doc/html/rfc4918#section-13.3)

第 [9.2.1][SECTION#9.2.1], [9.1.2][SECTION#9.1.2],
[9.6.1][SECTION#9.6.1], [9.8.3][SECTION#9.8.3] 和 [9.9.2][SECTION#9.9.2]
章中定义了多状态响应中使用的各种状态码. 本规范没有定义在这些响应中可能出现的其他状态码的含义.

<!-- refs -->

[SECTION#14.9]: 14-xml_element_definitions.md#149-location-xml-元素
[SECTION#9.1]: 9-http_methods_for_distributed_authoring.md#91-propfind-方法
[SECTION#9.1.2]: 9-http_methods_for_distributed_authoring.md#912-用于-propstat-元素的状态码
[SECTION#9.2]: 9-http_methods_for_distributed_authoring.md#92-proppatch-方法
[SECTION#9.2.1]: 9-http_methods_for_distributed_authoring.md#921-propstat-元素中使用的状态代码
[SECTION#9.6.1]: 9-http_methods_for_distributed_authoring.md#961-集合中的-delete
[SECTION#9.6.2]: 9-http_methods_for_distributed_authoring.md#962-示例---delete
[SECTION#9.8.3]: 9-http_methods_for_distributed_authoring.md#983-集合中的-copy
[SECTION#9.9.2]: s9-http_methods_for_distributed_authoring.md#992-集合中的-move
