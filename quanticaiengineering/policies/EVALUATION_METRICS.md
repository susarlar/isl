# Evaluation Metrics for Policy Document AI Application
**Document Type:** Technical Specification  
**Version:** 1.0  
**Date:** February 22, 2026  
**Owner:** AI Engineering Team

---

## Table of Contents
1. [Application Overview](#application-overview)
2. [Information Quality Metrics](#information-quality-metrics)
3. [System Performance Metrics](#system-performance-metrics)
4. [User Experience Metrics](#user-experience-metrics)
5. [Business Impact Metrics](#business-impact-metrics)
6. [Testing and Evaluation Framework](#testing-and-evaluation-framework)
7. [Continuous Monitoring](#continuous-monitoring)

---

## Application Overview

### Purpose
This document defines success metrics for an AI-powered policy document retrieval and question-answering system built on the Quantic AI Engineering policy corpus. The application enables employees to quickly find accurate policy information through natural language queries.

### Use Cases
- Employees asking policy questions ("How much PTO do I get?")
- HR support automation
- Manager policy lookups
- New hire onboarding assistance
- Compliance verification

### Target SLAs
- **Availability:** 99.9% uptime
- **Response Time:** <3 seconds for 95th percentile
- **Accuracy:** >90% for information quality metrics

---

## Information Quality Metrics

### 1. Groundedness / Faithfulness
**Definition:** Percentage of generated responses that are fully supported by the retrieved source documents without hallucination or fabrication.

**Measurement Method:**
- Human evaluation on sample queries (n=200)
- Automated fact-checking against source documents
- Binary classification: Grounded (1) or Hallucinated (0)

**Calculation:**
```
Groundedness = (Number of Fully Grounded Responses / Total Responses) × 100%
```

**Target:** ≥95% groundedness
**Threshold:** <90% triggers investigation and model review

**Example Evaluation:**
- ✓ **Grounded:** "Employees accrue 20 days of PTO annually in their first 2 years (from [employee_handbook.md](employee_handbook.md#L134))."
- ✗ **Hallucinated:** "Employees get unlimited PTO" (not supported by source)

---

### 2. Citation Accuracy
**Definition:** Percentage of responses where citations correctly identify the source document, section, and relevant content.

**Measurement Method:**
- Verify each citation links to correct document
- Confirm cited content actually supports the claim
- Check citation formatting and completeness

**Components:**
- **Document Accuracy:** Citation points to correct policy document (100% required)
- **Section Accuracy:** Citation includes correct section/heading (95% target)
- **Content Relevance:** Cited passage supports the stated claim (98% target)

**Calculation:**
```
Citation Accuracy = (Correct Citations / Total Citations Provided) × 100%
```

**Target:** ≥98% citation accuracy
**Threshold:** <95% requires immediate attention

**Validation Criteria:**
- [ ] Citation includes document name
- [ ] Citation includes section or line reference
- [ ] Cited text contains information stated in response
- [ ] Citation is accessible (link works)
- [ ] No broken or invalid citations

---

### 3. Answer Relevance
**Definition:** Degree to which the response directly addresses the user's question without extraneous information.

**Measurement Method:**
- Human rating on 5-point Likert scale
- Scale: 1=Irrelevant, 2=Partially relevant, 3=Mostly relevant, 4=Highly relevant, 5=Perfectly relevant
- Sample size: 100 queries per evaluation cycle

**Calculation:**
```
Average Relevance Score = Σ(Individual Ratings) / Number of Queries
```

**Target:** Average score ≥4.2/5.0
**Threshold:** <3.5/5.0 requires intervention

**Scoring Rubric:**
- **5 - Perfect:** Directly answers question, appropriate detail level, no irrelevant info
- **4 - High:** Answers question with minor tangential information
- **3 - Moderate:** Answers question but includes significant irrelevant content
- **2 - Low:** Partially addresses question, mostly irrelevant content
- **1 - None:** Does not address the question

---

### 4. Completeness
**Definition:** Percentage of responses that include all necessary information to fully answer the question.

**Measurement Method:**
- Human evaluation: Does response contain all required information?
- Binary: Complete (1) or Incomplete (0)
- Cross-reference with source documents to identify missing information

**Calculation:**
```
Completeness = (Complete Responses / Total Responses) × 100%
```

**Target:** ≥92% completeness
**Threshold:** <85% requires model tuning

**Example Evaluation:**
Query: "What's the parental leave policy?"
- ✓ **Complete:** Includes eligibility, duration (10-16 weeks), pay (100%), time frame (within 12 months), and how to request
- ✗ **Incomplete:** Only mentions "10 weeks paid leave" without eligibility or request process

---

### 5. Factual Accuracy
**Definition:** Percentage of factual claims in responses that are correct according to source documents.

**Measurement Method:**
- Extract all factual claims from response
- Verify each claim against source documents
- Calculate percentage of accurate claims

**Calculation:**
```
Factual Accuracy = (Correct Facts / Total Facts Stated) × 100%
```

**Target:** ≥98% factual accuracy
**Threshold:** <95% is unacceptable

**Common Error Types to Track:**
- Incorrect numbers (dates, amounts, percentages)
- Misattributed policies
- Outdated information
- Conflation of different policies

---

### 6. Retrieval Precision
**Definition:** Percentage of retrieved documents that are relevant to the query.

**Measurement Method:**
- Review top-k retrieved documents (typically k=5)
- Rate each as Relevant (1) or Not Relevant (0)
- Human evaluation on sample queries

**Calculation:**
```
Precision@k = (Relevant Docs in Top-k / k) × 100%
```

**Target:** ≥85% Precision@5
**Threshold:** <70% indicates retrieval issues

---

### 7. Retrieval Recall
**Definition:** Percentage of all relevant documents that were successfully retrieved.

**Measurement Method:**
- Identify all documents containing answer to query
- Determine how many were retrieved in top-k results
- Requires gold standard relevance judgments

**Calculation:**
```
Recall@k = (Relevant Docs Retrieved / Total Relevant Docs) × 100%
```

**Target:** ≥80% Recall@10
**Threshold:** <65% indicates insufficient retrieval depth

---

### 8. Answer Consistency
**Definition:** Percentage of identical queries that receive semantically equivalent answers across multiple requests.

**Measurement Method:**
- Submit same query multiple times (10 repetitions)
- Compare responses for semantic equivalence
- Allow for minor phrasing variations

**Calculation:**
```
Consistency = (Semantically Equivalent Responses / Total Repeated Queries) × 100%
```

**Target:** ≥95% consistency
**Threshold:** <85% indicates instability

---

## System Performance Metrics

### 1. Query Latency (P95)
**Definition:** Time from query submission to complete response delivery for 95th percentile of requests.

**Measurement Method:**
- Instrument API endpoints with timing
- Track end-to-end latency
- Calculate P50, P90, P95, P99 percentiles

**Components:**
- **Retrieval Time:** Document search and ranking
- **LLM Inference Time:** Response generation
- **Post-processing Time:** Citation formatting, etc.
- **Network Time:** API request/response overhead

**Target:** <3 seconds (P95)
**Threshold:** >5 seconds requires optimization

**Breakdown Targets:**
- Retrieval: <500ms (P95)
- LLM Inference: <2000ms (P95)
- Post-processing: <300ms (P95)
- Network: <200ms (P95)

---

### 2. Throughput
**Definition:** Number of queries the system can handle per second while maintaining quality standards.

**Measurement Method:**
- Load testing with realistic query patterns
- Measure queries per second (QPS) at various load levels
- Identify breaking point where latency or accuracy degrades

**Calculation:**
```
Throughput = Successful Queries Processed / Time Period (seconds)
```

**Target:** ≥50 QPS with <3s latency
**Threshold:** <20 QPS indicates scaling issues

**Load Testing Scenarios:**
- Light load: 10 QPS
- Normal load: 30 QPS
- Peak load: 50 QPS
- Stress test: 100 QPS

---

### 3. Token Efficiency
**Definition:** Average number of tokens (input + output) consumed per query.

**Measurement Method:**
- Track tokens for each query
- Monitor both prompt tokens and completion tokens
- Calculate cost per query

**Calculation:**
```
Average Tokens per Query = (Total Tokens / Total Queries)
Cost per Query = (Total Tokens × Token Price) / Total Queries
```

**Target:** <5,000 tokens per query average
**Threshold:** >8,000 tokens indicates inefficiency

**Optimization Opportunities:**
- Reduce retrieved context size
- Optimize prompt templates
- Implement response length limits
- Use smaller models for simple queries

---

### 4. Cache Hit Rate
**Definition:** Percentage of queries served from cache without requiring LLM inference.

**Measurement Method:**
- Track cache lookups vs. cache misses
- Implement semantic similarity for cache matching
- Monitor cache effectiveness

**Calculation:**
```
Cache Hit Rate = (Cache Hits / Total Queries) × 100%
```

**Target:** ≥30% cache hit rate
**Threshold:** <15% suggests cache strategy review

**Cache Strategy:**
- Exact match: 24-hour TTL
- Semantic similarity (>0.95): 6-hour TTL
- Track most common queries for optimization

---

### 5. Error Rate
**Definition:** Percentage of queries that result in errors or failures.

**Measurement Method:**
- Track all error types
- Categorize by severity and cause
- Monitor error patterns

**Types of Errors:**
- **5xx Server Errors:** System failures
- **4xx Client Errors:** Invalid requests
- **Timeout Errors:** Query exceeded time limit
- **LLM Errors:** Model inference failures
- **Retrieval Errors:** Document search failures

**Calculation:**
```
Error Rate = (Failed Queries / Total Queries) × 100%
```

**Target:** <0.5% error rate
**Threshold:** >2% requires immediate investigation

---

### 6. Uptime / Availability
**Definition:** Percentage of time the system is available and functioning correctly.

**Measurement Method:**
- Monitor service health checks
- Track downtime incidents
- Calculate availability over rolling 30-day window

**Calculation:**
```
Uptime = ((Total Time - Downtime) / Total Time) × 100%
```

**Target:** ≥99.9% uptime (43 minutes downtime/month)
**Threshold:** <99.5% violates SLA

---

### 7. Resource Utilization
**Definition:** Percentage of system resources (CPU, memory, GPU) being used during operation.

**Metrics:**
- **CPU Utilization:** <70% average, <90% peak
- **Memory Utilization:** <80% average, <95% peak
- **GPU Utilization:** <75% average (for LLM inference)
- **Disk I/O:** Monitor for bottlenecks

**Target:** Balanced utilization without bottlenecks
**Threshold:** >85% sustained utilization indicates need for scaling

---

## User Experience Metrics

### 1. User Satisfaction (CSAT)
**Definition:** User rating of satisfaction with the system's response.

**Measurement Method:**
- Post-response feedback: "Was this helpful?" (thumbs up/down)
- Optional follow-up: 5-star rating + feedback
- Track percentage of positive ratings

**Calculation:**
```
CSAT = (Positive Ratings / Total Ratings) × 100%
```

**Target:** ≥85% positive rating
**Threshold:** <75% indicates quality issues

**Feedback Collection:**
- In-app thumbs up/down after each response
- Optional detailed feedback form
- Periodic user surveys (quarterly)

---

### 2. Clarification Rate
**Definition:** Percentage of queries requiring follow-up clarification.

**Measurement Method:**
- Track queries where system asks for clarification
- Track user follow-up questions on same topic
- Identify ambiguous or unclear initial queries

**Calculation:**
```
Clarification Rate = (Queries Requiring Clarification / Total Queries) × 100%
```

**Target:** <15% clarification rate
**Threshold:** >25% suggests prompt engineering issues

---

### 3. Abandonment Rate
**Definition:** Percentage of users who abandon interaction before receiving full response.

**Measurement Method:**
- Track sessions where user closes/navigates away
- Monitor incomplete query flows
- Identify drop-off points

**Calculation:**
```
Abandonment Rate = (Abandoned Sessions / Total Sessions) × 100%
```

**Target:** <5% abandonment rate
**Threshold:** >10% indicates UX problems

---

### 4. Query Reformulation Rate
**Definition:** Percentage of users who reformulate their query after receiving initial response.

**Measurement Method:**
- Track sequential queries on same topic within session
- Identify patterns of dissatisfaction
- Distinguish between exploration vs. dissatisfaction

**Calculation:**
```
Reformulation Rate = (Reformulated Queries / Total Queries) × 100%
```

**Target:** <20% reformulation rate
**Threshold:** >35% suggests poor initial response quality

---

### 5. Time to Resolution
**Definition:** Average time from initial query to user's issue being resolved.

**Measurement Method:**
- Track from first query to last query in session
- User feedback: "Did this resolve your question?"
- Compare to traditional support channels

**Calculation:**
```
Avg Time to Resolution = Total Resolution Time / Number of Resolved Sessions
```

**Target:** <2 minutes average
**Threshold:** >5 minutes indicates inefficiency

---

## Business Impact Metrics

### 1. HR Support Ticket Deflection
**Definition:** Percentage reduction in HR support tickets due to self-service through AI application.

**Measurement Method:**
- Compare ticket volume before/after deployment
- Track queries successfully resolved without ticket
- Category-specific deflection rates

**Calculation:**
```
Deflection Rate = ((Baseline Tickets - Current Tickets) / Baseline Tickets) × 100%
```

**Target:** ≥40% ticket deflection
**ROI Calculation:** Tickets Deflected × Average Ticket Cost ($25) = Monthly Savings

---

### 2. Cost per Query
**Definition:** Total operational cost divided by number of queries served.

**Cost Components:**
- LLM API costs (tokens consumed)
- Infrastructure costs (compute, storage)
- Monitoring and logging
- Maintenance and support

**Calculation:**
```
Cost per Query = Total Monthly Costs / Total Monthly Queries
```

**Target:** <$0.05 per query
**Benchmark:** Compare to average HR support ticket cost ($25)

---

### 3. User Adoption Rate
**Definition:** Percentage of employees who have used the system at least once.

**Measurement Method:**
- Track unique users
- Monitor adoption over time
- Segment by department/role

**Calculation:**
```
Adoption Rate = (Active Users / Total Employees) × 100%
```

**Target:** ≥60% adoption within 6 months
**Milestones:**
- 1 month: 20%
- 3 months: 40%
- 6 months: 60%

---

### 4. Engagement Rate
**Definition:** Percentage of active users who use system regularly (weekly or more).

**Calculation:**
```
Engagement Rate = (Weekly Active Users / Total Active Users) × 100%
```

**Target:** ≥30% weekly engagement
**Power User Metric:** ≥5% use system daily

---

### 5. Policy Compliance Improvement
**Definition:** Measured improvement in policy compliance through better policy awareness.

**Measurement Method:**
- Track policy violation incidents before/after
- Survey employees on policy awareness
- Monitor policy quiz/certification scores

**Target:** 20% reduction in policy violations within 1 year

---

## Testing and Evaluation Framework

### Test Dataset Creation

**Gold Standard Dataset:**
- **Size:** 500 curated query-answer pairs
- **Distribution:**
  - Common questions: 60% (frequently asked)
  - Edge cases: 25% (complex or ambiguous)
  - Multi-hop: 10% (requires multiple docs)
  - Out-of-scope: 5% (cannot be answered from corpus)

**Query Categories:**
- PTO and leave questions (20%)
- Security and IT policies (20%)
- Remote work and equipment (15%)
- Professional development (10%)
- Expense reimbursement (10%)
- Safety and compliance (10%)
- General employment questions (15%)

---

### Evaluation Cycles

**Weekly:**
- Automated testing on gold standard dataset
- Latency and error rate monitoring
- Cache hit rate analysis

**Monthly:**
- Human evaluation of 200 random queries
- User satisfaction analysis
- Cost and ROI review

**Quarterly:**
- Comprehensive evaluation across all metrics
- User surveys and interviews
- A/B testing of improvements
- Executive reporting

---

### A/B Testing Framework

**Experimental Setup:**
- Control group: Current production system
- Treatment group: New model/prompt/retrieval strategy
- Traffic split: 90/10 or 80/20
- Minimum sample size: 1,000 queries per variant

**Success Criteria:**
- Statistical significance: p < 0.05
- Minimum improvement thresholds:
  - Groundedness: +2%
  - Latency: -10%
  - User satisfaction: +5%
- No degradation in other key metrics

---

### Human Evaluation Protocol

**Evaluator Training:**
- Complete training on evaluation criteria
- Calibration exercises (achieve >85% inter-rater agreement)
- Regular refresher sessions

**Evaluation Process:**
1. Evaluator reviews query and response
2. Rates each metric independently
3. Provides written justification for low scores
4. Flags edge cases or interesting examples

**Quality Control:**
- 10% overlap for inter-rater reliability
- Weighted Cohen's kappa >0.75 required
- Monthly calibration sessions

---

## Continuous Monitoring

### Real-Time Dashboards

**Executive Dashboard:**
- Overall system health (green/yellow/red)
- Daily query volume
- User satisfaction trend
- Cost per query
- Key metric summary

**Engineering Dashboard:**
- Latency percentiles (P50, P90, P95, P99)
- Error rates by type
- Cache hit rate
- Resource utilization
- Active incidents

**Quality Dashboard:**
- Groundedness score (weekly average)
- Citation accuracy
- User feedback sentiment
- Low-rated queries for review
- Retrieval performance

---

### Alerting Thresholds

**Critical Alerts (Page immediately):**
- Error rate >5%
- P95 latency >10 seconds
- System downtime >5 minutes
- Groundedness <85%

**Warning Alerts (Email/Slack):**
- Error rate >2%
- P95 latency >5 seconds
- User satisfaction <75%
- Cache hit rate <15%
- Groundedness <90%

**Informational:**
- Daily metric summary
- Weekly trend report
- Monthly evaluation results

---

### Feedback Loop

**User Feedback Collection:**
- In-app thumbs up/down
- Optional comment field
- "Report incorrect information" button
- Quarterly user surveys

**Feedback Processing:**
- Low-rated responses reviewed within 24 hours
- Patterns identified and addressed
- Feedback incorporated into training data
- Users notified of improvements

**Continuous Improvement:**
- Weekly review of flagged responses
- Monthly prompt engineering updates
- Quarterly model fine-tuning evaluation
- Biannual major system updates

---

## Success Criteria Summary

### Minimum Viable Product (MVP)
- ✓ Groundedness ≥90%
- ✓ Citation accuracy ≥95%
- ✓ P95 latency <5 seconds
- ✓ Error rate <2%
- ✓ User satisfaction ≥75%

### Production Launch
- ✓ Groundedness ≥95%
- ✓ Citation accuracy ≥98%
- ✓ P95 latency <3 seconds
- ✓ Error rate <0.5%
- ✓ User satisfaction ≥85%
- ✓ 99.9% uptime
- ✓ Cost per query <$0.05

### Excellence Targets (6-12 months)
- ✓ Groundedness ≥98%
- ✓ Citation accuracy ≥99%
- ✓ P95 latency <2 seconds
- ✓ User satisfaction ≥90%
- ✓ 60% user adoption
- ✓ 40% ticket deflection
- ✓ Positive ROI

---

## Appendix

### Metric Calculation Examples

**Example 1: Groundedness Evaluation**

Query: "How much PTO do new employees get?"

Response: "New employees at Quantic AI Engineering receive 20 days (160 hours) of PTO annually during their first two years of employment. This accrues at 6.15 hours per bi-weekly pay period."

Source Check:
- ✓ "20 days (160 hours)" - Verified in employee_handbook.md, Leave section
- ✓ "first two years" - Verified in leave_and_time_off.md
- ✓ "6.15 hours per bi-weekly" - Verified in accrual table

**Result: Grounded (1)**

---

**Example 2: Citation Accuracy Evaluation**

Response with Citations:
"Remote employees receive a monthly stipend of $75 for internet/phone expenses [remote_work_policy.md#equipment-and-technology], and full-time remote employees also receive a one-time $500 home office setup allowance [remote_work_policy.md#home-office-stipend]."

Citation Validation:
- ✓ Citation 1: Correct document, correct section, accurate amount
- ✓ Citation 2: Correct document, correct section, accurate amount

**Result: 100% citation accuracy (2/2)**

---

### Glossary

**Groundedness:** Responses fully supported by source documents without fabrication  
**Hallucination:** LLM-generated content not supported by source documents  
**Retrieval:** Process of finding relevant documents for a query  
**Precision@k:** Proportion of top-k retrieved documents that are relevant  
**Recall@k:** Proportion of all relevant documents found in top-k results  
**P95 Latency:** 95th percentile response time (95% of requests faster than this)  
**CSAT:** Customer Satisfaction Score  
**QPS:** Queries Per Second  
**TTL:** Time To Live (cache duration)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-22 | AI Engineering Team | Initial metrics framework |

---

**Document Classification:** Internal Use Only  
**Next Review Date:** May 22, 2026

*For questions about these metrics or to propose additional metrics, contact the AI Engineering Team at ai-engineering@quanticai.com*
