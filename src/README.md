# 用于 Web 分布式作者和版本控制的 HTTP 扩展（WebDAV）

## 关于该 memo 的状态

该文档为 Internet 社区定义了一种 Internet 标准跟踪协议, 并提出讨论和改进建议. 请参考
"Internet 官方协议标准" (STD 1) [RFC7101] 的最新版本以了解此协议的标准化和状态.
本 memo 不限制分发.

## 版权声明

Copyright (C) The IETF Trust (2007).

## 摘要

Web 分布式作者和版本控制 (WebDAV) 包括一组与 HTTP/1.1 相关的方法 (method), 头 (header)
与内容类型 (content-type)，用于管理:

- 资源属性 (resource)
- 创建与管理资源集合 (resource collections)
- URL 命名空间操作以及资源锁定 (resource locking) 以避免冲突.

[RFC2518] 于 1999 年 2 月发布，本规范废弃了 [RFC2518],
并从实际应用中获得的互操作性经验对其进行小幅修订.
