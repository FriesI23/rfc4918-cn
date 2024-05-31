# 规则定义

本附录列出了该文档中出现的以及由其他文档引用的由 `BNF` 定义的规则.

## Simple-ref

```bnf
Simple-ref = absolute-URI | ( path-absolute [ "?" query ] )
```

`Simple-ref` `=` [`absolute-URI`](#absolute-uri) `|` `(` [`path-absolute`](#path-absolute) `[` `"?"` [`query`](#query) `]` `)`

```text
// Simple-ref = absolute-URI
https://www.example.com/resource?id=123&name=value

// Simple-ref = path-absolute [ "?" query ]
/path/to/resource?search=test
```

参考: [8.3. 处理 URL](8-general_request_and_response_handling.md#83-处理-url)

## Coded-URL

```bnf
Coded-URL        = "<" absolute-URI ">"
```

`Coded-URL` `=` `"<"` [`absolute-URI`](#absolute-uri) `">"`

```text
<http://example.com/extensions/my-extension>
```

## DAV

```bnf
DAV              = "DAV" ":" #( compliance-class )
compliance-class = ( "1" | "2" | "3" | extend )
extend           = Coded-URL | token
Coded-URL        = "<" absolute-URI ">"
```

`extend` `=` [`Coded-URL`](#coded-url) `|` [`token`](#token)

```text
// DAV = "DAV" ":" "1"
DAV:1
DAV:1,2
DAV:3
// DAV = "DAV" ":" Coded-URL
DAV:<http://example.com/extensions/my-extension>
// DAV = "DAV" ":" token
DAV:my-token
```

## Depth

```dnf
Depth = "Depth" ":" ("0" | "1" | "infinity")
```

```text
Depth:0
Depth:1
Depth:infinity
```

## Destination

```bnf
Destination = "Destination" ":" Simple-ref
```

`Destination` `=` `"Destination"` `":"` [`Simple-ref`](#simple-ref)

## If

```bnf
If = "If" ":" ( 1*No-tag-list | 1*Tagged-list )

No-tag-list = List
Tagged-list = Resource-Tag 1*List

List = "(" 1*Condition ")"
Condition = ["Not"] (State-token | "[" entity-tag "]")
State-token = Coded-URL

Resource-Tag = "<" Simple-ref ">"
```

`Condition` `=` `["Not"]` `(State-token` `|` `"["` [`entity-tag`](#entity-tag) `"]")`
`State-token` `=` [`Coded-URL`](#coded-url)
`Resource-Tag` `=` `"<"` [`Simple-ref`](#simple-ref) `">"`

```text
// If = "If" ":" ( 1*( "(" 1*Coded-URL  ")" ) )
If: (<http://example.com/resource1>)
// If = "If" ":" ( 1*( "<" Simple-ref ">" "(" 1*( "Not" Coded-URL )  ")"  )  )
If: <http://example.com/resource1> (Not <http://example.com/resource2>)
```

## Lock-Token

```bnf
Lock-Token = "Lock-Token" ":" Coded-URL
```

`Lock-Token` `=` `"Lock-Token"` `":"` [`Coded-URL`](#coded-url)

```text
Lock-Token: <http://example.com/extensions/my-extension>
```

## Overwrite

```bnf
Overwrite = "Overwrite" ":" ("T" | "F")
```

```text
Overwrite: T
Overwrite: F
```

## Timeout

```bnf
TimeOut  = "Timeout" ":" 1#TimeType
TimeType = ("Second-" DAVTimeOutVal | "Infinite")
DAVTimeOutVal = 1*DIGIT

DIGIT    = <any US-ASCII digit "0".."9">
```

```text
Timeout: Second-30
Timeout: Second-30 Second-60
Timeout: Infinite Second-4100000000 Second-60
```

---------------------------------------------------

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

## token

```bnf
token          = 1*<any CHAR except CTLs or separators>
separators     = "(" | ")" | "<" | ">" | "@"
               | "," | ";" | ":" | "\" | <">
               | "/" | "[" | "]" | "?" | "="
               | "{" | "}" | SP | HT
SP             = <US-ASCII SP, space (32)>
HT             = <US-ASCII HT, horizontal-tab (9)>
```

```text
//valid
exToken
token123
some_token
another-token
//invalid - with ',', '@', ... (seperators)
invalid,token
some@token
token:123
```

参考: [RFC2616#2.2](https://datatracker.ietf.org/doc/html/rfc2616#section-2.2)

## entity-tag

```bnf
entity-tag = [ weak ] opaque-tag
weak       = "W/"
opaque-tag = quoted-string

quoted-string  = ( <"> *(qdtext | quoted-pair ) <"> )
qdtext         = <any TEXT except <">>
quoted-pair    = "\" CHAR
```

```text
// entity-tag = weak quoted-string
W/"example"
// entity-tag quoted-string
"example"
// with quoted-pair
"exa\"mple"
```

参考: [RFC2612#3.11](https://datatracker.ietf.org/doc/html/rfc2616#section-3.11)
