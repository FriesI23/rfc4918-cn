# 21. IANA 考量因素

## 21.1. 新 URI 方案

本规范定义了两种 URI 方案:

1. "opaquelocktoken" 方案，定义在[附录 C][APPENDIX#C]中.

2. "DAV" URI 方案, 以前是在 [RFC2518] 中用于区分 WebDAV 属性和 XML 元素名,
   并在本规范以及其他扩展 WebDAV 的规范中已该目的继续使用.
   在 "DAV:" 命名空间中如何创建标识符由 IETF 控制.

需要注意的是, 现在已经不鼓励为 XML 命名空间定义新的 URI 方案.
"DAV:" 是在标准最佳实践出现之前定义的.

## 21.2. XML 命名空间

XML 命名空间用于区分 WebDAV 属性名和 XML 元素.
任何 WebDAV 用户或应用程序都可以定义新的命名空间, 以创建自定义属性或扩展 WebDAV XML 语法.
IANA 不会管理这些命名空间, 属性名或元素名.

## 21.3. 消息标头字段

以下消息头字段应添加到持久注册表中 (参见 [RFC3864])

### 21.3.1. DAV

- **标头字段名**: DAV
- **适用协议**: HTTP
- **状态**: 标准 (standard)
- **作者/可变更者**: IETF
- **规范文档**: 本规范 ([第 10.1 章][SECTION#10.1])

### 21.3.2. Depth

- **标头字段名**: Depth
- **适用协议**: HTTP
- **状态**: 标准 (standard)
- **作者/可变更者**: IETF
- **规范文档**: 本规范 ([第 10.2 章][SECTION#10.2])

### 21.3.3. Destination

- **标头字段名**: Destination
- **适用协议**: HTTP
- **状态**: 标准 (standard)
- **作者/可变更者**: IETF
- **规范文档**: 本规范 ([第 10.3 章][SECTION#10.3])

### 21.3.4. If

- **标头字段名**: If
- **适用协议**: HTTP
- **状态**: 标准
- **作者/可变更者**: IETF
- **规范文档**: 本规范 ([第 10.4 章][SECTION#10.4])

### 21.3.5. Lock-Token

- **标头字段名**: Lock-Token
- **适用协议**: HTTP
- **状态**: 标准 (standard)
- **作者/可变更者**: IETF
- **规范文档**: 本规范 ([第 10.5 章][SECTION#10.5])

### 21.3.6. Overwrite

- **标头字段名**: Overwrite
- **适用协议**: HTTP
- **状态**: 标准 (standard)
- **作者/可变更者**: IETF
- **规范文档**: 本规范 ([第 10.6 章][SECTION#10.6])

### 21.3.7. Timeout

- **标头字段名**: Timeout
- **适用协议**: HTTP
- **状态**: 标准 (standard)
- **作者/可变更者**: IETF
- **规范文档**: 本规范 ([第 10.7 章][SECTION#10.7])

## 21.4. HTTP 状态码

本规范定义了以下 HTTP 状态代码：

- 207 Multi-Status ([第 11.1 章][SECTION#11.1])
- 422 Unprocessable Entity ([第 11.2 章][SECTION#11.2])
- 423 Locked ([第 11.3 章][SECTION#11.3])
- 424 Failed Dependency ([第 11.4 章][SECTION#11.4])
- 507 Insufficient Storage ([第 11.5 章][SECTION#11.5])

可以在[这里][HTTP_SATUTS_CODE]找到状态码更新的注册码.

注意: HTTP 状态码 102 (Processing) 已在本规范中删除;
[RFC2518] 将继续引用 IANA 中的该注册码.

<!-- refs -->

[SECTION#10.1]: 10-http_headers_for_distributed_authoring.md#101-dav-标头
[SECTION#10.2]: 10-http_headers_for_distributed_authoring.md#102-depth-标头
[SECTION#10.3]: 10-http_headers_for_distributed_authoring.md#103-destination-标头
[SECTION#10.4]: 10-http_headers_for_distributed_authoring.md#104-if-标头
[SECTION#10.5]: 10-http_headers_for_distributed_authoring.md#105-lock-token-标头
[SECTION#10.6]: 10-http_headers_for_distributed_authoring.md#106-overwrite-标头
[SECTION#10.7]: 10-http_headers_for_distributed_authoring.md#107-timeout-请求标头
[SECTION#11.1]: 11-status_code_extensions_to_http11.md#111-207-多状态-207-multi-status
[SECTION#11.2]: 11-status_code_extensions_to_http11.md#112-422-无法处理的实体-422-unprocessable-entity
[SECTION#11.3]: 11-status_code_extensions_to_http11.md#113-432-已锁定-423-locked
[SECTION#11.4]: 11-status_code_extensions_to_http11.md#114-424-依赖失败-424-failed-dependency
[SECTION#11.5]: 11-status_code_extensions_to_http11.md#115-507-存储空间不足-507-insufficient-storage
[APPENDIX#C]: c-the_opaquelocktoken_scheme_and_url.md
[HTTP_SATUTS_CODE]: http://www.iana.org/assignments/http-status-codes
