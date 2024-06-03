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

```bnf
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

## Status-Line

```bnf
Status-Line = HTTP-Version SP Status-Code SP Reason-Phrase CRLF

HTTP-Version   = "HTTP" "/" 1*DIGIT "." 1*DIGIT

Status-Code    =
      "100"  ; Section 10.1.1: Continue
      | "101"  ; Section 10.1.2: Switching Protocols
      | "200"  ; Section 10.2.1: OK
      | "201"  ; Section 10.2.2: Created
      | "202"  ; Section 10.2.3: Accepted
      | "203"  ; Section 10.2.4: Non-Authoritative Information
      | "204"  ; Section 10.2.5: No Content
      | "205"  ; Section 10.2.6: Reset Content
      | "206"  ; Section 10.2.7: Partial Content
      | "300"  ; Section 10.3.1: Multiple Choices
      | "301"  ; Section 10.3.2: Moved Permanently
      | "302"  ; Section 10.3.3: Found
      | "303"  ; Section 10.3.4: See Other
      | "304"  ; Section 10.3.5: Not Modified
      | "305"  ; Section 10.3.6: Use Proxy
      | "307"  ; Section 10.3.8: Temporary Redirect
      | "400"  ; Section 10.4.1: Bad Request
      | "401"  ; Section 10.4.2: Unauthorized
      | "402"  ; Section 10.4.3: Payment Required
      | "403"  ; Section 10.4.4: Forbidden
      | "404"  ; Section 10.4.5: Not Found
      | "405"  ; Section 10.4.6: Method Not Allowed
      | "406"  ; Section 10.4.7: Not Acceptable
      | "407"  ; Section 10.4.8: Proxy Authentication Required
      | "408"  ; Section 10.4.9: Request Time-out
      | "409"  ; Section 10.4.10: Conflict
      | "410"  ; Section 10.4.11: Gone
      | "411"  ; Section 10.4.12: Length Required
      | "412"  ; Section 10.4.13: Precondition Failed
      | "413"  ; Section 10.4.14: Request Entity Too Large
      | "414"  ; Section 10.4.15: Request-URI Too Large
      | "415"  ; Section 10.4.16: Unsupported Media Type
      | "416"  ; Section 10.4.17: Requested range not satisfiable
      | "417"  ; Section 10.4.18: Expectation Failed
      | "500"  ; Section 10.5.1: Internal Server Error
      | "501"  ; Section 10.5.2: Not Implemented
      | "502"  ; Section 10.5.3: Bad Gateway
      | "503"  ; Section 10.5.4: Service Unavailable
      | "504"  ; Section 10.5.5: Gateway Time-out
      | "505"  ; Section 10.5.6: HTTP Version not supported
      | extension-code

extension-code = 3DIGIT

Reason-Phrase  = *<TEXT, excluding CR, LF>

CRLF           = CR LF
SP             = <US-ASCII SP, space (32)>
CR             = <US-ASCII CR, carriage return (13)>
LF             = <US-ASCII LF, linefeed (10)>
```

```text
HTTP/1.0 404 Not Found
HTTP/1.1 200 OK
HTTP/1.1 500 Internal Server Error
```

参考: [RFC2612#6.1](https://datatracker.ietf.org/doc/html/rfc2616#section-6.1)

## date-time

```bnf
date-time       = full-date "T" full-time

full-date       = date-fullyear "-" date-month "-" date-mday
full-time       = partial-time time-offset

partial-time    = time-hour ":" time-minute ":" time-second
                  [time-secfrac]

date-fullyear   = 4DIGIT
date-month      = 2DIGIT  ; 01-12
date-mday       = 2DIGIT  ; 01-28, 01-29, 01-30, 01-31 based on
                           ; month/year

time-offset     = "Z" / time-numoffset
time-numoffset  = ("+" / "-") time-hour ":" time-minute
time-secfrac    = "." 1*DIGIT

time-hour       = 2DIGIT  ; 00-23
time-minute     = 2DIGIT  ; 00-59
time-second     = 2DIGIT  ; 00-58, 00-59, 00-60 based on leap second
                           ; rules
```

```text
// utc
2023-06-03T14:23:30Z
// +offset
2024-06-03T14:23:30+05:30
// with milliseconds
2024-01-01T00:00:00.123-05:00
```

参考: [RPC3339#5.6](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6)

## language-tag

```bnf
language-tag  = primary-tag *( "-" subtag )

primary-tag   = 1*8ALPHA
subtag        = 1*8ALPHA
```

```text
zh
zh-CN
zh-Hant-TW
```

参考: [RFC2616#3.10](https://datatracker.ietf.org/doc/html/rfc2616#section-3.10)

## media-type

```bnf
media-type     = type "/" subtype *( ";" parameter )

type           = token
subtype        = token
```

`token` 见[这里](#token).

```text
text/plain
application/json
application/octet-stream; charset=ISO-8859-1
application/xml; version=1.0
application/javascript; charset=UTF-8; version=ECMA-26
```

参考: [RFC2616#3.7](https://datatracker.ietf.org/doc/html/rfc2616#section-3.7)

## rfc1123-date

```bnf
rfc1123-date = wkday "," SP date1 SP time SP "GMT"

date1        = 2DIGIT SP month SP 4DIGIT
               ; day month year (e.g., 02 Jun 1982)

time         = 2DIGIT ":" 2DIGIT ":" 2DIGIT
               ; 00:00:00 - 23:59:59
wkday        = "Mon" | "Tue" | "Wed"
            | "Thu" | "Fri" | "Sat" | "Sun"
month        = "Jan" | "Feb" | "Mar" | "Apr"
            | "May" | "Jun" | "Jul" | "Aug"
            | "Sep" | "Oct" | "Nov" | "Dec"
```

```text
Fri, 02 Jun 1982 14:30:00 GMT
```

参考: [RFC2616#3.3.1](https://datatracker.ietf.org/doc/html/rfc2616#section-3.3.1)
