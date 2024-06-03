# 1. 简介

本文档描述了对 HTTP/1.1 协议的扩展, 允许客户端执行远程 Web 内容创作相关操作 (remote Web
content authoring operations). 该扩展提供一组相关方法 (methods), 标头 (heaeders),
请求实体正文格式 (request entity body formats) 和响应实体正文格式
(response entity body formats), 并提供下述操作:

- **属性 (Property)**: 创建, 删除, 查询有关 Web 页面信息, 例如作者或者创建日期等.
- **集合 (Collection)**：创建文档集合 (sets of documents),
  并检索层级成员列表 (hierarchical membership listing) (类似于文件系统中的目录树).
- **锁定 (Locking)**: 能够防止多人同时编辑一个文档, 避免"丢失更新问题",
  即在没有合并其他作者的更改的情况下, 连续两个作者先后进行修改, 这会导致第一个作者的修改丢失.
- **命名空间操作 (Namespace Operations)**: 能够指示服务器复制和移动 Web 资源,
  从而改变从 URL 到资源的映射关系.

[RFC2291] 对这些操作的要求和为什么这么定义进行了描述.

本文档未指定 [RFC2291] 中建议的版本控制操作. 该工作 [RFC3253] 中进行.

以下各章详细介绍了各种 WebDAV 的抽象:

- 资源属性 (resource properties) ([第 4 章][SECTION#4])
- 资源集合 (collections of resources) ([第 5 章][SECTION#5])
- 锁定 (locks) ([第 6 章][SECTION#6])
- 写锁定 (write locks) ([第 7 章][SECTION#7])

这些抽象使用以下方式操作

- WebDAV 中特定的 HTTP 方法 (WebDAV-specific HTTP methods) ([第 9 章][SECTION#9])
- 与 WebDAV 方法一起使用的额外 HTTP 标头 (extra HTTP headers used with
  WebDAV methods) ([第 10 章][SECTION#10])

关于在 WebDAV 中处理 HTTP 请求和响应的一般考虑事项,
请参考[第八章](./8_General%20Request%20and%20Response%20Handling.md).

虽然 HTTP/1.1 提供的状态码足以描述 WebDAV 方法中遇到的大多数错误条件 (error conditions),
但某些错误并不完全适用.
本规范定义了为 WebDAV 方法开发的额外状态码 ([第 11 章][SECTION#11]),
并描述了在 WebDAV 中使用的现有 HTTP 状态码 ([第 12 章][SECTION#12]).
由于一些 WebDAV 方法可能涉及多个资源, 因此引入了多状态响应 (Multi-Status response)
([第 13 章][SECTION#13]) 来返回多个资源的状态信息.
最后, 该版本 WebDAV 在错误响应正文 (response body) 的 XML 元素中引入了前置和后置条件
([第 16 章][SECTION#16]).

WebDAV 使用 XML ([REC-XML]) 作为属性名和部分值，
并且还使用 XML 来封装 (marshalling) 复杂的请求和响应. 本规范包含封装中使用的定义:

- XML 元素（[第 14 章][SECTION#14]）
- 所有 属性的 DTD 和文本定义 ([第 15 章][SECTION#15])

WebDAV 包含一些特殊规则，以向后兼容的方式扩展 WebDAV XML 封装 ([第 17 章][SECTION#17]).

规范的其他部分包括:

- 符合本规范资源含义的说明 ([第 18 章][SECTION#18])
- 国际化支持 ([第 19 章][SECTION#19])
- 安全性讨论([第 20 章][SECTION#20])

<!-- refs -->

[SECTION#4]: 4-data_model_for_resource_properties.md
[SECTION#5]: 5-collection_of_web_resources.md
[SECTION#6]: 6-locking.md
[SECTION#7]: 7-write_lock.md
[SECTION#9]: 9-http_methods_for_distributed_authoring.md
[SECTION#10]: 10-http_headers_for_distributed_authoring.md
[SECTION#11]: 11-status_code_extensions_to_http11.md
[SECTION#12]: 12-use-of-hhtp-status-code.md
[SECTION#13]: 13-multi_status_response.md
[SECTION#14]: 14-xml_element_definitions.md
[SECTION#15]: 15-dav_properties.md
[SECTION#16]: 16-precondition_postcondition_xml_elements.md
[SECTION#17]: 17-xml_extensibility_in_dav.md
[SECTION#18]: 18-dav_compliance_classes.md
[SECTION#19]: 19-internationalization_considerations.md
[SECTION#20]: 20-security_consideration.md
