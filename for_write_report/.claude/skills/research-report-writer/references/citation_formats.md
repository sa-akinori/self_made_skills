# Citation Formats Guide

This guide provides citation format guidelines for research reports.

## Default Citation Style

**For scientific and technical reports**: Use **numbered citation style** (Vancouver style)

**For business and market reports**: Use **author-year style** (APA-like)

---

## Numbered Citation Style (Vancouver)

### In-Text Citations

**Single source**:
```
Deep learning has revolutionized computer vision [1].
```

**Multiple sources**:
```
Several studies have demonstrated this approach [1-3].
Optimization techniques are well-documented [1,4,7,12].
```

**Sequential citations**:
```
Early studies [1,2] identified the pattern, while recent work [3-5] provided theoretical foundations.
```

### Reference List Format

**Journal article**:
```
[1] Smith J, Johnson A, Williams B. Advances in neural architecture search. Nature Machine Intelligence. 2023;5(3):123-134. doi:10.1038/s42256-023-00456-7
```

**Components**:
- [Number]
- Authors (Last Name Initial, up to 6 authors, then "et al.")
- Article title (sentence case)
- Journal name (abbreviated or full)
- Year;Volume(Issue):Pages
- DOI

**Book**:
```
[2] Brown C, Davis E. Deep Learning Fundamentals. 2nd ed. New York: Springer; 2024.
```

**Book chapter**:
```
[3] Wilson F. Optimization algorithms for neural networks. In: Taylor G, editor. Modern Machine Learning Methods. Boston: Academic Press; 2023. p. 45-67.
```

**Preprint** (ArXiv, bioRxiv, etc.):
```
[4] Martinez R, Lopez S. Novel transformer architecture for time series. arXiv. 2024. doi:10.48550/arXiv.2024.01234 [Preprint]
```

**Conference paper**:
```
[5] Chen X, Wang Y. Graph neural networks for recommendation. In: Proceedings of NeurIPS 2023; 2023 Dec 10-16; New Orleans, LA. Neural Information Processing Systems Foundation; 2023. p. 1234-1245.
```

**Website/Online resource**:
```
[6] GitHub. PyTorch documentation [Internet]. San Francisco: GitHub Inc.; 2024 [cited 2024 Jan 15]. Available from: https://pytorch.org/docs/
```

**Dataset**:
```
[7] ImageNet Large Scale Visual Recognition Challenge [Internet]. Stanford University; 2015 [cited 2024 Jan 15]. Available from: https://www.image-net.org/challenges/LSVRC/
```

**Technical report**:
```
[8] OpenAI. GPT-4 Technical Report. OpenAI Technical Report 2023-001. San Francisco: OpenAI; 2023.
```

---

## Author-Year Citation Style (APA)

### In-Text Citations

**Single author**:
```
According to Smith (2023), deep learning has transformed natural language processing.
Recent research shows significant improvements (Smith, 2023).
```

**Two authors**:
```
Johnson and Williams (2024) demonstrated the effectiveness of this approach.
The method shows promise (Johnson & Williams, 2024).
```

**Three or more authors**:
```
Martinez et al. (2023) proposed a novel architecture.
Performance improvements were observed (Martinez et al., 2023).
```

**Multiple works**:
```
Several studies support this finding (Brown, 2022; Chen, 2023; Davis, 2024).
```

**Multiple works by same author**:
```
Smith (2022, 2023, 2024) has extensively studied this phenomenon.
```

### Reference List Format

**Journal article**:
```
Smith, J., Johnson, A., & Williams, B. (2023). Advances in neural architecture search. Nature Machine Intelligence, 5(3), 123-134. https://doi.org/10.1038/s42256-023-00456-7
```

**Book**:
```
Brown, C., & Davis, E. (2024). Deep learning fundamentals (2nd ed.). Springer.
```

**Book chapter**:
```
Wilson, F. (2023). Optimization algorithms for neural networks. In G. Taylor (Ed.), Modern machine learning methods (pp. 45-67). Academic Press.
```

**Preprint**:
```
Martinez, R., & Lopez, S. (2024). Novel transformer architecture for time series. arXiv. https://doi.org/10.48550/arXiv.2024.01234 (Preprint)
```

**Conference paper**:
```
Chen, X., & Wang, Y. (2023, December 10-16). Graph neural networks for recommendation [Conference presentation]. NeurIPS 2023, New Orleans, LA, United States.
```

