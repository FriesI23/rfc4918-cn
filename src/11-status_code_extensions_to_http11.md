# 11. HTTP/1.1 状态代码扩展

> [原文](https://datatracker.ietf.org/doc/html/rfc4918#section-11)

以下状态代码已添加到 HTTP/1.1 [RFC2616] 中.

## 11.1. 207 多状态 (207 Multi-Status)

> [原文](https://datatracker.ietf.org/doc/html/rfc4918#section-11.1)

207 (Multi-Status) 状态码为多个独立操作提供状态信息 (详见[第 13 章][SECTION#13]以获取更多信息).

## 11.2. 422 无法处理的实体 (422 Unprocessable Entity)

> [原文](https://datatracker.ietf.org/doc/html/rfc4918#section-11.2)

422 (Unprocessable Entity) 状态码表示服务器理解请求实体的内容类型
(因此不适用 415 (Unsupported Media Type) 状态码), 且请求实体的语法正确
(因此不适用 400 (Bad Request) 状态码), 但服务器无法处理其中包含的指令.
例如, 如果 XML 请求正文内包含形式正确 (i.e., 语法正确), 但在语义上错误, 则可能会发生此错误.

## 11.3. 432 已锁定 (423 Locked)

> [原文](https://datatracker.ietf.org/doc/html/rfc4918#section-11.3)

423 (Locked) 状态码表示方法的源资源或目标资源被锁定.
此响应**应该[SHOULD]**包含适当的前置/后置条件码,
比如 `"lock-token-submitted"` 或 `"no-conflicting-lock"`.

## 11.4. 424 依赖失败 (424 Failed Dependency)

> [原文](https://datatracker.ietf.org/doc/html/rfc4918#section-11.4)

424 (Failed Dependency) 状态码表示由于请求的操作依赖于另一个操作, 且该操作失败,
因此无法对资源执行此方法. 例如, 如果 PROPPATCH 方法中的某个命令失败, 那么,
至少其余命令也将因依赖失败而无法执行, 并返回 424 (Failed Dependency) 状态码.

## 11.5. 507 存储空间不足 (507 Insufficient Storage)

> [原文](https://datatracker.ietf.org/doc/html/rfc4918#section-11.5)

507 (Insufficient Storage) 状态码表示由于服务器无法存储完成请求所需的数据表示,
因此无法对资源执行该方法. 这种情况被视为临时性的. 如果导致此状态码的请求是由用户操作引起的,
则直到单独用户再次操作前, **不能[SHOULD_NOT]**重复该请求.

<!-- refs -->

[SECTION#13]: 13-multi_status_response.md
