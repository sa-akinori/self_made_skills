# MCP Server Selection Guide

This guide helps select the appropriate MCP servers for data collection based on chapter topics and research needs across all disciplines.

## Available MCP Servers

Common MCP servers for research (availability depends on installation):

1. **Google-Scholar-MCP-Server** - Academic papers across all disciplines
2. **paperclip** - ArXiv, OpenAlex, OSF paper search and PDF analysis
3. **firecrawl-mcp-server** - Web scraping and content extraction
4. **Domain-specific MCPs** - Varies by field (see installation guide)

**Note**: The specific MCP servers available will depend on what's installed in your project. Use the skill-recommender to find and install domain-specific MCPs based on your research needs.

---

## MCP Selection by Research Domain

### Academic & General Research

**Primary MCPs**:

- **Google Scholar**: Broad academic coverage across all fields
- **paperclip**: ArXiv (physics, CS, math), OpenAlex (multidisciplinary)

**Search Strategy**:

1. Start with Google Scholar for comprehensive academic coverage
2. Use paperclip for ArXiv if your field is covered (physics, CS, math, biology)
3. Use firecrawl for institutional websites, research lab pages

**Query Examples**:

```
Google Scholar: "your research topic" since:2020
ArXiv (paperclip): "algorithm name" OR "methodology"
Web (firecrawl): Research institute URLs, conference proceedings
```

---

### Data Science & Machine Learning

**Primary MCPs**:

- **Google Scholar**: ML papers, algorithms, benchmarks
- **paperclip**: ArXiv CS section, OpenAlex
- **firecrawl**: GitHub repos, documentation, blogs

**Secondary MCPs**:

- **Dataset APIs** (if installed): Kaggle, UCI ML Repository, Hugging Face

**Search Strategy**:

1. Google Scholar for peer-reviewed ML papers
2. ArXiv for latest preprints (cs.LG, cs.CV, cs.AI)
3. firecrawl for implementation details, tutorials, datasets

**Query Examples**:

```
Google Scholar: "transformer architecture" "attention mechanism"
ArXiv: cat:cs.LG "self-supervised learning"
Web: site:github.com "model implementation"
```

---

### Financial & Business Research

**Primary MCPs**:

- **Google Scholar**: Finance literature, economics papers
- **firecrawl**: Financial news, company reports, market data

**Secondary MCPs**:

- **Financial data APIs** (if installed): Market data, economic indicators
- **Patent MCP** (if installed): Business method patents

**Search Strategy**:

1. Google Scholar for academic finance research
2. firecrawl for real-time market analysis, company filings
3. Patent searches for innovation landscape

**Query Examples**:

```
Google Scholar: "portfolio optimization" "risk management"
Web: site:sec.gov "10-K filing" company_name
Patent: "financial technology" "blockchain"
```

---

### Social Sciences & Humanities

**Primary MCPs**:

- **Google Scholar**: Social science journals, humanities papers
- **paperclip**: OpenAlex for multidisciplinary research

**Secondary MCPs**:

- **Survey/Census data APIs** (if installed): Demographics, public records
- **Archive MCPs** (if installed): Historical documents

**Search Strategy**:

1. Google Scholar for peer-reviewed research
2. OpenAlex for interdisciplinary connections
3. firecrawl for institutional data, reports

**Query Examples**:

```
Google Scholar: "social mobility" "education policy"
OpenAlex: author:"researcher name" concepts:"sociology"
Web: site:census.gov "demographic data"
```

---

### Engineering & Technical Research

**Primary MCPs**:

- **Google Scholar**: Engineering papers, technical reports
- **paperclip**: ArXiv physics/engineering sections
- **firecrawl**: Standards documents, technical specifications

**Secondary MCPs**:

- **Patent MCP** (if installed): Technical patents, inventions

**Search Strategy**:

1. Google Scholar for engineering research
2. ArXiv for physics/engineering preprints
3. Patent searches for prior art and innovation trends
4. firecrawl for standards (IEEE, ISO), datasheets

**Query Examples**:

```
Google Scholar: "material properties" "finite element"
ArXiv: cat:physics.app-ph "device fabrication"
Patent: "semiconductor" "manufacturing process"
Web: site:ieee.org "standard specification"
```

---

### Environmental & Earth Sciences

**Primary MCPs**:

