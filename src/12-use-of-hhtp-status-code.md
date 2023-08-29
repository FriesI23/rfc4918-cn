# 12. HTTP 状态码的使用 (Use of HTTP Status Codes)

这些 HTTP 状态码并未重新定义, 但它们的使用某种程度上来说是一种通过 WebDAV
方法和要求进行的扩展. 一般来说, 很多 HTTP 状态码可以用作对任何请求的响应，
而不是仅限于本文档中描述的情况. 还要注意的是, 已知 WebDAV 服务器使用 300-level
的重定向响应 (而早期的互操作性测试发现很多客户端对这些响应没有准备).
当服务器根据请求创建了新资源时，**不能** (MUST NOT) 使用 300-level 的响应.

## 12.1. 412 前置条件失败 (412 Precondition Failed)

任何请求都可以包含在 HTTP 中定义的条件标头 (如 "If-Match", "If-Modified-Since" 等)
或是在本规范中定义的 "If" 或 "Overwrite" 条件标头. 如果服务器评估了一个条件标头,
且不满足该条件, 则**必须** (MUST) 返回此错误代码. 另一方面,
如果客户端在请求中未包含条件标头, 服务器则**不能** (MUST NOT) 使用此状态码.

## 12.2. 414 Request-URL 过长 (414 Request-URI Too Long)

此状态代码在 HTTP 1.1 中仅用于 Request-URI，不适用于其他位置的 URI.
