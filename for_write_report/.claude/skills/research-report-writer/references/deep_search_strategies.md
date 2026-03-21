# Deep Search Strategies

This guide defines when and how to conduct deep, comprehensive searches using multiple MCP servers and the Task tool.

## Table of Contents

1. [When to Use Deep Search](#when-to-use-deep-search)
2. [Deep Search vs. Basic Search](#deep-search-vs-basic-search)
3. [Multi-MCP Integration Strategies](#multi-mcp-integration-strategies)
4. [Task Tool for Comprehensive Searches](#task-tool-for-comprehensive-searches)
5. [Ensuring Information Completeness](#ensuring-information-completeness)
6. [Deep Search Workflows](#deep-search-workflows)

---

## When to Use Deep Search

### Criteria for Deep Search

Use deep search when ANY of these conditions apply:

1. **High Detail Level Requested**
   - User requests detail level 4-5 for report structure
   - Chapter page estimate >10 pages
   - Topic is core to the research (e.g., main analysis chapters)

2. **Complex or Multi-Faceted Topics**
   - Topic spans multiple domains (e.g., theory + implementation + evaluation)
   - Requires integration of different data types
   - Multiple perspectives needed (e.g., methodology + performance + applications)

3. **Comprehensive Coverage Required**
   - User explicitly asks for "comprehensive", "exhaustive", or "thorough" analysis
   - Literature review section
   - State-of-the-art assessment

4. **Critical Decision Points**
   - Recommendations chapter
   - Strategic analysis
   - Comparative evaluation of options

5. **Data-Intensive Sections**
   - Requires quantitative analysis of many data points
   - Systematic comparison across multiple sources
   - Meta-analysis type synthesis

6. **Uncertain Information Landscape**
   - Don't know how much literature exists
   - Need to explore topic boundaries
   - Discovering unexpected connections

### When Basic Search is Sufficient

Use basic search when:

- **Background sections**: General context, well-established facts
- **Low detail level**: User requests detail level 1-2
- **Short chapters**: <5 pages
- **Well-defined narrow topics**: Single specific question
- **Time constraints**: Quick turnaround needed

---

## Deep Search vs. Basic Search

### Basic Search

**Characteristics**:
- 1-2 MCP servers
- 10-20 references total
- Direct queries with known keywords
- 15-30 minutes search time
- Focused on high-quality core papers

**Example workflow**:
```
1. Google Scholar: "transformer architecture optimization" → 15 papers
2. Filter: Reviews, last 5 years
3. Select top 10 most cited
Total: 10 references, 20 minutes
```

**Appropriate for**:
- Introduction/background
- Well-established concepts
- Supplementary information

---

### Deep Search

**Characteristics**:
- 3-5+ MCP servers
- 50-100+ references
- Multiple query variations and strategies
- 1-4 hours search time (mostly automated with Task tool)
- Comprehensive coverage including edge cases

**Example workflow**:
```
1. Task tool (Explore agent): Comprehensive Scholar + ArXiv + OpenAlex
   - Multiple keyword combinations
   - Discovers 60 papers

2. GitHub/Repository search: 20 code implementations
3. Technical documentation: 15 specification documents
4. Patent search: 25 patents
5. Cross-reference and synthesize

Total: 120+ sources, 2-3 hours (mostly automated)
```

**Appropriate for**:
- Core analysis chapters
- Literature reviews
- Comparative analyses
- Strategic recommendations

---

## Multi-MCP Integration Strategies

### Strategy 1: Sequential Deepening

**Approach**: Start broad, progressively narrow and deepen

**Steps**:
1. **Initial sweep**: Google Scholar for breadth (30-40 papers)
2. **Focused search**: Domain-specific database for peer-reviewed depth (20-30 papers)
3. **Latest findings**: ArXiv or preprint servers for recent work (10-15 papers)
4. **Full-text analysis**: paperclip for detailed reading of key papers

**When to use**: Literature review, comprehensive topic coverage

**Example**:
```
Topic: Neural architecture search optimization

Step 1 (Google Scholar): "neural architecture search" → 35 papers (broad)
Step 2 (ArXiv): cat:cs.LG "NAS optimization" → 25 papers (focused)
Step 3 (GitHub): NAS implementation repositories → 12 implementations
Step 4 (paperclip): Analyze full PDFs of 10 most important papers

Total: 70+ sources with deep analysis of key papers
```

---

### Strategy 2: Parallel Multi-Source

**Approach**: Query multiple MCPs simultaneously with different focuses

**Steps**:
1. **Literature** (Google Scholar + ArXiv): Theoretical studies
2. **Data** (Dataset repositories + APIs): Quantitative data
3. **Implementation** (GitHub + Documentation): Practical approaches
4. **Integration**: Synthesize across data types

**When to use**: Multi-faceted analysis requiring different data types

**Example**:
```
Topic: Time series forecasting methods

Parallel searches:
- Google Scholar: "time series forecasting" → 30 papers (theory)
- ArXiv: cat:stat.ML "forecasting methods" → 25 papers (recent)
- GitHub: Forecasting libraries and implementations → 20 repositories
- Kaggle: Forecasting competition datasets → 15 datasets

Synthesis: Integrate theoretical foundations + implementations + benchmark results
Total: 90 sources across 4 dimensions
```

---

### Strategy 3: Iterative Refinement

**Approach**: Use initial results to refine subsequent searches

**Steps**:
1. **Exploratory search**: Broad initial query
2. **Analyze results**: Identify key terms, authors, subtopics
3. **Refined search**: Use discovered terms for focused queries
4. **Targeted search**: Deep dive into specific subtopics
5. **Validation**: Cross-reference findings

**When to use**: Unfamiliar topic, exploratory research

**Example**:
```
Topic: Graph neural networks for recommendation systems

Iteration 1 (Google Scholar): "graph neural network recommendation" → 25 papers
  → Discover: "message passing", "heterogeneous graphs"

Iteration 2 (ArXiv): "message passing recommendation" → 20 papers
  → Discover: Specific architectures (GraphSAGE, GAT)

Iteration 3 (GitHub): GraphSAGE and GAT implementations → 15 repositories
  → Discover: Performance benchmarks, dataset usage

Iteration 4 (Google Scholar): "GraphSAGE recommendation systems" → 10 papers (specific)

Total: 70 sources with progressively refined focus
```

---

### Strategy 4: Cross-Validation

**Approach**: Verify findings across multiple independent sources

**Steps**:
1. **Primary search**: Main MCP for core data
2. **Secondary search**: Alternative MCP for validation
3. **Tertiary search**: Third MCP for completeness
4. **Triangulation**: Confirm consistent findings

**When to use**: Critical findings, controversial topics, high-stakes decisions

**Example**:
```
Claim: "Transformer models outperform RNNs for long-sequence tasks"

Validation across sources:
- Google Scholar: 20 papers reporting superior performance
- ArXiv: 15 recent preprints confirming findings
- GitHub: 10 benchmark repositories with comparative results
- Conference proceedings: 5 papers from top ML conferences

Result: Cross-validated across 50 sources from 4 different MCPs
```

---

## Task Tool for Comprehensive Searches

### When to Use Task Tool

Use Task tool (subagent_type=Explore) when:

1. **Need 50+ sources**: Basic searches insufficient
2. **Multiple search queries needed**: Complex boolean combinations
3. **Cross-MCP synthesis**: Integrate results from 3+ MCPs
4. **Uncertain search space**: Don't know all relevant keywords
5. **Time efficiency**: Automate a 2-4 hour manual search

### Task Tool Invocation Pattern

```markdown
Use Task tool with these parameters:

subagent_type: Explore
thoroughness: "very thorough" (for deep search)
prompt: "
  Comprehensively search for [TOPIC] using the following MCP servers:

  1. Google Scholar: Search for peer-reviewed papers on [specific aspect]
     - Use keywords: [keyword list]
     - Filters: Last 10 years, highly cited papers
     - Target: 30-40 papers

  2. ArXiv: Search for recent research on [specific aspect]
     - Use keywords: [keyword list]
     - Categories: [relevant categories]
     - Target: 20-30 papers

  3. Domain-specific database: [specific aspect]
     - Use keywords: [keyword list]
     - Target: 10-15 sources

  4. [Additional MCPs as needed]: [Specific goals]

  Requirements:
  - Find at least 60 total sources
  - Cover [list key subtopics]
  - Include both theoretical and empirical perspectives
  - Organize results by subtopic
  - Provide citation information for each source
  - Summarize key findings from each major source
"
```

### Example Task Tool Usage

**Scenario**: Writing Chapter 3 on "Advanced Optimization Algorithms for Deep Learning"

```
Task tool invocation:

subagent_type: Explore
thoroughness: very thorough
prompt: "
  Comprehensively research advanced optimization algorithms for deep learning
  using multiple MCP servers. This is for a detailed research report chapter.

  Search Strategy:

  1. Google Scholar (target: 30-40 papers):
     - "Adam optimizer" variations
     - "adaptive learning rate" methods
     - "second-order optimization" deep learning
     - Filters: Last 10 years, highly cited papers

  2. ArXiv (target: 20-30 papers):
     - cat:cs.LG "optimization algorithm"
     - cat:cs.LG "gradient descent" variations
     - Recent papers (last 3 years)

  3. GitHub (target: 15-20 repositories):
     - PyTorch optimizer implementations
     - TensorFlow optimizer libraries
     - Benchmark comparisons

  4. Conference proceedings (if available):
     - NeurIPS, ICML, ICLR papers on optimization
     - Target: 10-15 papers

  Coverage Requirements:
  - First-order methods (SGD, Adam, AdaGrad, RMSprop)
  - Second-order methods (L-BFGS, natural gradient)
  - Adaptive learning rates
  - Momentum-based methods
  - Convergence analysis
  - Empirical comparisons

  Deliverables:
  - At least 60 total sources
  - Organized by subtopic (method categories)
  - Citation information (authors, title, venue, year, DOI)
  - Key findings summary for top 20 papers
  - Performance comparison tables if available
"
```

**Expected Output**:
- Comprehensive list of 60-80 sources
- Organized by subtopic
- Ready for integration into chapter

---

## Ensuring Information Completeness

### Completeness Checklist

For deep searches, ensure coverage of:

- [ ] **Temporal completeness**: Recent (last 2 years) + established (5-10 years)
- [ ] **Methodological diversity**: Reviews, original research, empirical studies
- [ ] **Perspective diversity**: Theory, implementation, applications
- [ ] **Geographic diversity**: US, Europe, Asia research
- [ ] **Publication tier**: Top conferences/journals + specialized venues
- [ ] **Data types**: Qualitative + quantitative
- [ ] **Conflicting views**: Different approaches and perspectives
- [ ] **Edge cases**: Specialized variants, unusual findings

### Coverage Gaps to Avoid

**Common gaps**:
1. **Recency bias**: Only recent papers, missing foundational work
2. **Citation bias**: Only highly-cited papers, missing recent important work
3. **Venue bias**: Only top-tier venues, missing specialized insights
4. **Language bias**: Only English, missing key international research
5. **Methodology bias**: Only one study type (e.g., only theory, no empirical)

**Mitigation strategies**:
- Explicitly search different time periods
- Use multiple MCPs (different indexing)
- Include preprints (ArXiv) for cutting-edge work
- Search specialized databases for domain-specific content
- Use Task tool to systematically cover gaps

---

## Deep Search Workflows

### Workflow 1: Comprehensive Literature Review

**Goal**: Exhaustive coverage of a topic

**Time**: 2-3 hours (mostly automated)

**Steps**:
1. **Define scope**: Subtopics, date range, inclusion criteria
2. **Launch Task tool**: Explore agent with detailed prompt
3. **Parallel manual queries**: While Task runs, do targeted repository/dataset searches
4. **Integrate results**: Combine Task output + manual searches
5. **Organize**: Group by subtopic, identify key papers
6. **Synthesize**: Extract main themes, controversies, gaps

**Output**: 80-100+ sources, organized and synthesized

---

### Workflow 2: Multi-Dimensional Analysis

**Goal**: Integrate different data types (literature + data + implementation)

**Time**: 3-4 hours

**Steps**:
1. **Dimension 1 - Literature** (Task tool): 40-50 papers
2. **Dimension 2 - Empirical Data** (Dataset repositories): 15-20 datasets
3. **Dimension 3 - Implementations** (GitHub): 20-30 repositories
4. **Dimension 4 - Industry/Market** (Reports + company data): 20-30 sources
5. **Integration**: Create unified view across dimensions
6. **Analysis**: Identify patterns, gaps, opportunities

**Output**: 100-150 sources across 4 data dimensions

---

### Workflow 3: Focused Deep Dive

**Goal**: Extremely detailed analysis of a specific narrow topic

**Time**: 2-3 hours

**Steps**:
1. **Core papers** (Google Scholar + ArXiv): 20-30 definitive papers
2. **Full-text analysis** (paperclip): Deep read of all core papers
3. **Cited references**: Chase citations backward (another 20-30 papers)
4. **Citing papers**: Chase citations forward (another 10-20 papers)
5. **Recent updates** (ArXiv/preprints): Latest 5-10 papers
6. **Data extraction**: Detailed tables, figures, quantitative synthesis

**Output**: 60-80 sources with deep analysis and data extraction

---

## Efficiency Tips for Deep Searches

### Automation

1. **Use Task tool liberally**: Let it handle repetitive searches
2. **Parallel processing**: Run Task tool while doing manual queries
3. **Batch queries**: Group similar searches together

### Organization

1. **Tag as you go**: Mark sources by subtopic during search
2. **Priority flagging**: Mark must-read vs. supporting papers
3. **Data extraction during search**: Collect key data immediately

### Quality over Quantity

1. **Set minimum threshold**: E.g., "top 50% by citation count"
2. **Diversify**: Ensure multiple methodologies, not just more of the same
3. **Diminishing returns**: Stop when new sources add little new information

---

## Deep Search Documentation Template

For each deep search, document:

```markdown
## Search Strategy for [Chapter/Section Name]

**Search Date**: [Date]

**Objective**: [What information was needed]

**MCPs Used**:
- Google Scholar: [queries, filters, results count]
- ArXiv: [queries, categories, results count]
- Domain-specific database: [queries, results count]
- [Other MCPs]: [details]

**Task Tool Usage**: [Yes/No, if yes, describe prompt and thoroughness level]

**Results**:
- Total sources found: [N]
- Sources selected: [M]
- Organization: [By subtopic/date/methodology]

**Key Findings**:
- [Major theme 1]: [M] papers
- [Major theme 2]: [N] papers
- [Emerging area]: [K] papers

**Gaps Identified**:
- [Gap 1]: Limited data on [topic]
- [Gap 2]: No recent studies on [topic]

**Quality Assessment**:
- High-impact venues: [N] papers
- Recent (<2 years): [M] papers
- Empirical studies: [K] papers
- Reviews/surveys: [L] papers
```

---

## Conclusion

Deep search strategies are essential for producing high-quality, comprehensive research reports. The key is matching search depth to chapter importance and detail requirements, using Task tool for automation, and ensuring multi-dimensional coverage through strategic MCP selection.

**Decision Framework**:
- Detail level 1-2 → Basic search
- Detail level 3 → Medium search (30-40 sources)
- Detail level 4-5 → Deep search (60-100+ sources, Task tool)
- Core analysis chapters → Always deep search
- Background/intro → Basic to medium search
