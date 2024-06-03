# 用于 Web 分布式作者和版本控制的 HTTP 扩展（WebDAV）

## 关于该 memo 的状态

该文档为 Internet 社区定义了一种 Internet 标准跟踪协议, 并提出讨论和改进建议.
请参考 "Internet 官方协议标准" (STD 1) [RFC7101] 的最新版本以了解此协议的标准化和状态.
本 memo 不限制分发.

## 版权声明

Copyright (C) The IETF Trust (2007).

## 摘要

Web 分布式作者和版本控制 (WebDAV) 包括一组与 HTTP/1.1 相关的方法 (method),
头 (header) 与内容类型 (content-type)，用于管理:

- 资源属性 (resource)
- 创建与管理资源集合 (resource collections)
- URL 命名空间操作以及资源锁定 (resource locking) 以避免冲突.

[RFC2518] 于 1999 年 2 月发布，本规范废弃了 [RFC2518],
并从实际应用中获得的互操作性经验对其进行小幅修订.

## 翻译版本修订状态

- v2
  - 校对并修正大量翻译问题 (机翻 or 原文理解错误).
  - 增加对该文档中一些重要外部引用文档的部分翻译.
  - 修复在线文档的一些错误.
- v1
  - 完成翻译.

## IETF 原文完整版权声明

```text
   Copyright (C) The IETF Trust (2007).

   This document is subject to the rights, licenses and restrictions
   contained in BCP 78, and except as set forth therein, the authors
   retain all their rights.

   This document and the information contained herein are provided on an
   "AS IS" basis and THE CONTRIBUTOR, THE ORGANIZATION HE/SHE REPRESENTS
   OR IS SPONSORED BY (IF ANY), THE INTERNET SOCIETY, THE IETF TRUST AND
   THE INTERNET ENGINEERING TASK FORCE DISCLAIM ALL WARRANTIES, EXPRESS
   OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTY THAT THE USE OF
   THE INFORMATION HEREIN WILL NOT INFRINGE ANY RIGHTS OR ANY IMPLIED
   WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.

Intellectual Property

   The IETF takes no position regarding the validity or scope of any
   Intellectual Property Rights or other rights that might be claimed to
   pertain to the implementation or use of the technology described in
   this document or the extent to which any license under such rights
   might or might not be available; nor does it represent that it has
   made any independent effort to identify any such rights.  Information
   on the procedures with respect to rights in RFC documents can be
   found in BCP 78 and BCP 79.

   Copies of IPR disclosures made to the IETF Secretariat and any
   assurances of licenses to be made available, or the result of an
   attempt made to obtain a general license or permission for the use of
   such proprietary rights by implementers or users of this
   specification can be obtained from the IETF on-line IPR repository at
   http://www.ietf.org/ipr.

   The IETF invites any interested party to bring to its attention any
   copyrights, patents or patent applications, or other proprietary
   rights that may cover technology that may be required to implement
   this standard.  Please address the information to the IETF at
   ietf-ipr@ietf.org.

Acknowledgement

   Funding for the RFC Editor function is currently provided by the
   Internet Society.
```

## 本文版权声明

```text
 rfc4918-cn (c) by Fries_I23

 rfc4918-cn is licensed under a
 Creative Commons Attribution-ShareAlike 4.0 International License.

 You should have received a copy of the license along with this
 work. If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
```
