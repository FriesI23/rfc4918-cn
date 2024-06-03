# 方法速查

## WebDAV 方法表

| 方法名                   | 作用                                                  | 是否幂等 | 是否安全 | 备注                       |
| ------------------------ | ----------------------------------------------------- | -------- | -------- | -------------------------- |
| [PROPFIND][M:PROPFIND]   | 用于检索由请求 URI (Request-URI) 标识资源上定义的属性 | Y        | Y        |                            |
| [PROPPATCH][M:PROPPATCH] | 用于设置和/或移除由请求 URI 标识资源上定义的属性      | Y        | N        | 不要缓存此方法的响应       |
| [MKCOL][M:MKCOL]         | 在由 `Request-URI` 指定的位置创建一个新的集合资源     | Y        | N        | 不要缓存此方法的响应       |
| [GET/HEAD][M:GET]        |                                                       |          |          | 与 HTTP 中的 GET 用法相同  |
| [POST][M:POST]           |                                                       |          |          | 与 HTTP 中的 POST 用法相同 |
| [DELETE][M:DELETE]       | 删除由 Request-URI 标识的资源                         |          |          |                            |
| [PUT][M:PUT]             |                                                       |          |          |                            |
| [COPY][M:COPY]           | 创建源资源的副本                                      | Y        | N        | 不要缓存此方法的响应       |
| [MOVE][M:MOVE]           | 将资源移动到一个新的位置                              |          |          |                            |
| *[LOCK][M:LOCK]          | 用于获取任何访问类型的锁                              | N        | N        | 不要缓存此方法的响应       |
| **[UNLOCK][M:UNLOCK]      | 移除由 `Lock-Token` 请求标头中的锁定牌标识的锁        | Y        | N        | 不要缓存此方法的响应       |

> `*`: 方法是可选的
> `**`: 当有 LOCK 方法是, 该方法是必选的, 否则是可选的

[M:PROPFIND]: 9-http_methods_for_distributed_authoring.md#91-propfind-方法
[M:PROPPATCH]: 9-http_methods_for_distributed_authoring.md#92-proppatch-方法
[M:MKCOL]: 9-http_methods_for_distributed_authoring.md#93-mkcol-方法
[M:GET]: 9-http_methods_for_distributed_authoring.md#94-集合中的-get-和-head
[M:POST]: 9-http_methods_for_distributed_authoring.md#95-集合中的-post
[M:DELETE]: 9-http_methods_for_distributed_authoring.md#96-delete-要求
[M:PUT]: 9-http_methods_for_distributed_authoring.md#97-put-要求
[M:COPY]: 9-http_methods_for_distributed_authoring.md#98-copy-方法
[M:MOVE]: 9-http_methods_for_distributed_authoring.md#99-move-方法
[M:LOCK]: 9-http_methods_for_distributed_authoring.md#910-lock-方法
[M:UNLOCK]: 9-http_methods_for_distributed_authoring.md#911-unlock-方法
