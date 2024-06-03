# 附录 E. 客户端希望进行认证的相关指导

许多 WebDAV 客户端已经实现了帐户设置 (类似于电子邮件客户端存储 IMAP 帐户设置的方式).
因此, WebDAV 客户端将能够通过向服务器发出的前几个请求进行认证,
前提是其有办法从服务器获取包含域名, 随机数与其他质询信息的身份验证质询.
需要注意的是, 某些请求的结果可能会根据客户端是否经过认证而有所不同
-- 如果客户端是认证的, 则 PROPFIND 可能会返回更多可见资源, 但如果客户端是匿名的，请求也不会失败.

客户端可能有多种方式触发服务器来提供认证质询. 本附录中描述了几种似乎特别有可能工作的方式.

第一种方法是执行一个应需认证的请求. 但是即使没有认证, 服务器仍可能会处理任何请求,
因此为了绝对安全, 客户端可以添加条件标头, 确保即使请求通过权限检查, 实际上也不会由服务器处理.
遵循此方法的一个示例是使用带有 `If-Match` 标头和虚构 `ETag` 值的 PUT 请求.
如果服务器在测试条件之前不测试认证 (参考[第 8.5 章][SECTION#8.5]) 或服务器不需要测试认证,
则此方法可能无法导致认证质询.

示例 - 使用写请求强制进行认证质询

```http
>>Request

PUT /forceauth.txt HTTP/1.1
Host: www.example.com
If-Match: "xxx"
Content-Type: text/plain
Content-Length: 0
```

第二种方法是使用 `Authorization` 标头 ([RFC2617]中定义), 这可能会被服务器拒绝,
然后会提示一个适当的身认证质询. 例如, 客户端可以从包含 `Authorization` 标头的 PROPFIND 请求开始,
该标头包含虚构的 `Basic userid:password` 字符串或实际可信的凭据.
这种方法依赖于服务器对具有未识别用户名, 无效密码或甚至不处理 Basic 认证的 Authorization 标头的要求,
如果服务器接收到这些内容，将会响应 "401 Unauthorized" 并附带一个质询. 由于[RFC2617]的要求, 以下应该可以工作:

"如果源服务器不希望接受随请求发送的凭证, 其**应该[SHOULD]**返回 401 (Unauthorized) 响应.
该响应**必须[MUST]**包含 `WWW-Authenticate` 标头字段, 其中包含至少一个适用于所请求资源的
(可能是新的) 质询."

在某些情况下, 实施这个建议会有微小的问题, 因为一些服务器对于某些资源甚至都没有质询信息.
因此, 当没有办法对资源进行认证, 或是资源完全可以通过所有可接受的方法公开访问时,
服务器**可能[MAY]**忽略 `Authorization` 标头, 并且客户端大概率会在稍后尝试再次发起请求.

示例 - 使用认证标头强制进行授权质询

```http
>>Request

PROPFIND /docs/ HTTP/1.1
Host: www.example.com
Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
Content-type: application/xml; charset="utf-8"
Content-Length: xxxx

[body omitted]
```

<!-- refs -->

[SECTION#8.5]: 8-general_request_and_response_handling.md#85-用于-webdav-的-http-标头
