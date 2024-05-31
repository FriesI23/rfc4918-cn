# 规则定义

本附录列出了该文档中出现的以及由其他文档引用的由 `BNF` 定义的规则.

## Simple-ref

`Simple-ref` = [absolute-URI](#absolute-uri) | ( [path-absolute](#path-absolute) [ "?" [query](#query) ] )

```bnf
Simple-ref = absolute-URI | ( path-absolute [ "?" query ] )
```

```text
// Simple-ref = absolute-URI
https://www.example.com/resource?id=123&name=value

// Simple-ref = path-absolute [ "?" query ]
/path/to/resource?search=test
```

参考: [8.3. 处理 URL](8-general_request_and_response_handling.md#83-处理-url)

---

## absolute-URI

```bnf
absolute-URI = scheme ":" hier-part [ "?" query ]
```

```text
https://www.example.com/resource?id=123&name=value
----- | ----------------------- | -------------
scheme         hier-part           ? query
```

参考: [RFC3986#4.3](https://datatracker.ietf.org/doc/html/rfc3986#section-4.3)

## path-absolute

```bnf
path-absolute = "/" [ segment-nz *( "/" segment ) ]
```

```text
/thisisalongrootpath/applications/somethingelse
- | ------------- | - | ------
/   segment-nz     /   segment
```

参考: [RFC3986#3.3](https://datatracker.ietf.org/doc/html/rfc3986#section-3.3)

## query

```bnf
query = *( pchar / "/" / "?" )
```

```text
path=/folder/subfolder?param=value&name=value
------------------------------- | - | -----
   include "/" "?"                &   another query param
```

参考: [RFC3986#3.4](https://datatracker.ietf.org/doc/html/rfc3986#section-3.4)
