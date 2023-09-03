# RFC 4918 中文文档

## 状态

施工中

## 进度

- [x] 1. Introduction
- [x] 2. Notational Conventions
- [x] 3. Terminology
- [x] 4. Data Model for Resource Properties
  - [x] 4.1. The Resource Property Model
  - [x] 4.2. Properties and HTTP Headers
  - [x] 4.3. Property Values
    - [x] 4.3.1. Example - Property with Mixed Content
  - [x] 4.4. Property Names
  - [x] 4.5. Source Resources and Output Resources
- [x] 5. Collections of Web Resources
  - [x] 5.1. HTTP URL Namespace Model
  - [x] 5.2. Collection Resources
- [ ] 6. Locking
  - [ ] 6.1. Lock Model
  - [ ] 6.2. Exclusive vs. Shared Locks
  - [ ] 6.3. Required Support
  - [ ] 6.4. Lock Creator and Privileges
  - [ ] 6.5. Lock Tokens
  - [ ] 6.6. Lock Timeout
  - [ ] 6.7. Lock Capability Discovery
  - [ ] 6.8. Active Lock Discover
- [ ] 7. Write Lock
  - [ ] 7.1. Write Locks and Properties
  - [ ] 7.2. Avoiding Lost Updates
  - [ ] 7.3. Write Locks and Unmapped URLs
  - [ ] 7.4. Write Locks and Collections
  - [ ] 7.5. Write Locks and the If Request Header
    - [ ] 7.5.1. Example - Write Lock and COPY
    - [ ] 7.5.2 Example - Deleting a Member of a Locked Collection
  - [ ] 7.6. Write Locks and COPY/MOVE
  - [ ] 7.7. Refreshing Write Locks
- [x] 8. General Request and Response Handling
  - [x] 8.1. Precedence in Error Handling
  - [x] 8.2. Use of XML
  - [x] 8.3. URL Handling
    - [x] 8.3.1. Example - Correct URL Handling
  - [x] 8.4. Required Bodies in Requests
  - [x] 8.5. HTTP Headers for Use in WebDAV
  - [x] 8.6. ETag
  - [x] 8.7. Including Error Response Bodies
  - [x] 8.8. Impact of Namespace Operations on Cache Validators
- [x] 9. HTTP Methods for Distributed Authoring
  - [x] 9.1. PROPFIND Method
    - [x] 9.1.1. PROPFIND Status Codes
    - [x] 9.1.2. Status Codes for Use in 'propstat' Element
    - [x] 9.1.3. Example - Retrieving Named Properties
    - [x] 9.1.4. Example - Using 'propname' to Retrieve All Property Name
    - [x] 9.1.5. Example - Using So-called 'allprop'
    - [x] 9.1.6. Example - Using 'allprop' with 'include'
  - [x] 9.2. PROPPATCH Method
    - [x] 9.2.1. Status Codes for Use in 'propstat' Element
    - [x] 9.2.2. Example - PROPPATCH
  - [x] 9.3. MKCOL Method
    - [x] 9.3.1. MKCOL Status Codes
    - [x] 9.3.2. Example - MKCOL
  - [x] 9.4. GET, HEAD for Collections
  - [x] 9.5. POST for Collections
  - [x] 9.6. DELETE Requirements
    - [x] 9.6.1. DELETE for Collections
    - [x] 9.6.2. Example - DELETE
  - [x] 9.7. PUT Requirements
    - [x] 9.7.1. PUT for Non-Collection Resources
    - [x] 9.7.2. PUT for Collections
  - [x] 9.8. COPY Method
    - [x] 9.8.1. COPY for Non-collection Resources
    - [x] 9.8.2. COPY for Properties
    - [x] 9.8.3. COPY for Collections
    - [x] 9.8.4. COPY and Overwriting Destination Resources
    - [x] 9.8.5. Status Codes
    - [x] 9.8.6. Example - COPY with Overwrite
    - [x] 9.8.7. Example - COPY with No Overwrite
    - [x] 9.8.8. Example - COPY of a Collection
  - [x] 9.9. MOVE Method
    - [x] 9.9.1. MOVE for Properties
    - [x] 9.9.2. MOVE for Collections
    - [x] 9.9.3. MOVE and the Overwrite Header
    - [x] 9.9.4. Status Codes
    - [x] 9.9.5. Example - MOVE of a Non-Collection
    - [x] 9.9.6. Example - MOVE of a Collection
  - [ ] 9.10. LOCK Method
    - [ ] 9.10.1. Creating a Lock on an Existing Resource
    - [ ] 9.10.2. Refreshing Locks
    - [ ] 9.10.3. Depth and Locking
    - [ ] 9.10.4. Locking Unmapped URLs
    - [ ] 9.10.5. Lock Compatibility Table
    - [ ] 9.10.6. LOCK Responses
    - [ ] 9.10.7. Example - Simple Lock Request
    - [ ] 9.10.8. Example - Refreshing a Write Lock
    - [ ] 9.10.9. Example - Multi-Resource Lock Request
  - [ ] 9.11 UNLOCK Method
    - [ ] 9.11.1. Status Codes
    - [ ] 9.11.2. Example - UNLOCK
