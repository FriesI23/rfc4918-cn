# 14. XML 元素定义 (XML Element Definitions)

在本章节中，每个小节的最后一行使用 [REC-XML] 中定义的格式给出了元素类型声明. 如果存在
"Value" 字段, 则会使用 `BNF` 对 XML 元素内的允许内容进行进一步限制 (i.e., 进一步限制
PCDATA 元素的值). 需要注意的是, 这里定义的所有元素都可以根据[第 17 章]中定义的规则进行扩展.
这里定义的所有元素都属于 "DAV:" 命名空间.

## 14.1. activelock XML 元素 (activelock XML Element)

- **名称**: activelock
- **目的**: 描述一个资源上的锁.

```xml
<!ELEMENT activelock (lockscope, locktype, depth, owner?, timeout?,
            locktoken?, lockroot)>
```

## 14.2. allprop XML 元素 (allprop XML Element)

- **名称**: allprop
- **目的**: 指定要返回资源上存在的所有死属性和本文档中定义活属性的名称和值.

```xml
<!ELEMENT allprop EMPTY >
```

## 14.3. collection XML 元素 (collection XML Element)

- **名称**: collection
- **目的**: 将相关资源标识为集合. 集合资源的 `DAV:resourcetype` 属性中**必须** (MUST)
  包含此元素. 通常它是空的，但一些扩展可能会为其添加子元素.

```xml
<!ELEMENT collection EMPTY >
```

## 14.4. depth XML 元素 (depth XML Element)

- **名称**: depth
- **目的**: 用于表示 XML 内容中的深度 (e.g., 在锁信息中).
- **取值**: "0" | "1" | "infinity"

```xml
<!ELEMENT depth (#PCDATA) >
```
