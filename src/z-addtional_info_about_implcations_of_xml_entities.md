# 与 XML 实体相关的影响补充

在 [20. 安全性考量 / 与 XML 实体相关的影响][SECIONT#20.6] 中讨论了 XML 相关的安全问题.
这里补充一些有关 "外部实体", "内部实体" 定义相关文档的翻译.

## 内部实体(声明)

> [原文](https://www.w3.org/TR/xml/#sec-internal-ent)

**定义**: 如果实体定义有 [`EntityValue`](z-typedefs.md#entityvalue), 则该实体称为内部实体.
没有单独的物理存储对象, 实体的内容在声明中给出.
请注意, 可能需要对文字实体值中的实体引用和字符引用进行处理,
以产生正确的替换文本: 请参阅[第4.5节 "构造实体替换文本"][REF-XML#4.5].

内部实体是一个解析实体.

内部实体声明的示例:

```xml
<!ENTITY Pub-Status "This is a pre-release of the specification.">
```

> 译者注, 举个例子:
>
> ```xml
> <!ENTITY imageData "PGh0bWw+CiAgPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJ1dGYtOCI+CgogICAgPGltZyBzaXplPSJ3aWR0aDoxMDAlIiBzdHJva2U9Im5vbmUiIGJvcmRlcj0iMCIgLz4KCiAgICA8L2hlYWQ+CiAgPC9odG1sPg==">
> <image>
>   <data>$imageData</data>
> </image>
> ```

## 外部实体(声明)

> [原文](https://www.w3.org/TR/xml/#sec-external-ent)

**定义**: 如果实体不是内部的, 则是外部实体. 声明如下:

```bnf
ExternalID     ::= 'SYSTEM' S SystemLiteral
                 | 'PUBLIC' S PubidLiteral S SystemLiteral
NDataDecl      ::= S 'NDATA' S Name

; ---------------------------------------------------------
; Below are some common syntactic constructs

S              ::= (#x20 | #x9 | #xD | #xA)+
SystemLiteral  ::= ('"' [^"]* '"') | ("'" [^']* "'")

PubidLiteral   ::= '"' PubidChar* '"' | "'" (PubidChar - "'")* "'"
PubidChar      ::= #x20 | #xD | #xA | [a-zA-Z0-9] | [-'()+,./:=?;!*#@$_%]

Name           ::= NameStartChar (NameChar)*
NameChar       ::= NameStartChar | "-" | "." | [0-9] | #xB7
                 | [#x0300-#x036F] | [#x203F-#x2040]

NameStartChar  ::= ":" | [A-Z] | "_" | [a-z] | [#xC0-#xD6] | [#xD8-#xF6]
                 | [#xF8-#x2FF] | [#x370-#x37D] | [#x37F-#x1FFF]
                 | [#x200C-#x200D] | [#x2070-#x218F] | [#x2C00-#x2FEF]
                 | [#x3001-#xD7FF] | [#xF900-#xFDCF] | [#xFDF0-#xFFFD]
                 | [#x10000-#xEFFFF]
```

如果存在 `NDataDecl`, 则这是一个一般的未解析实体; 否则是一个已解析实体.

有效性约束: 符号声明.

名称**必须[MUST]**与符号声明的名称匹配.

**定义**: `SystemLiteral` 被称为实体的系统标识符.
其应当被转换为一个 URI 引用 (如 [RFC3986] 中定义的那样),
作为将其解引用以获取 XML 处理器构造实体替换文本所需输入的一部分过程.

一部分以 `#` 字符开头的片段标识符作为系统标识符是错误的. 除非在本规范范围之外提供了其他信息
(e.g., 由特定 DTD 定义的特殊 XML 元素类型, 或由特定应用程序规范定义的处理指令),
否则相对 URI 是相对于声明中包含的资源位置. 此位置被定义为在解析为声明时开始的包含 `'<'` 的外部实体.
因此, URI 可能相对于文档实体, 亦或是相对于包含外部 DTD 子集的实体, 又或者相对于某些其他外部参数实体.
尝试检索由 URI 标识的资源可能会在解析器层级 (e,g., 在实体解析器中) 或更低层级
(e.g., 通过 HTTP 的 `Location:` 标头) 进行重定向.
如果在资源内部范围之外没有额外的信息, 那么资源的基本 URI 总是为实际返回资源的 URI.
换句话说, 该 URI 是在发生所有重定向后检索到的资源 URI.

系统标识符 (以及其他用作 URI 引用的 XML 字符串) 可能包含根据 [RFC3986] 的规定的,
在使用 URI 检索引用资源之前**必须[MUST]**进行转义的字符.
要转义的字符包括从控制字符 `#x0` 到 `#x1F` 与 `#x7F` (其中大多数不能出现在 XML 中);
空格 `#x20`; 分隔符 '<' `#x3C`, '>' `#x3E` 和 '"' `#x22`;
不安全的字符 '{' `#x7B`, '}' `#x7D`, '|' `#x7C`, '' `#x5C`=, '^' `#x5E` 和 '\`' `#x60`,
以及所有大于 `#x7F` 的字符. 由于转义并不总是一个完全可逆的过程,
因此转义**必须[MUST]**仅在绝对必要且在处理链中尽可能晚地执行. 特别的:

- 转换相对 URI 为绝对 URI 的过程;
- 将 URI 引用传递给负责解引用或是软件组件的过程;

**不应[SHOULD_NOT]**触发转义. 当转义发生时, **必须[MUST]**按以下方式执行:

1. 每个要转义字符都需表示为 UTF-8 [Unicode] 中的一个或多个字节.
2. 结束字节使用 URI 转义机制进行转义 (即转换为 `%HH` 的形式, 其中 `HH` 是字节值的十六进制表示).
3. 原始字符被结束字符序列替换,

> **注:**
> 在本规范的将来版本中, XML 核心工作组打算使用即将发布的 [RFC3987] 的修订版
> (将定义为 "Legacy Extended IRIs (LEIRIs)") 用以取代上述段落和步骤列表, 这将成为规范的规范性参考.
> 当上述修订版可用时, XML 核心工作组打算将其用于替换其监管下的任何未来的 XML 相关规范中类似上述的话术.

**定义**: 除系统标识符外, 外部标识符还可以包括一个公共标识符.

尝试检索实体内容的 XML 处理器可以使用公共标识符和系统标识符的任意组合, 以及本规范范围之外的其他信息,
用来尝试生成替代的 URI 引用. 如果处理器无法这样做, 则**必须[MUST]**使用系统标识符中指定的 URI 引用.
在尝试匹配之前, 公共标识符中的所有空白字符串**必须[MUST]**规范化为单个空格字符 (`#x20`),
并且**必须[MUST]**删除前导和尾随空白 (leading and trailing white).

外部实体声明示例:

```xml
<!ENTITY open-hatch
         SYSTEM "http://www.textuality.com/boilerplate/OpenHatch.xml">
<!ENTITY open-hatch
         PUBLIC "-//Textuality//TEXT Standard open-hatch boilerplate//EN"
         "http://www.textuality.com/boilerplate/OpenHatch.xml">
<!ENTITY hatch-pic
         SYSTEM "../grafix/OpenHatch.gif"
         NDATA gif >
```

> 译者注, 举个例子:
>
> ```xml
> <!ENTITY hatch-pic SYSTEM "../grafix/OpenHatch.gif" NDATA gif>
> <image>&hatch-pic;</image>
> ```

<!-- refs -->

[SECIONT#20.6]: 20-security_consideration.md#206-与-xml-实体相关的影响
[REF-XML#4.5]: https://www.w3.org/TR/xml/#intern-replacement
