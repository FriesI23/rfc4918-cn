# 14. XML 元素定义 (XML Element Definitions)

在本章节中，每个小节的最后一行使用 [REC-XML] 中定义的格式给出了元素类型声明. 如果存在
"Value" 字段, 则会使用 `BNF` 对 XML 元素内的允许内容进行进一步限制 (i.e., 进一步限制
PCDATA 元素的值). 需要注意的是,
这里定义的所有元素都可以根据[第 17 章]()中定义的规则进行扩展.这里定义的所有元素都属于
"DAV:" 命名空间.

> 译者注: 可以先移步[第 17 章]()查看 BNF 语法在该文档中的定义, 再回来看本章给出的元素声明.

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

## 14.5. error XML 元素 (error XML Element)

- **名称**: error
- **目的**: 错误响应, 特别是 403 Forbidden 和 409 Conflict,
  有时需要更多的信息来指示具体是什么问题. 在这些情况下, 服务器**可能** (MAY) 返回一个
  XML 响应正文, 包含一个名为 "error" 的文档元素, 该文档元素内部包含标识特定条件码子元素.
- **描述**: 至少包含一个 XML 元素，并且**不得** (MUST NOT) 包含文本或混合内容.
  "error" 元素的任何子元素都被认为是一个前置或后置条件码.
  无法识别的元素**必须** (MUST) 被忽略.

```xml
<!ELEMENT error ANY >
```

## 14.6. exclusive XML 元素 (exclusive XML Element)

- **名称**: exclusive
- **目的**: 指定一个排他锁

```xml
<!ELEMENT exclusive EMPTY >
```

## 14.7. href XML 元素 (href XML Element)

- **名称**: href
- **目的**: **必须** (MUST) 包含一个 URI 或者一个相对引用.
- **描述**: "href" 的值, 根据其使用的上下文, 可能存在一些限制.
  参考使用了 "href" 的相关规范, 了解在每种情况下适用的限制.
- **数值**: Simple-ref

```xml
<!ELEMENT href (#PCDATA)>
```

## 14.8. include XML 元素 (include XML Element)

- **名称**: include
- **目的**: 'include' XML 元素的任意子元素都代表一个包含在 PROPFIND 响应中的属性名称.
  在 "include" XML 元素中的所有元素**必须** (MUST) 定义与资源相关的属性,
  尽管可能的属性名称不仅仅局限于本文档或其他标准中定义的名字.
  该元素**不能** (MUST NOT) 包含文本或混合内容.

```xml
<!ELEMENT include ANY >
```

## 14.9. location XML 元素 (location XML Element)

- **名称**: location
- **目的**: HTTP 在一些状态码 (如 201 和 300 系列状态码) 中定义 "Location" 标头 (参见
  [RFC2616#14.30]). 当这些状态码在 "multistatus" 元素内使用时, 可以使用 "location"
  元素来提供相应的 Location 标头值。
- **描述**: 包含一个单独的 href 元素, 其值与 Location 标头中使用的值相同.

```xml
<!ELEMENT location (href)>
```

## 14.10. lockentry XML 元素 ( lockentry XML Element)

- **名称**: lockentry

- **目的**: 定义可与资源一起使用的锁类型.

```xml
<!ELEMENT lockentry (lockscope, locktype) >
```

## 14.11. lockinfo XML Element (lockinfo XML 元素)

- **名称**: lockinfo

- **目的**: "lockinfo" XML 元素用于在 LOCK 方法指定客户端希望创建的锁类型.

```xml
<!ELEMENT lockinfo (lockscope, locktype, owner?)  >
```

## 14.12. lockroot XML 元素 (lockroot XML Element)

- **名称**: lockroot

- **目的**: 包含锁的根 URL, 即在 LOCK 请求中用于寻址资源的 URL.

- **描述**: href 元素包含锁根. 服务器**应该** (SHOULD) 在所有 "DAV:lockdiscovery"
  属性值和 LOCK 请求的响应中包含它.

```xml
<!ELEMENT lockroot (href) >
```

## 14.13. lockscope XML 元素 (lockscope XML Element)

- **名称**: lockscope

- **目的**: 指定该锁是独占锁还是共享锁.

```xml
<!ELEMENT lockscope (exclusive | shared) >
```

## 14.14. locktoken XML 元素 (locktoken XML Element)

- **名称**: locktoken

- **目的**: 与锁关联的锁令牌。

- **描述**: href 包含一个单独的指向该锁的锁令牌 URI.

```xml
<!ELEMENT locktoken (href) >
```

## 14.15. locktype XML 元素 (locktype XML Element)

- **名称**: locktype

- **目的**: 指定锁的访问类型. 本规范目前仅定义了一种锁类型, 即写入锁 (write lock).

```xml
   <!ELEMENT locktype (write) >
```

## 14.16. multistatus XML 元素 (multistatus XML Element)

- **名称**: multistatus

- **目的**: 包含多个响应消息.

- **描述**: 位于最上层的 "responsedescription" 元素用于提供一个概括性的消息,
  用来描述响应的总体性质. 如果有该值, 应用可以使用它, 而不是显示包含在响应中的各个响应描述.

```xml
<!ELEMENT multistatus (response*, responsedescription?)  >
```

## 14.17. owner XML 元素 (owner XML Element)

- **名称**: owner

- **目的**: 包含有关锁创建者的客户端提供 (client-supplied) 的信息.

- **描述**: 允许客户端提供足够的信息, 用于直接联系主体 (例如, 电话号码或电子邮件 URI),
  或者用于发现创建锁主体 (例如, 主页的 URL). 所提供的值按照 XML 信息项保存而言,
  **必须** (MUST) 按照死属性来处理. 除非客户端提供的 owner 值为空, 服务器**不得**
  (MUST NOT) 更改该值. 为了在不同客户端实现之间一定程度的互操作性,
  如果客户端拥有适合用户显示的锁创建者的 URI-formatted 联系信息,
  那么客户端**应该** (SHOULD) 将这些 URI 放入 "owner" 元素的 "href" 子元素中.

- **可扩展性**: 可以使用子元素, 混合内容, 文本内容或属性进行扩展.

```xml
<!ELEMENT owner ANY >
```

## 14.18. prop XML 元素 (prop XML Element)

- **名称**: prop

- **目的**: 包含与资源相关的属性.

- **描述**: 一个定义在资源上属性的通用容器. "prop" XML 元素内部的所有元素**必须** (MUST)
  定义与资源相关的属性, 尽管其中可能的属性名称不受限于本文档或其他标准中定义的属性名称.
  此元素**不得** (MUST NOT) 包含文本或混合内容.

```xml
<!ELEMENT prop ANY >
```

## 14.19. propertyupdate XML 元素 (propertyupdate XML Element)

- **名称**: propertyupdate

- **目的**: 包含对资源上属性进行更改的请求.

- **描述**: 此 XML 元素是一个容器, 用于包含修改资源属性所需的信息.

```xml
<!ELEMENT propertyupdate (remove | set)+ >
```

## 14.20. propfind XML 元素 (propfind XML Element)

- **名称**: propfind
- **目的**: 用于指定从 PROPFIND 方法中需要返回的属性. 针对 "propfind" 的使用,
  指定了四个特殊元素: 'prop', 'allprop', 'include' 和 'propname'.
  如果在 'propfind' 中使用了 'prop', 则 'prop' 内部**不能** (MUST NOT) 包含属性值.

```xml
<!ELEMENT propfind ( propname | (allprop, include?) | prop ) >
```
