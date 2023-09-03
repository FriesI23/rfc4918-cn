# 4. 资源属性的数据模型

## 4.1. 资源属性模型

属性是描述资源状态的一段数据。属性是描述数据的数据.

在分布式创作环境中, 属性用于高效地发现和管理资源. e.g. 通过主题属性可以对所有资源进行索引,
通过作者属性可以发现哪些作者写了哪些文档.

> 译者注: "资源" 通常指的是可以通过标识符或链接进行引用的外部数据或信息.
> 这些资源可以是图像, 文本文件, 音视频, 网页或其他类型的数据.
>
> ```xml
> <!-- URL资源 -->
> <image src="https://example.com/image.jpg" />
> <!-- CDATA资源 -->
> <script><![CDATA[function alertMessage() { alert(''); }]]></script>
> <!-- 媒体资源(base64编码) -->
> <image>iVBORw0KGgoA...AASUVORK5CYII=</image>
> ```

DAV 属性模型由名称与值的键值对组成. 属性名称用来标识属性的语法和语义,
并提供一个地址来引用其语法和语义.

这里存在两种属性类别: "活属性" 和 "死属性". 活属性的语法和语义由服务器强制, 包括以下情况：

1. 属性的值由服务器进行保护和维护
2. 属性的值由客户端维护, 但服务器对提交的值执行语法检查。

给定活属性的所有实例都必须符合与该属性名称相关联的定义。

死属性的语法和语义由客户端强制, 服务器仅记录属性的值.

## 4.2. 属性和 HTTP 标头

属性在有限的情况下已经存在于 Http 头消息中. 然而分布式创作环境中需要相对大量属性描述资源状态,
通过 HTTP 头设置或者返回所有这些属性是低效的. 因此需要一种机制,
允许正文识别并设置或检索感兴趣的一组属性.

## 4.3. 属性值

属性值始终是一个 (格式良好的) XML 片段.

选择使用 XML 是因为其支持丰富的模式定义, 并有弹性, 自描述, 结构化的数据格式,
同时支持多种字符集. XML 的自描述性质允许其通过添加元素来扩展任何属性的值.
由于其仍拥有在原始模式中指定的数据, 且**必须[MUST]**忽略不理解的元素,
导致客户端遇到扩展时不会发生崩溃.

XML 支持多种字符集, 且允许对任何可读的属性进行编码并让用户使用熟悉的字符集进行阅读.
XML 通过使用 `xml:lang` 属性来支持多种人类语言 (human languages),
同时处理同一字符集被多种语言使用的情况. 需要注意的是 `xml:lang` 的范围是递归的.
因此除非这个值被更具局部的属性覆盖, 包含属性名称元素的任何元素上的 `xml:lang`
属性都适用于该值. 同时需要注意, 在一种语言 (或者一种可能没有被定义的语言) 中属性只会有一个值;
属性不会在不同语言中存在多个值, 也不会一个值对应多种语言.

属性始终用包含属性名称的 XML 元素表示，称之为 "属性名称元素". 最简单的示例是一个空属性,
这与不存在的属性是不同的:

```xml
<R:title xmlns:R="http://www.example.com/ns/">
    <!-- empty property -->
</R:title>
```

属性值出现在属性名称元素的内部. 该值可以是任何包括纯文本和混合内容且格式良好的 XML 内容.
服务器在存储和传输死属性时必须保留以下 XML 信息项 (使用 [REC-XML-INFOSET] 中的术语):

对于属性名称元素自身的信息项:

- 命名空间名称 (namespace name)
- 本地名称 (local name)
- 属性 (attributes): 命名为 `xml:lang` 或在作用域内的任何类似的属性
- 子元素 (children): 元素或字符类型的子元素

对于属性值中所有元素的信息项:

- 命名空间名称 (namespace name)
- 本地名称 (local name)
- 属性 (attributes)
- 子元素 (children): 元素或字符类型的子元素

对于属性值中的属性信息项:

- 命名空间名称 (namespace name)
- 本地名称 (local name)
- 标准化值 (normalized value)

对于属性值中的字符信息项 :

- 字符编码 (character code)

由于一些 XML 词汇表 (e.g., `XPath`, `XML Schema`) 中使用了前缀,
因此服务器**应该[SHOULD]**保留值中以下任何信息项:

- 前缀 (prefix)

> 译者注: 前缀通常指的是在 XML 表达式中为 XML 命名空间中的元素和属性指定一个名称.
> 前缀可以对元素和属性进行逻辑分组, 防止名称冲突.
>
> ```xml
> <root xmlns:ns="http://example.com/ns">
>   <!-- ns是一个命名空间前缀, 其向命名空间 "http://example.com/ns" -->
>   <ns:element>Hello, XPath!</ns:element>
> </root>
> ```

