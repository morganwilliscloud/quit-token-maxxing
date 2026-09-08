---
name: database-optimization
description: Optimize database queries, schema design, and connection management
allowed-tools: file_read shell
---

# Database Optimization

## Analysis Steps
1. Check for missing indexes on WHERE/JOIN columns
2. Look for N+1 query patterns
3. Identify opportunities for query batching
4. Evaluate denormalization tradeoffs
5. Check connection pool configuration

## Common Fixes
- Add composite indexes for multi-column queries
- Use EXPLAIN ANALYZE to verify query plans
- Batch inserts/updates where possible
- Consider read replicas for heavy read workloads
- Use connection pooling (PgBouncer, RDS Proxy)

## Output Format
For each recommendation:
- **Problem**: What's slow and why
- **Solution**: Specific change to make
- **Impact**: Expected improvement (order of magnitude)
