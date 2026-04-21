# Digital Twin API - System Design

## Redis Operations: Message Flow Analysis

### Message Flow: 1st Message vs Consecutive Messages

#### Redis Operations Summary

**Redis Call Locations:**
- `redis.get()` → [core/session.py:53](core/session.py#L53)
- `redis.incr()` → [core/session.py:113](core/session.py#L113)
- `redis.expire()` → [core/session.py:117](core/session.py#L117)
- `redis.setex()` → [core/session.py:81](core/session.py#L81)

| Operation | Type | 1st Message<br/>(Any Day) | 2nd+ Messages<br/>(Same Day) | When? | Frequency |
|-----------|------|:---:|:---:|---------|-----------|
| Load conversation | **READ** | ✓ | ✓ | Every message | Per message |
| Increment message counter | **WRITE** | ✓ | ✓ | Every message | Per message |
| Set 24-hour TTL on counter | **WRITE** | ✓ | ✗ | 1st message only | **ONE-TIME per day** |
| Save updated conversation | **WRITE** | ✓ | ✓ | Every message | Per message |
| **TOTAL COMMANDS** | — | **4** | **3** | — | — |
| **TOTAL READS** | — | **1** | **1** | — | — |
| **TOTAL WRITES** | — | **3** | **2** | — | — |

---

## Upstash Redis Free Tier

### Free Tier Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| **Commands/Month** | 500,000 | Billable operations against Redis |
| **Bandwidth** | 50 GB | Total data transfer in/out |
| **Storage** | 256 MB | Maximum database size |

### Capacity Analysis

#### Per User Consumption (Average 3-4 messages/day)

```
1st message:  4 commands
2nd+ message: 3 commands each (avg 3 more messages)

Per user per day: 4 + (3 × 3) = 13 commands
Per user per month (30 days): 13 × 30 = 390 commands
```

#### Maximum Users Supported

```
Free tier capacity: 500,000 commands/month
Commands per user: 390 commands/month

Maximum users: 500,000 ÷ 390 ≈ 1,282 active users/month
```

### Storage Breakdown

```
Per session: ~4 KB (conversation history + metadata)
Available storage: 256 MB

Sessions that can fit: 256 MB ÷ 4 KB ≈ 65,536 sessions
```

### Bandwidth Usage

```
Average per request: ~8-10 KB
Available bandwidth: 50 GB = 51,200 MB

Messages supported: 51,200 MB ÷ 8 KB ≈ 6.4M messages/month
(Limited by commands first, not bandwidth)
```

### Upgrade Plans

| Plan | Commands/Month | Price | Best For |
|------|----------------|-------|----------|
| Free | 500,000 | Free | Development, small projects |
| Pro | 10,000,000 | ~$20/month | Growing apps (2,500-10k users) |
| Business | 100,000,000 | ~$200/month | Large scale (10k+ users) |