- **Google Scholar**: Environmental research, climate papers
- **paperclip**: ArXiv physics section, OpenAlex

**Secondary MCPs**:

- **Climate/Earth data APIs** (if installed): Satellite data, weather, GIS

**Search Strategy**:

1. Google Scholar for environmental literature
2. ArXiv for atmospheric/earth science preprints
3. firecrawl for government reports, environmental data

**Query Examples**:

```
Google Scholar: "climate change" "carbon emissions"
ArXiv: cat:physics.ao-ph "atmospheric modeling"
Web: site:noaa.gov "climate data" OR site:nasa.gov "earth observation"
```

---

### Linguistics & Language Research

**Primary MCPs**:

- **Google Scholar**: Linguistics papers, language studies
- **paperclip**: OpenAlex for interdisciplinary language research

**Secondary MCPs**:

- **Corpus/Language data APIs** (if installed): Text corpora, linguistic databases

**Search Strategy**:

1. Google Scholar for linguistics research
2. OpenAlex for computational linguistics connections
3. firecrawl for language resources, corpora websites

**Query Examples**:

```
Google Scholar: "syntax" "morphology" language_name
OpenAlex: concepts:"natural language processing"
Web: site:linguistic-corpora.org corpus_name
```

---

## General Search Strategies

### Google Scholar Best Practices

**Basic syntax**:

- **Quotes for exact phrases**: "machine learning"
- **OR for alternatives**: algorithm OR method
- **Minus to exclude**: neural -network
- **Year range**: since:2020 OR 2015..2020

**Advanced operators**:

- **Author search**: author:"lastname"
- **Title search**: intitle:"keyword"
- **Source search**: source:"journal name"
- **File type**: filetype:pdf

**Example queries**:

```
"deep learning" "image classification" since:2020
author:"researcher" intitle:"survey"
("method A" OR "method B") evaluation -deprecated
```

### ArXiv Search Tips (via paperclip)

**Categories**:

- cs.LG - Machine Learning
- cs.CV - Computer Vision
- cs.AI - Artificial Intelligence
- physics.* - Physics sections
- math.* - Mathematics sections

**Query format**:

```
cat:cs.LG "transformer"
author:"lastname" cat:cs.AI
"your topic" submittedDate:[2023-01-01 TO 2024-12-31]
```

### Web Scraping Strategy (firecrawl)

**Best for**:

- Institutional websites
- Research lab pages
- Technical documentation
- Conference proceedings
- Government reports
- Company research pages
- Research papers

**Approach**:

1. Identify authoritative sources in your domain
2. Use firecrawl to extract structured content
3. Verify credibility of sources
4. Cross-reference with peer-reviewed literature

---

## Multi-MCP Deep Search Workflows

### Standard Literature Review

**Goal**: Comprehensive understanding of a topic

**Workflow**:

1. **Google Scholar** (30-50 papers): Core peer-reviewed literature
2. **ArXiv/paperclip** (10-20 papers): Latest preprints and working papers
3. **firecrawl** (5-10 sources): Gray literature, reports, documentation

**Total coverage**: 50-80 sources

**Time estimate**: 2-3 hours of searching + analysis

### Quick Topic Overview

**Goal**: Rapid understanding of a topic

**Workflow**:

1. **Google Scholar** (10-15 papers): Key review papers and recent studies
2. **Web search/firecrawl** (3-5 sources): Summary articles, introductory materials

**Total coverage**: 15-20 sources

**Time estimate**: 30-60 minutes

### Comprehensive Domain Analysis

**Goal**: Exhaustive coverage of a research area

**Workflow**:

1. **Google Scholar** (50-100 papers): Systematic literature review
2. **ArXiv/paperclip** (20-30 papers): Preprints and emerging research
3. **Domain-specific APIs** (as available): Specialized databases
4. **firecrawl** (10-20 sources): Technical reports, white papers, documentation
5. **Patent search** (if applicable): Innovation landscape

**Total coverage**: 100-150+ sources

**Time estimate**: 5-10 hours of searching + analysis

---

## Citation Management

### Standard Citation Formats

**Academic papers**:

```
Author A, Author B, Author C. Title of paper. Journal Name. Year;Volume(Issue):Pages.

Example:
Smith J, Johnson A, Williams B. Machine learning advances. Nature. 2024;123(4):456-789.
```

