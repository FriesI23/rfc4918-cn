# 3. 术语 (Terminology)

## URI/URL

包括统一资源标识符 (Uniform Resource Identifier) 和统一资源定位符
(Uniform Resource Locator). 这些术语（以及它们之间的区别）在 [RFC3986] 中有详细定义。

## URI/URL 映射

代表绝对 URI 和资源之间的关系.
由于资源 (Resource) 可以表示那些可或者不可通过网络检索的项目, 因此资源可能具有
0, 1 或者 n 个 URI 映射. 将资源影杀到 "http" 协议 URI 的设计, 使得我的可以使用 URI
向资源提交 HTTP 请求.

## 路径段 (Path Segment)

非正式地说, URI 中斜线（"/"）之间的字符. 正式地说, 在 [RFC3986#3.3] 中定义.

## 集合 (Collection)

非正式地说, 集合是一个资源 (resource), 同时也作为包含对其子资源的引用的容器.
正式地说, 它是包含[路径段](#路径段-path-segment)与资源 (Resources) 之间映射的集合,
并满足[第五章](./5_collection_of_web_resources.md)中定义的要求.

## 集合的内部成员 (Internal Member (of a Collection))

非正式地说, 它是集合的子资源.
正式地说, 它是由集合中包含的[路径段](#路径段-path-segment)映射引用的资源.

## 集合的内部成员 URL (Internal Member URL (of a Collection))

集合的内部成员的 URL 由集合的 URL（包括尾部'/'）
和标识内部成员的[路径段](#路径段-path-segment)组成.

## 集合的成员 (Member (of a Collection))

非正式地说, 它是集合的"后代". 正式地说,
它是[集合的内部成员](#集合的内部成员-internal-member-of-a-collection).
或者用递归地说, 是一个内部成员的成员.

## 集合的成员 URL (Member URL of a Collection)

可以是集合本身的内部成员 URL, 也可以是该集合的成员的内部成员 URL.

## 属性 (Property)

一个包含有关资源的描述性信息的名称与值键值对.

## 活属性 (Live Property)

由服务器强制其语义和语法的[属性](#属性-property). e.g., 活属性 `DAV:getcontentlength`
的值表示实体的长度, 该值由服务器自动计算并可以使用 GET 方法返回.

## 死属性 (Dead Property)

服务器不强制其语义和语法的属性. 服务器只记录死属性的值; 客户端负责维护其语法和语义的一致性.

## 主体 (Principal)

发起对网络资源访问的特定角色 (人或者计算资源).

## 状态令牌 (State Token)

代表资源状态的 URI. 锁令牌 (Lock tokens) 是本规范中唯一定义的状态令牌.