**Website**:
```
GitHub. (2024). PyTorch documentation. https://pytorch.org/docs/ (Accessed: 2024-01-15)
```

**Dataset**:
```
Stanford University. (2015). ImageNet Large Scale Visual Recognition Challenge. https://www.image-net.org/challenges/LSVRC/ (Accessed: 2024-01-15)
```

**Technical report**:
```
OpenAI. (2023). GPT-4 technical report (Report No. 2023-001). https://openai.com/research/gpt-4
```

---

## Special Cases

### Same Author, Same Year

**[Numbered]**: Use alphabetical suffixes
```
[1] Smith J. Optimization methods. 2023.
[2] Smith J. Learning rate schedules. 2023.
```

**[Author-year]**: Use alphabetical suffixes
```
Smith, J. (2023a). Optimization methods...
Smith, J. (2023b). Learning rate schedules...
```

### Preprints

**[Numbered]**: Include "[Preprint]" marker and preprint server DOI
```
... arXiv. 2024. doi:10.48550/arXiv.2024.01234 [Preprint]
```

**[Author-year]**: Include "(Preprint)" at the end
```
... arXiv. https://doi.org/10.48550/arXiv.2024.01234 (Preprint)
```

### Press Releases / News

**[Numbered]**: Include "[Press release]" marker
```
[10] Google AI. Announcing Gemini 2.0 [Press release]. Mountain View; 2024 Jan 10.
```

**[Author-year]**: Include type in brackets
```
Google AI. (2024, January 10). Announcing Gemini 2.0 [Press release].
```

---

## Citation Density Guidelines

### High Citation Density

Use when:
- Making factual claims about research findings
- Discussing specific methodologies
- Presenting quantitative data
- Controversial or debated topics

**Example**:
```
Deep neural networks have achieved remarkable performance on image classification tasks [1,2]. Convolutional architectures dominate the field [3-5], with residual connections providing significant improvements [6,7]. Recent transformer-based models have shown competitive results [8-10], achieving state-of-the-art accuracy on ImageNet [11].
```

### Medium Citation Density

Use when:
- General background information
- Well-established facts
- Synthesizing multiple sources

**Example**:
```
The field of deep learning has evolved rapidly over the past decade [1]. Major breakthroughs include convolutional networks for vision [2], recurrent networks for sequences [3], and attention mechanisms for various tasks [4]. These advances have enabled applications in natural language processing, computer vision, and reinforcement learning [5].
```

### Low Citation Density

Use when:
- Introducing common knowledge in the field
- Describing your own methodology
- Presenting original analysis

**Example**:
```
We implemented a standard transformer architecture with 12 layers and 768 hidden dimensions. The model was trained on 8 NVIDIA A100 GPUs using the Adam optimizer. Training converged after approximately 100,000 steps.
```

---

## Managing Citations During Writing

### Workflow

1. **During research**: Collect full citation info immediately
   - Author names, title, journal/venue, year, DOI/URL
   - Use a reference manager or spreadsheet

2. **During writing**: Insert citation markers
   - **Numbered style**: Use sequential numbers [1], [2], etc.
   - **Author-year**: Use (Author, Year) format

3. **After writing**: Build reference list
   - Verify all citations have matching references
   - Check for formatting consistency
   - Ensure DOIs/URLs are correct

### Tools for Citation Management

- **Manual**: Maintain numbered list in spreadsheet
- **Reference managers**: Zotero, Mendeley, EndNote (for complex projects)
- **LaTeX**: BibTeX for automated formatting

### Common Mistakes to Avoid

1. **Incomplete citations**: Missing DOI, page numbers, or issue numbers
2. **Inconsistent formatting**: Mixing citation styles within same document
3. **Orphaned citations**: Citation number with no corresponding reference
4. **Duplicate references**: Same source listed multiple times with different numbers
5. **Incorrect author order**: Authors not in the order shown on original paper

### Quick Tips

1. **Cite as you write**: Don't delay adding citations
2. **Use placeholders**: [CITE: Smith optimization] if you don't have full info yet
3. **Verify before finalizing**: Cross-check all citations against original sources
4. **Update preprints**: If preprint is later published, update to journal citation
5. **Maintain consistency**: Stick to one citation style throughout

