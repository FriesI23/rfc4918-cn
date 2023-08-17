# 2. 符号约定 (Notational Conventions)

由于本文档描述了对 HTTP/1.1 协议的一系列扩展, 因此这里使用增强 BNF (augmented BNF)
描述协议元素与 [RFC2616#2.1] 中所述的完全相同，包括有关隐含空格 (liner spacing) 的规则.
增强 BNF 使用了 [RFC2616#2.2] 中提供的基本生成规则, 因此这些规则也适用于本文档.
请**注意**, 该语法不是其他 RFC 文档中使用的标准 BNF 语法 (standard BNF syntax).

本文档中的关键字

- "MUST", "REQUIRED", "SHALL": 表示必须遵守.
- "MUST NOT", "SHALL NOT": 表示必须被禁止.
- "SHOULD", "RECOMMENDED": 表示特定情况可以忽略该条件, 不过必须正确理解上下文含义.
- "SHOULD NOT": 表示特定情况可以接受该条件
- "MAY", "OPTIONAL": 表示一个可选项

皆按照 [RFC2119] 中描述解释。

请注意, 在自然语言中有时为了简洁, 类似 XML 里 `DAV:` 命名空间中的 `creationdate`属性,
会简称为 `DAV:creationdate`。
