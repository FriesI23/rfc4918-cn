# 附录 C. "opaquelocktoken" 方案和 URI

"opaquelocktoken" URI 方案在 [RFC2518] 中定义 (由 IANA 注册),
旨在使用 UUID 创建正确语法且易于生成的 URI 用与锁令牌, 并使其在所有资源和时间内是唯一的.

opaquelocktoken URI 由 "opaquelocktoken" 方案与 UUID 以及可选的扩展串联.
服务器可以为每个新的锁令牌创建新的 UUID. 如果服务器希望重用 UUID,
其**必须[MUST]**添加一个扩展,
并且生成扩展的算法**必须[MUST]**保证相同的扩展永远不会与关联的 UUID 一起重复使用.

```bnf
OpaqueLockToken-URI = "opaquelocktoken:" UUID [Extension]
    ; UUID 在 [RFC4122#3] 中定义. 需要注意的是,
    ; 在此产生的元素之间不允许使用线性空白 LWS.

Extension = path
    ; path 在 [RFC3986#3.3] 中定义
```