---

## Domain-Specific Citation Guidelines

### Computer Science / Machine Learning

**Key sources**:
- Conference papers (NeurIPS, ICML, ICLR, CVPR, ACL)
- ArXiv preprints
- Technical reports (OpenAI, Google, DeepMind)
- Code repositories (GitHub with DOI via Zenodo)

**Citation priorities**:
1. Peer-reviewed conference/journal papers
2. ArXiv preprints (for very recent work)
3. Technical reports from reputable institutions
4. Code repositories (when referencing implementations)

### Data Science / Statistics

**Key sources**:
- Journal papers (JMLR, Journal of Statistical Software)
- R/Python package documentation
- Kaggle competitions and datasets
- Statistical methodology papers

**Special considerations**:
- Cite software packages with version numbers
- Reference datasets with access dates
- Include statistical method citations

### Finance / Economics

**Key sources**:
- Journal papers (Journal of Finance, Econometrica)
- Working papers (SSRN, NBER)
- Central bank reports
- Financial data sources (Bloomberg, Reuters)

**Special considerations**:
- Cite data sources with specific date ranges
- Reference market indices with provider
- Include regulatory documents when relevant

### Social Sciences

**Key sources**:
- Journal papers (peer-reviewed)
- Government reports and census data
- Survey datasets
- NGO/research institute reports

**Special considerations**:
- Cite datasets with version/year
- Reference survey methodologies
- Include institutional reports

---

## Example Reference Lists

### Machine Learning Research Report

**Numbered style**:

```
References

[1] Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need. In: Proceedings of NeurIPS 2017; 2017 Dec 4-9; Long Beach, CA. Neural Information Processing Systems Foundation; 2017. p. 5998-6008.

[2] Devlin J, Chang MW, Lee K, Toutanova K. BERT: Pre-training of deep bidirectional transformers for language understanding. In: Proceedings of NAACL-HLT 2019; 2019 Jun 2-7; Minneapolis, MN. Association for Computational Linguistics; 2019. p. 4171-4186.

[3] Brown T, Mann B, Ryder N, et al. Language models are few-shot learners. In: Proceedings of NeurIPS 2020; 2020 Dec 6-12; Virtual. Neural Information Processing Systems Foundation; 2020. p. 1877-1901.

[4] Dosovitskiy A, Beyer L, Kolesnikov A, et al. An image is worth 16x16 words: Transformers for image recognition at scale. arXiv. 2020. doi:10.48550/arXiv.2010.11929 [Preprint]

[5] OpenAI. GPT-4 Technical Report. OpenAI Technical Report 2023-001. San Francisco: OpenAI; 2023.
```

**Author-year style**:

```
References

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020, December 6-12). Language models are few-shot learners [Conference presentation]. NeurIPS 2020, Virtual.

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019, June 2-7). BERT: Pre-training of deep bidirectional transformers for language understanding [Conference presentation]. NAACL-HLT 2019, Minneapolis, MN, United States.

Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., ... & Houlsby, N. (2020). An image is worth 16x16 words: Transformers for image recognition at scale. arXiv. https://doi.org/10.48550/arXiv.2010.11929 (Preprint)

OpenAI. (2023). GPT-4 technical report (Report No. 2023-001). https://openai.com/research/gpt-4

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017, December 4-9). Attention is all you need [Conference presentation]. NeurIPS 2017, Long Beach, CA, United States.
```

---

## Quality Checklist

Before finalizing citations:

- [ ] **All claims cited**: Every factual claim has supporting citation
- [ ] **Complete information**: All references have authors, title, year, venue
- [ ] **Consistent style**: Single citation format used throughout
- [ ] **DOIs included**: Digital object identifiers for all papers that have them
- [ ] **URLs functional**: All web links tested and working
- [ ] **Author names correct**: Verified against original publications
- [ ] **No orphans**: Every citation number has matching reference entry
- [ ] **Chronological/alphabetical**: References ordered correctly
- [ ] **Special characters**: Properly escaped in LaTeX or formatted in Markdown
- [ ] **Preprints marked**: Clear indication of non-peer-reviewed sources

---

## Conclusion

Proper citation is essential for research report credibility. Choose the citation style appropriate for your field (numbered for technical/scientific, author-year for business/social sciences), maintain consistency throughout, and ensure completeness of all bibliographic information.
