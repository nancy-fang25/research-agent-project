# Retrieval Evaluation Report

## Goal
This report compares keyword-based retrieval and semantic chunk-level retrieval on a small benchmark of representative queries.

## Metrics
- **Top-1 Hit**: whether the first retrieved document is correct
- **Top-3 Hit**: whether any of the top-3 retrieved documents is correct
- **Correct Doc Rank**: the rank position of the first correct document

## Summary

- Total queries: 7
- Keyword Top-1 Hit Rate: 7/7 (100.00%)
- Keyword Top-3 Hit Rate: 7/7 (100.00%)
- Vector Top-1 Hit Rate: 7/7 (100.00%)
- Vector Top-3 Hit Rate: 7/7 (100.00%)
- Keyword Errors: 0
- Vector Errors: 0
- Avg Keyword Correct Rank: 1.00
- Avg Vector Correct Rank: 1.00

## Query 1
**Query:** Compare methods that improve language model performance using retrieval versus additional task-specific training.
**Expected Docs:** paper1.txt, paper2.txt

### Keyword
- Retrieved Docs: paper1.txt, paper2.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper1.txt | score=9 | matched_terms=additional, improve, language, model, retrieval, using
  - paper2.txt | score=6 | matched_terms=language, model, performance, task-specific

### Vector
- Retrieved Docs: paper2.txt, paper1.txt, paper3.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper2.txt | chunk=0 | similarity=0.6382
  - paper1.txt | chunk=0 | similarity=0.543
  - paper3.txt | chunk=0 | similarity=0.1178

## Query 2
**Query:** Which approach involves autonomous systems that break problems into steps and call outside functions?
**Expected Docs:** paper3.txt

### Keyword
- Retrieved Docs: paper3.txt, paper1.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper3.txt | score=5 | matched_terms=autonomous, systems
  - paper1.txt | score=3 | matched_terms=approach, systems

### Vector
- Retrieved Docs: paper3.txt, paper1.txt, paper2.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper3.txt | chunk=0 | similarity=0.4461
  - paper1.txt | chunk=1 | similarity=0.1378
  - paper2.txt | chunk=0 | similarity=0.1091

## Query 3
**Query:** Which method enhances generation by leveraging information retrieved at runtime rather than relying only on model parameters?
**Expected Docs:** paper1.txt

### Keyword
- Retrieved Docs: paper1.txt, paper2.txt, paper3.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper1.txt | score=7 | matched_terms=generation, method, model, retrieved
  - paper2.txt | score=4 | matched_terms=method, model
  - paper3.txt | score=2 | matched_terms=method, than

### Vector
- Retrieved Docs: paper1.txt, paper2.txt, paper3.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper1.txt | chunk=0 | similarity=0.4314
  - paper2.txt | chunk=0 | similarity=0.3108
  - paper3.txt | chunk=0 | similarity=0.2428

## Query 4
**Query:** Which approach specializes a pretrained model for a narrow domain by continuing training on targeted data?
**Expected Docs:** paper2.txt

### Keyword
- Retrieved Docs: paper2.txt, paper1.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper2.txt | score=4 | matched_terms=data, model, pretrained
  - paper1.txt | score=2 | matched_terms=approach, model

### Vector
- Retrieved Docs: paper2.txt, paper1.txt, paper3.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper2.txt | chunk=0 | similarity=0.4575
  - paper1.txt | chunk=1 | similarity=0.281
  - paper3.txt | chunk=0 | similarity=0.1768

## Query 5
**Query:** Which paper is about autonomous workflows and sequential decision-making rather than search augmentation or model adaptation?
**Expected Docs:** paper3.txt

### Keyword
- Retrieved Docs: paper3.txt, paper1.txt, paper2.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper3.txt | score=5 | matched_terms=autonomous, paper, than, workflows
  - paper1.txt | score=4 | matched_terms=augmentation, model, paper, search
  - paper2.txt | score=3 | matched_terms=model, paper

### Vector
- Retrieved Docs: paper3.txt, paper1.txt, paper2.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper3.txt | chunk=0 | similarity=0.4051
  - paper1.txt | chunk=1 | similarity=0.3463
  - paper2.txt | chunk=0 | similarity=0.3449

## Query 6
**Query:** Which method improves trustworthiness in generated answers by grounding them in external information?
**Expected Docs:** paper1.txt

### Keyword
- Retrieved Docs: paper1.txt, paper3.txt, paper2.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper1.txt | score=3 | matched_terms=improves, method
  - paper3.txt | score=2 | matched_terms=method, them
  - paper2.txt | score=2 | matched_terms=method

### Vector
- Retrieved Docs: paper1.txt, paper2.txt, paper3.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper1.txt | chunk=0 | similarity=0.3256
  - paper2.txt | chunk=0 | similarity=0.2253
  - paper3.txt | chunk=0 | similarity=0.133

## Query 7
**Query:** Which paper focuses on adapting models for specialized fields like medicine or law?
**Expected Docs:** paper2.txt

### Keyword
- Retrieved Docs: paper2.txt, paper1.txt, paper3.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper2.txt | score=7 | matched_terms=adapting, models, paper, specialized
  - paper1.txt | score=3 | matched_terms=models, paper
  - paper3.txt | score=2 | matched_terms=models, paper

### Vector
- Retrieved Docs: paper2.txt, paper1.txt, paper3.txt
- Top-1 Hit: Yes
- Top-3 Hit: Yes
- Correct Doc Rank: 1
- Top Results Preview:
  - paper2.txt | chunk=0 | similarity=0.4233
  - paper1.txt | chunk=1 | similarity=0.1308
  - paper3.txt | chunk=0 | similarity=0.0954

## Observations

- In this small benchmark, both keyword retrieval and semantic vector retrieval may achieve high hit rates because the dataset contains only a few short documents.
- The limited corpus size makes retrieval relatively easy, so hit-based metrics alone may not fully reveal the difference between lexical matching and semantic matching.
- Even when both methods retrieve the correct document, semantic chunk retrieval can still provide better grounding by returning more focused and query-relevant evidence snippets.
- The added ranking signal helps compare retrieval quality more precisely, since a method may rank the correct document higher even when both methods achieve the same hit rate.
- A larger benchmark with more documents, stronger paraphrased queries, and more distractor content would better highlight the advantage of semantic retrieval.
- This evaluation is intended as a lightweight sanity check and comparison baseline rather than a full-scale retrieval study.