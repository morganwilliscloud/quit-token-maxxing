---
name: api-design
description: Design and review REST APIs following best practices
allowed-tools: file_read file_write
---

# API Design

## Principles
1. Use nouns for resources, not verbs
2. Use HTTP methods correctly (GET=read, POST=create, PUT=replace, PATCH=update, DELETE=remove)
3. Version your API in the URL path (/v1/...)
4. Use consistent pagination (cursor-based for large datasets)
5. Return appropriate HTTP status codes

## Request/Response Conventions
- Use camelCase for JSON fields
- Include a top-level `data` wrapper for collections
- Include pagination metadata in responses
- Use ISO 8601 for dates

## Error Format
```json
{
    "error": {
        "code": "RESOURCE_NOT_FOUND",
        "message": "Human readable message",
        "details": []
    }
}
```