**Preprints**:

```
Author A, Author B. Title of preprint. Preprint server. Year. DOI or URL.

Example:
Zhang X, Li Y. Novel algorithm for optimization. arXiv. 2024. arXiv:2401.12345
```

**Web sources**:

```
Author/Organization. Title. Website Name. Publication Date. URL. [Accessed Date].

Example:
Research Lab. Technical report on methodology. University Website. 2024. https://example.edu/report. [Accessed: 2024-01-15].
```

### Quality Assessment

**Peer-reviewed papers**:

- Journal impact factor
- Citation count
- Author credentials
- Institutional affiliation

**Preprints**:

- Author credentials
- Institutional affiliation
- Clarity and rigor
- Citation of prior work

**Web sources**:

- Source credibility (government, academic, industry)
- Publication date (recency)
- Author expertise
- Cross-reference with peer-reviewed literature

---

## Quick Reference: MCP Selection by Task

**Literature review**:

- Primary: Google Scholar
- Secondary: paperclip (ArXiv, OpenAlex)

**Latest research**:

- Primary: paperclip (ArXiv)
- Secondary: Google Scholar (recent papers)

**Technical documentation**:

- Primary: firecrawl
- Secondary: Google Scholar

**Data collection**:

- Primary: Domain-specific data APIs (if installed)
- Secondary: firecrawl (data repository websites)

**Industry trends**:

- Primary: firecrawl (news, reports)
- Secondary: Google Scholar (market research)

**Historical analysis**:

- Primary: Google Scholar
- Secondary: firecrawl (archives, institutional sites)

---

## Tips for Effective MCP Usage

### Search Query Optimization

1. **Start broad, then narrow**: Begin with general terms, refine based on results
2. **Use domain vocabulary**: Employ technical terms from your field
3. **Combine multiple concepts**: Use AND/OR operators effectively
4. **Filter by date**: Focus on recent research unless historical perspective needed
5. **Iterate based on results**: Adjust queries based on what you find

### Source Diversity

1. **Multiple perspectives**: Don't rely on a single MCP or source type
2. **Geographic diversity**: Include international research when relevant
3. **Methodological variety**: Include theoretical, empirical, and review papers
4. **Time span**: Balance recent advances with foundational work

### Quality Control

1. **Verify claims**: Cross-check important facts across multiple sources
2. **Check citations**: Ensure cited works actually support the claims
3. **Assess methodology**: Evaluate research design and statistical rigor
4. **Consider bias**: Be aware of funding sources and potential conflicts

### Efficiency

1. **Use saved searches**: Record effective query patterns for reuse
2. **Track sources**: Document what you've already searched
3. **Batch processing**: Collect multiple papers before detailed reading
4. **Focus on abstracts first**: Screen relevance before full-text reading

---

## Troubleshooting

### Low result quality

**Problem**: Search returns irrelevant or low-quality results

**Solutions**:

1. Refine search terms using domain-specific vocabulary
2. Add exclusion terms to filter out irrelevant content
3. Use field-specific operators (author, source, date)
4. Try alternative MCPs or search angles

### Missing key research

**Problem**: Known important papers not appearing in results

**Solutions**:

1. Search by author name
2. Search by specific journal/conference
3. Use exact title search
4. Check if topic uses alternative terminology

### Too many results

**Problem**: Overwhelming number of search results

**Solutions**:

1. Add more specific terms to narrow scope
2. Restrict date range to recent years
3. Filter by source (top journals, specific conferences)
4. Use review papers to get curated overview

### MCP not available

**Problem**: Needed MCP server not installed

**Solutions**:

1. Use skill-recommender to find and install appropriate MCPs
2. Use alternative MCPs with broader coverage
3. Use firecrawl to access content directly from web
4. Consider manual searches as fallback

---

## Adapting to Your Research Domain

This guide provides general strategies. For your specific research domain:

1. **Identify key journals/conferences**: Focus searches on top venues in your field
2. **Learn domain terminology**: Use field-specific search terms
3. **Find domain databases**: Install relevant domain-specific MCPs using skill-recommender
4. **Understand citation norms**: Follow field-specific citation practices
5. **Engage with community**: Reference key researchers and institutions in your area

**Remember**: The skill-recommender can help identify and install domain-specific MCP servers tailored to your research needs.
