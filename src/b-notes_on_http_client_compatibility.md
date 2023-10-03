# 附录 B. HTTP 客户端兼容性注意事项

WebDAV 设计时考虑了与 HTTP 1.1 的向后兼容性, 并已被证明确实与 HTTP 1.1 兼容.
PUT 和 DELETE 方法在 HTTP 中定义, 因此可以由 HTTP 客户端和 WebDAV 感知的客户端使用,
但对于 PUT 和 DELETE 响应, 在本规范中以只有 WebDAV 客户端完全准备好的方式进行扩展.
关于这些响应是否会导致与仅支持 HTTP 的客户端的互操作性问题, 有人曾提出了一些理论上的担忧,
本章将解决上面这些担忧.

由于任何 HTTP 客户端都应将未识别的 400 和 500 级别状态码视为错误,
因此下面新的状态码不应该引发任何问题: 422, 423 和 507 (424 也是一个新的状态码，
但只出现在 Multistatus 响应正文中). 因此, 例如,
如果一个 HTTP 客户端尝试使用 PUT 或 DELETE 访问锁定的资源,
423 Locked 响应应会导致向用户显示通用错误.

207 Multistatus 响应很有意思, 因为发送 DELETE 请求到集合的 HTTP 客户端可能会将 207
响应解释为成功, 即使其意识不到资源是一个集合, 且不能理解 DELETE 操作可能是完全或部分失败.
这种解释并不完全合理, 因为 200 级别响应表示服务器 "接收, 理解和接受" 了请求,
而不表示请求完全成功.

一种选择是, 服务器可以将对集合的 DELETE 操作视为原子操作, 并在成功时使用 204 No Content,
或者在出现错误时使用适当的错误响应 (400 或 500 级别). 这种方法的确会最大程度提高向后兼容性.
然而, 由于互操作性测试和工作组讨论中并没有发现 HTTP 客户端会向 WebDAV 集合发出 DELETE 请求,
因此这个问题更多是理论上而不会实际发生. 因此, 即使服务器将任何集合 DELETE 请求视为 WebDAV
请求并发送 207 Multi-Status 响应, 服务器也可能与 HTTP 客户端进行完全成功地互操作.

总体来说, 对于服务器实现, 鼓励使用本文档中定义的详细响应和其他机制,
而不是出于理论上的互操作性问题而进行更改.