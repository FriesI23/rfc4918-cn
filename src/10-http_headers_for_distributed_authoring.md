# 10. 用于分布式创作的 HTTP 标头 (HTTP Headers for Distributed Authoring

所有的 DAV 标头都遵循与 HTTP 标头同样的基本格式规则. 其中包括一些规则, 像是行延续
(line continuation) 与 怎样使用逗号将多个具有相同标头的实例融合(或分离).

WebDAV 在 HTTP 定义集中添加了两个新的条件性标头: If 和 Overwrite 标头.

## 10.1. DAV 标头 (DAV Header)

```lisp
DAV              = "DAV" ":" #( compliance-class )
compliance-class = ( "1" | "2" | "3" | extend )
extend           = Coded-URL | token
                    ; token 在 RFC 2616 第 2.2 章定义
Coded-URL        = "<" absolute-URI ">"
                    ; Coded-URL 中允许非线性空白 (LAWS)
                    ; absolute-URI 在 RFC 3986, 第 4.3 章定义
```

响应中出现的这个通用标头指出: 资源支持按照规范指定的 DAV 模式和协议. 所有符合 DAV
规范的资源**必须** (MUST) 在所有 OPTIONS 响应中返回带有 `compliance-class` 为 "1" 的
DAV 标头. 在服务器中只有一部分命名空间支持 WebDAV 的情况下, 对非 WebDAV 资源 (包括"/")
的 OPTIONS 请求**不应该** (SHOULD NOT) 宣称支持 WebDAV.

DAV 的值是资源支持的所有 `compliance-class` 标识符并使用逗号分隔的列表, 类标识符可以是
`Coded-URLs` 或 `token` (根据[RFC2616]定义). 标识符可以以任何顺序出现.
`token` 是通过 IETF RFC 过程标准化的标识符, 但其他标识符出于鼓励唯一性的目的**应该**
(SHOULD) 为 `Coded-URL`.

当资源显示其遵守对 `class 2` 或 `class 3` 合规, 则其必须显示对 `class 1` 合规.
一般来说，对一个合规类的支持并不意味着对其他任何合规类也支持, 并且, 特别的, 支持对 `class 3`
合规并不需要支持对 `class 2` 合规. 有关此规范中定义中对合规类的更多详细信息,
请参考[第 18 章]().

需要注意的是，许多 WebDAV 服务器在 "OPTIONS \*" 的响应中不会宣称支持 WebDAV.

作为一个请求标头, 此标头允许客户端在服务器需要该信息时宣称其具对命名功能的合规性.
除非标准化进城规范 (standards track specification) 需要, 否则客户端**不应**
(SHOULD NOT)发送此标头. 任何使用此标头作为请求标头的扩展都需要仔细考虑缓存该请求带来的影响.

## 10.2. Depth 标头 (Depth Header)

```lisp
Depth = "Depth" ":" ("0" | "1" | "infinity")
```
