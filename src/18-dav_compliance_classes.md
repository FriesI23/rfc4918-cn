# 18. DAV 合规类

DAV 兼容 (DAV-compliant) 的资源可以宣布多种类合规性,
客户端可以通过在资源上执行 OPTIONS 并检查返回的 `DAV` 标头来发现一个资源的合规类.
资源（而不是服务器）被认为是合规的, 这是因为理论上服务器中的一些资源可以支持不同的功能集.
例如, 服务器可以具有一个子存储库 (sub-repository), 该子库支持如版本控制这类高级功能,
即使不是所有子存储库都支持这个功能。

由于本文档描述了对 HTTP/1.1 协议的扩展,
至少所有符合 DAV 的资源, 客户端和代理都必须符合 [RFC2616]。

符合 `class 2` 或 `class 3` 标准的资源也必须符合 `class 1` 标准.

## 18.1. Class 1（类别 1）

一个 `class 1` 合规资源必须满足本文档的所有 "**必须[MUST]**" 要求.
Class 1 合规资源**必须[MUST]**在对 OPTIONS 方法的所有响应的 DAV 标头中至少返回值 "1".

## 18.2. Class 2（类别 2）

一个 `class 2` 合规资源**必须[MUST]**满足所有 `class 1` 的要求, 并支持:

- LOCK 方法
- `DAV:supportedlock` 属性
- `DAV:lockdiscovery` 属性
- `Time-Out` 响应标头
- `Lock-Token` 请求标头

一个 `class 2` 合规的源还**应该[SHOULD]**支持:

- `Timeout` 请求标头
- `<owner>` XML 元素

`class 2` 合规资源**必须[MUST]**在对 OPTIONS 方法的所有响应的 DAV 标头中至少返回值
`1` 和 `2`.

## 18.3. Class 3（类别 3）

该资源可以明确宣称其支持此文档中对 [RFC2518] 所作的修改.
`class 1` **必须[MUST]**支持. `class 2` **可选[MAY]**支持.
如果在宣称支持 `class 3` 的同时还支持 `class 1` 和 `class 2`,
这意味着服务器支持本规范中的所有要求.
如果在宣称支持 `class 3` 和 `class 1` 的同时不支持 `class 2`，
则意味着服务器支持本规范中的所有要求, 但可能不涉及锁相关支持.

**示例**: `DAV: 1, 3`