未在上述内容中列出的 XML 信息集属性 (XML Infoset attributes)
**可能[MAY]**会被服务器保留, 但客户端**不能[MUST_NOT]**依赖这些属性是否被保留.
上述规则除非另有定义, 也默认适用于活属性.

如果存在 XML 属性 `xml:space`, 服务器**必须[MUST]**进行忽略,
并且绝不能将其用于改变空白处理. 属性值中的空白 (Whitespace) 是有意义的.

### 4.3.1. 示例 - 具有混合内容的属性

考虑一个由客户端创建的死属性 `author`, 如下所示:

```xml
<D:prop xml:lang="en" xmlns:D="DAV:">
    <x:author xmlns:x='http://example.com/ns'>
        <x:name>Jane Doe</x:name>
        <!-- Jane 的联系方式 -->
        <x:uri type='email' added='2005-11-26'>
            mailto:jane.doe@example.com
        </x:uri>
        <x:uri type='web' added='2005-11-27'>
            http://www.example.com
        </x:uri>
        <x:notes xmlns:h='http://www.w3.org/1999/xhtml'>
            Jane has been working way <h:em>too</h:em> long on the
            long-awaited revision of <![CDATA[<RFC2518>]]>.
        </x:notes>
    </x:author>
</D:prop>
```

当请求这个属性时, 服务器可能返回:

```xml
<D:prop xmlns:D='DAV:'>
    <author xml:lang='en'
            xmlns:x='http://example.com/ns'
            xmlns='http://example.com/ns'
            xmlns:h='http://www.w3.org/1999/xhtml'>
        <x:name>Jane Doe</x:name>
        <x:uri added="2005-11-26" type="email">
            mailto:jane.doe@example.com
        </x:uri>
        <x:uri added="2005-11-27" type="web">
            http://www.example.com
        </x:uri>
        <x:notes>
            Jane has been working way <h:em>too</h:em> long on the
            long-awaited revision of &lt;RFC2518&gt;.
        </x:notes>
    </author>
</D:prop>
```

在这个示例中需要注意:

- 属性名称本身的前缀由于不重要并没有被保留; 而其他所有前缀值都被保留.
- 属性值已经被用双引号而不是单引号进行重写 (引号样式并不重要), 且属性顺序不会被保留.
- `xml:lang` 属性在属性名称元素 (例子中为 `<author>`) 上返回 (该属性在设置时处于作用域内,
  但是响应中的位置并不重要, 只要其在作用域内即可)
- 标签间的空白被保留 (属性之间的空白则不然)
- `CDATA`封装被字符转义替代 (反之也是合法的)
- 注释被剥离 (处理指令也会被剥离)

实施说明: 在某些情况下, 比如编辑场景, 客户端可能需要逐字保留 XML 内容中的字符
(e.g., 属性顺序或引号样式). 在这种情况下,
客户端应当考虑转义所有在 XML 解析中具有特殊含义的字符, 使用纯文本的属性值.

## 4.4. 属性名称

属性名称是提供属性语法和语义信息架构关联的通用唯一标识符.

由于每一个属性的名称是通用且唯一的. 只要属性在相关资源上是"活"的,
并且其实现对于其定义是可行的, 客户端便可以依赖在同一或跨越不同服务器中多个资源属性的一致性.

XML 命名空间机制基于 [RFC3986] (URL). 由于可以防止命名空间冲突并提供不同程度的管理控制,
XML 命名空间被用于命名属性.

属性命名空间是平面 (flat) 的. 也就是说其没有明确的属性层次结构. 因此,
如果在一个资源上存在 `属性A` 和 `属性A/B`, 则无法识别这两个属性之间的任何关系.
预计最终将产生一个单独的规范以解决与层次属性相关的问题.

最后, 不能在同一个资源上重复定义属性, 因为这会导致资源的属性命名空间中冲突.

## 4.5. 原始资源与输出资源

一些 HTTP 资源是由服务器动态生成的. 对于这些资源, 可能存在一些源码用于控制如何生成该资源.
源文件与输出 HTTP 资源的关系可以是一对一, 一对多, 多对一或多对多的.
HTTP 中并没有机制来确定资源是否是动态的，更不用说其源文件在哪里或如何编写 (Author).
尽管这个问题将被得到有效的解决, 但是那些仅用于处理静态资源的可交互性 WebDAV 已经被广泛部署,
而它们并没有真正解决这个问题.
因此这个规范中没有解决源资源与输出不一致 (source vs output problam) 的问题,
该问题将被推迟到一个单独的文档中处理.