- [x] 10. HTTP Headers for Distributed Authoring
  - [x] 10.1. DAV Header
  - [x] 10.2. Depth Header
  - [x] 10.3. Destination Header
  - [x] 10.4. If Header
    - [x] 10.4.1. Purpose
    - [x] 10.4.2. Syntax
    - [x] 10.4.3. List Evaluation
    - [x] 10.4.4. Matching State Tokens and ETags
    - [x] 10.4.5. If Header and Non-DAV-Aware Proxies
    - [x] 10.4.6. Example - No-tag Production
    - [x] 10.4.7. Example - Using "Not" with No-tag Production
    - [x] 10.4.8. Example - Causing a Condition to Always Evaluate to True
    - [x] 10.4.9. Example - Tagged List If Header in COPY
    - [x] 10.4.10. Example - Matching Lock Tokens with Collection Locks
    - [x] 10.4.11. Example - Matching ETags on Unmapped URLs
  - [x] 10.5. Lock-Token Header
  - [x] 10.6. Overwrite Header
  - [x] 10.7. Timeout Request Header
- [x] 11. Status Code Extensions to HTTP/1.1
  - [x] 11.1. 207 Multi-Status
  - [x] 11.2. 422 Unprocessable Entity
  - [x] 11.3. 423 Locked
  - [x] 11.4. 424 Failed Dependency
  - [x] 11.5. 507 Insufficient Storage
- [x] 12. Use of HTTP Status Codes
  - [x] 12.1. 412 Precondition Failed
  - [x] 12.2. 414 Request-URI Too Long
- [x] 13. Multi-Status Response
  - [x] 13.1. Response Headers
  - [x] 13.2. Handling Redirected Child Resources
  - [x] 13.3. Internal Status Codes
- [x] 14. XML Element Definitions
  - [x] 14.1. activelock XML Element
  - [x] 14.2. allprop XML Element
  - [x] 14.3. collection XML Element
  - [x] 14.4. depth XML Element
  - [x] 14.5. error XML Element
  - [x] 14.6. exclusive XML Element
  - [x] 14.7. href XML Element
  - [x] 14.8. include XML Element
  - [x] 14.9. location XML Element
  - [x] 14.10. lockentry XML Element
  - [x] 14.11. lockinfo XML Element
  - [x] 14.12. lockroot XML Element
  - [x] 14.13. lockscope XML Element
  - [x] 14.14. locktoken XML Element
  - [x] 14.15. locktype XML Element
  - [x] 14.16. multistatus XML Element
  - [x] 14.17. owner XML Element
  - [x] 14.18. prop XML Element
  - [x] 14.19. propertyupdate XML Element
  - [x] 14.20. propfind XML Element
  - [x] 14.21. propname XML Element
  - [x] 14.22. propstat XML Element
  - [x] 14.23. remove XML Element
  - [x] 14.24. response XML Element
  - [x] 14.25. responsedescription XML Element
  - [x] 14.26. set XML Element
  - [x] 14.27. shared XML Element
  - [x] 14.28. status XML Element
  - [x] 14.29. timeout XML Element
  - [x] 14.30. write XML Element
- [x] 15. DAV Properties
  - [x] 15.1. creationdate Property
  - [x] 15.2. displayname Property
  - [x] 15.3. getcontentlanguage Property
  - [x] 15.4. getcontentlength Property
  - [x] 15.5. getcontenttype Property
  - [x] 15.6. getetag Property
  - [x] 15.7. getlastmodified Property
  - [x] 15.8. lockdiscovery Property
    - [x] 15.8.1. Example - Retrieving DAV:lockdiscovery
  - [x] 15.9. resourcetype Property
  - [x] 15.10. supportedlock Property
  - [x] 15.10.1. Example - Retrieving DAV:supportedlock
- [ ] 16. Precondition/Postcondition XML Elements
- [ ] 17. XML Extensibility in DAV
- [ ] 18. DAV Compliance Classes
  - [ ] 18.1. Class 1
  - [ ] 18.2. Class 2
  - [ ] 18.3. Class 3
- [ ] 19. Internationalization Considerations
- [ ] 20. Security Considerations
  - [ ] 20.1. Authentication of Clients
  - [ ] 20.2. Denial of Service
  - [ ] 20.3. Security through Obscurity
  - [ ] 20.4. Privacy Issues Connected to Locks
  - [ ] 20.5. Privacy Issues Connected to Properties
  - [ ] 20.6. Implications of XML Entities
  - [ ] 20.7. Risks Connected with Lock Tokens
  - [ ] 20.8. Hosting Malicious Content
- [ ] 21. IANA Considerations
  - [ ] 21.1. New URI Schemes
  - [ ] 21.2. XML Namespaces
  - [ ] 21.3. Message Header Fields
    - [ ] 21.3.1. DAV
    - [ ] 21.3.2. Depth
    - [ ] 21.3.3. Destination
    - [ ] 21.3.4. If
    - [ ] 21.3.5. Lock-Token
    - [ ] 21.3.6. Overwrite
    - [ ] 21.3.7. Timeout
  - [ ] 21.4. HTTP Status Codes
- [ ] 22. Acknowledgements
- [ ] 23. Contributors to This Specification
- [ ] 24. Authors of RFC 2518
- [ ] 25. References
  - [ ] 25.1. Normative References
  - [ ] 25.2.Informative References
- [ ] A. Notes on Processing XML Elements
  - [ ] A.1. Notes on Empty XML Elements
  - [ ] A.2. Notes on Illegal XML Processing
  - [ ] A.3. Example - XML Syntax Error
  - [ ] A.4. Example - Unexpected XML Element
- [ ] B. Notes on HTTP Client Compatibility
- [ ] C. The 'opaquelocktoken' Scheme and URIs
- [ ] D. Lock-null Resources
  - [ ] D.1. Guidance for Clients Using LOCK to Create Resources
- [ ] E. Guidance for Clients Desiring to Authenticate
- [ ] F. Summary of Changes from RFC 2518
  - [ ] F.1. Changes for Both Client and Server Implementations
  - [ ] F.2. Changes for Server Implementations
  - [ ] F.3. Other Changes
