# 15. DAV 属性

对于 DAV 属性，属性名称与包含其值的 XML 元素名称相同. 在下面的章节中, 每章的最后一行使用
[REC-XML] 中定义的格式给出了元素类型声明. 其中 "Value" 字段 (如果存在) 使用 BNF 指定对
XML 元素允许内容的进一步限制 (i.e., 进一步限制 PCDATA 元素的值).

受保护属性 (protected property) 是指不能通过 PROPPATCH 请求更改的属性.
可能还有其他请求会导致受保护属性发生更改 (例如, 当 LOCK 请求影响 DAV:lockdiscovery
的值时). 需要注意的是, 给定属性可以在一种类型的资源上被保护, 但在另一种类型的资源上不被保护.

可计算属性 (computed property) 是指其值基于计算定义的属性 (基于该资源,
甚至是其他资源的内容和其他属性). 可计算属性始终是一个受保护属性.

COPY 和 MOVE 行为指的是本地 COPY 和 MOVE 操作.

对于基于 HTTP GET 响应标头 (`DAV:get*`) 定义的属性, 标头值可以包含如 [RFC2616#4.2]
中定义的 LWS (线性空白, Linear White Space). 服务器实现者在使用这些值作为 WebDAV
属性值之前, **应该** (SHOULD) 去除这些值中的 LWS.

## 15.1. creationdate 属性

- **名称**: creationdate
- **目的**: 记录资源创建的时间和日期
- **数值**: date-time (在 [RFC3339#5.6] 中关于 ABNF 的定义)
- **保护**: **可能** (MAY) 是受保护的. 某些服务器允许修改 DAV:creationdate
  以反映文档创建的时间, 如果这个时间对用户来说是更有意义的 (而不是使用上传的时间). 因此,
  客户端**不应** (SHOULD NOT) 在同步逻辑中使用这个属性 (应该使用 DAV:getetag).
- **COPY/MOVE 行为**: 此属性值**应该** (SHOULD) 在 MOVE 操作期间保持不变,
  但该值通常在使用 COPY 创建资源时被重新初始化. 不应在使用 COPY 时设置它.
- **描述**: DAV:creationdate 属性应该在所有符合 DAV 规范的资源上定义. 如果该属性存在,
  应包含资源创建的时间戳. 无法持久记录创建日期的服务器**应该** (SHOULD) 保留该值为未定义的
  (i.e., 回报为 "Not Found").

```xml
<!ELEMENT creationdate (#PCDATA) >
```
