# A Segment-Level Expected Loss Framework for Unsecured Revolving Credit: The Cardinal Loss Rate Model (CLRM v4.2) vs HELIX: A Lifetime, Account-Level Loss Engine for Credit Card Portfolios

**Champion:** `lit_md/champion.md`
**Challenger:** `lit_md/challenger.md`
**Model:** sentence-transformers/all-MiniLM-L6-v2 (revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`)
**Layout:** html-table
**Generated:** 2026-09-13T00:34:57+00:00

<details><summary>Run parameters</summary>

| Parameter | Value |
|---|---|
| model | sentence-transformers/all-MiniLM-L6-v2 |
| revision | None |
| device | cpu |
| threads | None |
| batch_size | 32 |
| calibration | percentile |
| blend_weight | 0.5 |
| section_top_k | 3 |
| section_margin | 0.03 |
| section_anchor_floor | 0.75 |
| section_secondary_floor | 0.9 |
| section_capacity | 3 |
| section_weak_floor | 0.93 |
| block_top_k | 2 |
| block_margin | 0.02 |
| block_anchor_floor | 0.8 |
| block_secondary_floor | 0.95 |
| block_capacity | 1 |
| block_weak_floor | 0.97 |
| coverage_floor | 0.9 |
| inline_diff_floor | 0.97 |
| excerpt_chars | 420 |
| layout | html-table |
| include_matrix | False |
| cache | True |

</details>

<details><summary>Calibration (this pair's own null distribution)</summary>

| Stat | Raw cosine |
|---|---|
| min | 0.0604 |
| p05 | 0.1709 |
| median | 0.3944 |
| p95 | 0.6205 |
| max | 0.7648 |
| lexical median | 0.037 |
| lexical max | 0.3383 |
| mode | percentile |

Decile distribution (raw cosine, 0–100%): [0.0604, 0.2145, 0.2636, 0.3128, 0.3553, 0.3944, 0.4342, 0.4804, 0.5205, 0.5696, 0.7648]

</details>


## Scorecard

| Metric | Value |
|---|---|
| Mean accepted score | 0.951 |
| Accepted pairs (strong / weak) | 18 (12 / 6) |
| Anchors | 5 |
| Sections (champion / challenger) | 27 / 22 |
| Left-only / right-only sections | 10 / 9 |
| Split / merge / moved | 6 / 6 / 8 |
| Order divergence (1 − LIS/pairs) | 0.4444 |
| Kendall tau | 0.1952 |
| Document cosine (not the headline — see note) | 0.8674 |

**Coverage (champion → challenger):** overall 0.9454 — prose 0.9681, table 0.9321, math 0.6071
**Coverage (challenger → champion):** overall 0.8771 — prose 0.8697, table 0.8832, math 1.0

## Table of contents

- [Alignment map](#alignment-map)
- [Side-by-side](#side-by-side)
- [Only in champion](#only-in-champion)
- [Only in challenger](#only-in-challenger)
- [Numeral cross-index](#numeral-cross-index)
- [Citation overlap](#citation-overlap)
- [Terminology diff](#terminology-diff)
- [Table pairs](#table-pairs)

## Alignment map

| # | Champion section | cos | score | Challenger section | relation | moved |
|---|---|---|---|---|---|---|
| 1 | Abstract | 0.7648 | 0.9928 | Executive Summary | split |  |
| 2 | Abstract | 0.6075 | 0.9492 | The horizon problem | split |  |
| 3 | Abstract | 0.5791 | 0.9286 | Results | weak | yes |
| 4 | 1. Introduction | 0.6453 | 0.948 | The horizon problem | split |  |
| 5 | 1. Introduction | 0.5366 | 0.9146 | The factor-correlation problem | weak |  |
| 6 |  | — | 0.7535 | Part I — Why a Lifetime Account-Level Framework | right-only |  |
| 7 | 2. Related Work | — | 0.9504 |  | left-only |  |
| 8 | 3. Data | — | 0.7324 |  | left-only |  |
| 9 | 3.1 Portfolio description | — | 0.7772 |  | left-only |  |
| 10 |  | — | 0.7493 | Part II — The Framework | right-only |  |
| 11 |  | — | 0.8984 | Notation and assembly | right-only |  |
| 12 | 3.2 Segmentation scheme | — | 0.8293 |  | left-only |  |
| 13 | 3.3 Default definition | 0.5246 | 0.9062 | Box 1 — What HELIX does not change | weak |  |
| 14 | 4. Methodology | — | 0.7447 |  | left-only |  |
| 15 | 4.1 Loss rate decomposition | 0.6582 | 0.9758 | Executive Summary | merge | yes |
| 16 | 4.2 Probability of default | 0.5933 | 0.9152 | Default hazard | weak |  |
| 17 | 4.3 Exposure at default | 0.7136 | 0.9916 | Exposure simulation | merge |  |
| 18 | 4.4 Loss given default | 0.6575 | 0.9842 | Loss severity | merge | yes |
| 19 | 4.5 Aggregation and stress overlay | 0.5322 | 0.9189 | The factor-correlation problem | weak | yes |
| 20 | 5. Model Estimation Results | — | 0.6977 |  | left-only |  |
| 21 | 5.1 PD estimates | — | 0.8632 |  | left-only |  |
| 22 |  | — | 0.6283 | Behavioural life | right-only |  |
| 23 | 5.2 CCF estimates | 0.6529 | 0.948 | Exposure simulation | merge |  |
| 24 | 5.3 LGD estimates | 0.6338 | 0.9636 | Loss severity | merge |  |
| 25 | 5.4 Assembled loss rate | — | 0.8971 |  | left-only |  |
| 26 |  | — | 0.6479 | Part III — Governance, Weaknesses and the Promotion Question | right-only |  |
| 27 |  | — | 0.8498 | Where HELIX is worse than the incumbent | right-only |  |
| 28 | 6. Validation | — | 0.7084 |  | left-only |  |
| 29 | 6.1 Discriminatory power | — | 0.7155 |  | left-only |  |
| 30 | 6.2 Calibration and backtest | 0.5251 | 0.9104 | Results | weak | yes |
| 31 |  | — | 0.6144 | Where the incumbent is not salvageable | right-only |  |
| 32 |  | — | 0.6961 | Recommendation | right-only |  |
| 33 |  | — | 0.6622 | Required controls if promoted | right-only |  |
| 34 | 6.3 Independence-assumption bias | 0.5662 | 0.9418 | The factor-correlation problem | merge | yes |
| 35 | 6.4 Sensitivity | — | 0.655 |  | left-only |  |
| 36 | 7. Limitations and Known Findings | 0.7254 | 0.971 | Executive Summary | split | yes |
| 37 | 7. Limitations and Known Findings | 0.6545 | 0.971 | The aggregation problem | split | yes |
| 38 | 7. Limitations and Known Findings | 0.6985 | 0.9867 | Loss severity | split |  |
| 39 | 8. Conclusion | — | 0.9382 |  | left-only |  |
| 40 | References | 0.0 | 0.1333 | Selected References | 1:1 |  |
| 41 |  | — | 0.6441 | Annexes | right-only |  |
| 42 |  | — | 0.6755 | Annex 1 · Data lineage | right-only |  |
| 43 | Appendix A. Delinquent-Account Roll-Rate Treatment | — | 0.7954 |  | left-only |  |
| 44 |  | — | 0.9358 | Annex 2 · Reconciliation to the incumbent | right-only |  |
| 45 | Appendix B. Variable Dictionary | — | 0.8922 |  | left-only |  |
| 46 |  | — | 0.379 | Annex 3 · Reproducibility | right-only |  |

## Side-by-side

### Abstract ↔ Executive Summary

_relation: split — score 0.9928_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>We document the specification, estimation and validation of the Cardinal Loss Rate Model (CLRM), the incumbent expected credit loss engine for Meridian Bancorp's unsecured credit card portfolio. CLRM decomposes the twelve-month portfolio loss rate into the classical product of probability of default (PD), exposure at default (EAD) and loss given default (LGD), estimated at the level of 48 homogeneous risk segments de…<br><sub>lit_md/champion.md:15</sub></td><td>0.9898</td><td>HELIX estimates credit card credit losses account by account and month by month over the full behavioural life of each account, rather than producing a single twelve-month loss rate for a risk segment. Loss is assembled as a discounted sum over monthly survival-weighted default events:<br><sub>lit_md/challenger.md:17</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>We document the specification, estimation and validation of the Cardinal Loss Rate Model (CLRM), the incumbent expected credit loss engine for Meridian Bancorp's unsecured</del> <strong>HELIX estimates</strong> credit card <del>portfolio. CLRM decomposes</del> <strong>credit losses account by account and month by month over</strong> the <strong>full behavioural life of each account, rather than producing a single</strong> twelve-month <del>portfolio</del> loss rate <del>into the classical product of probability of</del> <strong>for a risk segment. Loss is assembled as a discounted sum over monthly survival-weighted</strong> default <del>(PD), exposure at default (EAD) and loss given default (LGD), estimated at the level of 48 homogeneous risk segments defined by a cross of behaviour score band, utilization band and delinquency stage. PD is estimated with a segment-conditional logistic regression on a quarterly cohort panel spanning 2009Q1-2023Q4; EAD is estimated through a credit conversion factor (CCF) applied to undrawn commitments; LGD is estimated as one minus a beta-regression recovery rate on post-charge-off cash collections. On a holdout period covering 2021Q1-2023Q4 the model reproduces the realized annualized net loss rate of 3.41% with an absolute error of 14 basis points, and achieves a segment-level Gini coefficient of 0.612 on the twelve-month default indicator. We argue that the transparency and stability of a segment-level multiplicative decomposition outweigh the modest discriminatory gains available from account-level machine learning alternatives, and we provide the sensitivity analysis required to support that claim.</del> <strong>events:</strong></td></tr>
<tr><td>**Keywords:** expected credit loss, credit cards, probability of default, exposure at default, loss given default, credit conversion factor, loss rate<br><sub>lit_md/champion.md:17</sub></td><td>0.9974</td><td>The three factors are the same as in any expected-loss framework — a default probability, an exposure, and a loss severity — but each is a *function of account age and of a macroeconomic path* rather than a segment constant.<br><sub>lit_md/challenger.md:21</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>**Keywords:** expected credit loss, credit cards, probability</del> <strong>The three factors are the same as in any expected-loss framework - a default probability, an exposure, and a loss severity - but each is a *function</strong> of <del>default, exposure at default, loss given default, credit conversion factor, loss rate</del> <strong>account age and of a macroeconomic path* rather than a segment constant.</strong></td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- **JEL:** G21, G28, C25 (`lit_md/champion.md:19`)
_Challenger content in this section pair with no counterpart here:_
- <code>\text{Loss}_i = \sum_{m=1}^{M_i} S_i(m-1) \, h_i(m) \, \widehat{EAD}_i(m) \, \widehat{LGD}_i(m) \, (1+r)^{-m/12}.</code> (`lit_md/challenger.md:19`)
- Headline findings on the 2015–2023 panel: (`lit_md/challenger.md:23`)
- Monthly hazard estimated by gradient-boosted trees attains an out-of-time AUC of **0.847** on the next-12-month default indicator, against **0.803** for a reproduction of the incumbent segment logit on the same sample. (`lit_md/challenger.md:25`)
- Lifetime loss rate for the 2023Q4 book is **8.94%** of outstanding balance at a 24-month behavioural life assumption, decomposing into 4.11% in the first twelve months and 4.83% thereafter. (`lit_md/challenger.md:25`)
- Exposure is simulated rather than scaled: the fitted balance path reproduces the observed pre-default run-up with a mean absolute error of 3.2% of limit, against 7.9% for a fixed credit conversion factor. (`lit_md/challenger.md:25`)
- Severity is estimated as a *discounted* recovery curve. Discounting at the effective interest rate raises portfolio LGD from 0.851 (nominal) to **0.879**. (`lit_md/challenger.md:25`)
- Forecast volatility is materially higher: the month-over-month standard deviation of the portfolio lifetime loss rate is 31 basis points, against 9 basis points for the incumbent. (`lit_md/challenger.md:25`)
- The last bullet is the crux of the promotion decision and is treated at length in Part III. (`lit_md/challenger.md:31`)

### Abstract ↔ The horizon problem

_relation: split — score 0.9492_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>**Keywords:** expected credit loss, credit cards, probability of default, exposure at default, loss given default, credit conversion factor, loss rate<br><sub>lit_md/champion.md:17</sub></td><td>0.9858</td><td>A twelve-month loss rate answers a question that neither the accounting standard nor the pricing desk actually asks. Accounting requires expected credit losses over the expected life of the exposure; pricing requires the net present value of a relationship. The incumbent framework answers both by multiplying a twelve-month number by a judgmental lifetime factor, currently 2.18. That factor is a single scalar applied…<br><sub>lit_md/challenger.md:39</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>**Keywords:**</del> <strong>A twelve-month loss rate answers a question that neither the accounting standard nor the pricing desk actually asks. Accounting requires</strong> expected credit <del>loss, credit cards, probability</del> <strong>losses over the expected life</strong> of <del>default, exposure at default, loss given default, credit conversion</del> <strong>the exposure; pricing requires the net present value of a relationship. The incumbent framework answers both by multiplying a twelve-month number by a judgmental lifetime</strong> factor, <del>loss rate</del> <strong>currently 2.18. That factor is a single scalar applied across a portfolio whose behavioural lives differ by a factor of four between the revolver and transactor populations.</strong></td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- We document the specification, estimation and validation of the Cardinal Loss Rate Model (CLRM), the incumbent expected credit loss engine for Meridian Bancorp's unsecured credit card portfolio. CLRM decomposes the twelve-month portfolio loss rate into the classical product of probability of default (PD), exposure at default (EAD) and loss given default (LGD), estimated at the level of 48 homogeneous risk segments de… (`lit_md/champion.md:15`)
- **JEL:** G21, G28, C25 (`lit_md/champion.md:19`)
_Challenger content in this section pair with no counterpart here:_
- Directly modelling the monthly timing of default removes the scalar. It also produces, as a by-product, the timing profile needed for interest-income projection and for the staging decisions that the incumbent cannot support. (`lit_md/challenger.md:41`)

### Abstract ↔ Results

_relation: weak (moved) — score 0.9286_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>We document the specification, estimation and validation of the Cardinal Loss Rate Model (CLRM), the incumbent expected credit loss engine for Meridian Bancorp's unsecured credit card portfolio. CLRM decomposes the twelve-month portfolio loss rate into the classical product of probability of default (PD), exposure at default (EAD) and loss given default (LGD), estimated at the level of 48 homogeneous risk segments de…<br><sub>lit_md/champion.md:15</sub></td><td>0.954</td><td><table class="lc-nested"><caption>Table — out-of-time discrimination, next-12-month default</caption><thead><tr><th>Model</th><th>AUC</th><th>Gini</th><th>KS</th></tr></thead><tbody><tr><td>Incumbent segment logit (reproduced on this panel)</td><td>0.803</td><td>0.606</td><td>0.443</td></tr><tr><td>HELIX hazard, monotone-constrained</td><td>0.847</td><td>0.694</td><td>0.521</td></tr><tr><td>HELIX hazard, unconstrained</td><td>0.851</td><td>0.702</td><td>0.527</td></tr><tr><td>HELIX hazard, no macro features</td><td>0.844</td><td>0.688</td><td>0.517</td></tr></tbody></table><br><sub>lit_md/challenger.md:163</sub></td></tr>
<tr><td>**Keywords:** expected credit loss, credit cards, probability of default, exposure at default, loss given default, credit conversion factor, loss rate<br><sub>lit_md/champion.md:17</sub></td><td>0.9431</td><td><table class="lc-nested"><caption>Table — lifetime loss rate build-up, 2023Q4 book, baseline macro path</caption><thead><tr><th>Behavioural cohort</th><th>Balance share</th><th>12m loss rate</th><th>Lifetime loss rate</th><th>Mean behavioural life (months)</th></tr></thead><tbody><tr><td>Transactor</td><td>21.4%</td><td>0.61%</td><td>1.02%</td><td>14.1</td></tr><tr><td>Light revolver</td><td>28.9%</td><td>2.14%</td><td>4.77%</td><td>31.6</td></tr><tr><td>Heavy revolver</td><td>34.7%</td><td>5.38%</td><td>12.91%</td><td>34.8</td></tr><tr><td>Deteriorating</td><td>11.2%</td><td>13.92%</td><td>21.06%</td><td>18.3</td></tr><tr><td>Delinquent at reporting date</td><td>3.8%</td><td>42.71%</td><td>46.18%</td><td>9.2</td></tr><tr><td>**Portfolio**</td><td>**100%**</td><td>**4.11%**</td><td>**8.94%**</td><td>**27.4**</td></tr></tbody></table><br><sub>lit_md/challenger.md:150</sub></td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- **JEL:** G21, G28, C25 (`lit_md/champion.md:19`)
_Challenger content in this section pair with no counterpart here:_
- Note that the behavioural cohorts above are a *reporting* view constructed after estimation for communication purposes; they are not an estimation unit. Nothing in HELIX is fitted at cohort level. (`lit_md/challenger.md:161`)
- Macro features contribute little to *ranking* — the relative ordering of accounts is nearly unchanged — but they carry nearly all of the *level* response across the 2020 stress period, which is the property that matters for scenario forecasting. (`lit_md/challenger.md:172`)
- <table class="lc-nested"><caption>Table — backtest of realized twelve-month losses, out-of-time</caption><thead><tr><th>Period</th><th>Incumbent predicted</th><th>HELIX predicted</th><th>Realized</th><th>HELIX error (bps)</th></tr></thead><tbody><tr><td>2022H1</td><td>2.81%</td><td>2.94%</td><td>3.02%</td><td>−8</td></tr><tr><td>2022H2</td><td>3.11%</td><td>3.19%</td><td>3.14%</td><td>+5</td></tr><tr><td>2023H1</td><td>3.44%</td><td>3.31%</td><td>3.28%</td><td>+3</td></tr><tr><td>2023H2</td><td>3.72%</td><td>3.57%</td><td>3.53%</td><td>+4</td></tr></tbody></table> (`lit_md/challenger.md:174`)

### 1. Introduction ↔ The horizon problem

_relation: split — score 0.948_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>The regulatory and accounting literature has converged on a multiplicative decomposition of expected loss,<br><sub>lit_md/champion.md:27</sub></td><td>0.991</td><td>A twelve-month loss rate answers a question that neither the accounting standard nor the pricing desk actually asks. Accounting requires expected credit losses over the expected life of the exposure; pricing requires the net present value of a relationship. The incumbent framework answers both by multiplying a twelve-month number by a judgmental lifetime factor, currently 2.18. That factor is a single scalar applied…<br><sub>lit_md/challenger.md:39</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <strong>A twelve-month loss rate answers a question that neither the accounting standard nor the pricing desk actually asks. Accounting requires expected credit losses over the expected life of the exposure; pricing requires the net present value of a relationship.</strong> The <del>regulatory</del> <strong>incumbent framework answers both by multiplying a twelve-month number by a judgmental lifetime factor, currently 2.18. That factor is a single scalar applied across a portfolio whose behavioural lives differ by a factor of four between the revolver</strong> and <del>accounting literature has converged on a multiplicative decomposition of expected loss,</del> <strong>transactor populations.</strong></td></tr>
<tr><td>**Discrete annual horizon with cohort stacking.** PD is estimated on twelve-month cohorts rather than on a monthly hazard. This sacrifices timing resolution in exchange for a direct, auditable mapping between the estimation target and the reported twelve-month loss rate.<br><sub>lit_md/champion.md:35</sub></td><td>0.9295</td><td>Directly modelling the monthly timing of default removes the scalar. It also produces, as a by-product, the timing profile needed for interest-income projection and for the staging decisions that the incumbent cannot support.<br><sub>lit_md/challenger.md:41</sub></td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- Unsecured revolving credit remains the most loss-intensive major asset class on the balance sheet of a diversified retail bank. Unlike a term loan, a credit card account has no contractual amortization schedule, a borrower-controlled drawdown option, and a balance that can grow materially in the months immediately preceding default. Any credible loss forecasting framework for the asset class must therefore model not… (`lit_md/champion.md:25`)
- <code>EL = PD \times EAD \times LGD,</code> (`lit_md/champion.md:29`)
- which we adopt without modification. The contribution of this paper is not the decomposition itself but the disciplined treatment of each factor for a revolving retail portfolio, and the demonstration that a segment-level implementation is sufficient for the uses to which the model is put: allowance estimation under CECL, loss forecasting in the annual capital plan, and portfolio-level pricing floors. (`lit_md/champion.md:31`)
- Three design commitments distinguish CLRM from the alternatives reviewed in Section 2. (`lit_md/champion.md:33`)
- **Segment-level estimation.** The unit of observation is a (segment, cohort) cell rather than an account-month. Segments are defined ex ante from variables that the business already uses to manage the portfolio, so that every model output can be traced to a population a line-of-business owner recognizes. (`lit_md/champion.md:35`)
- **Separable factor estimation.** PD, EAD and LGD are estimated independently and combined multiplicatively. Correlation between factors is handled through an explicit stress overlay (Section 4.5) rather than through a joint likelihood. (`lit_md/champion.md:35`)
- Section 2 situates the model in the literature. Section 3 describes the data and the segmentation scheme. Section 4 gives the specification of each factor. Section 5 reports estimation results, Section 6 the validation evidence, and Section 7 the limitations that motivate the challenger program. (`lit_md/champion.md:39`)

### 1. Introduction ↔ The factor-correlation problem

_relation: weak — score 0.9146_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>**Separable factor estimation.** PD, EAD and LGD are estimated independently and combined multiplicatively. Correlation between factors is handled through an explicit stress overlay (Section 4.5) rather than through a joint likelihood.<br><sub>lit_md/champion.md:35</sub></td><td>0.9935</td><td>The product $PD \times EAD \times LGD$ of separately estimated factor means is not the mean of the product. Under stress all three factors deteriorate together, and the product form understates loss. The incumbent handles this with a judgmental additive overlay applied when projected unemployment change exceeds 200 basis points. HELIX instead conditions all three factors on the same macroeconomic path, so that the co…<br><sub>lit_md/challenger.md:52</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>**Separable</del> <strong>The product $PD \times EAD \times LGD$ of separately estimated</strong> factor <del>estimation.** PD, EAD</del> <strong>means is not the mean of the product. Under stress all three factors deteriorate together,</strong> and <del>LGD are estimated independently and combined multiplicatively. Correlation between</del> <strong>the product form understates loss. The incumbent handles this with a judgmental additive overlay applied when projected unemployment change exceeds 200 basis points. HELIX instead conditions all three</strong> factors <strong>on the same macroeconomic path, so that the covariance</strong> is <del>handled through an explicit stress overlay (Section 4.5)</del> <strong>generated by the model</strong> rather than <del>through a joint likelihood.</del> <strong>supplied by committee.</strong></td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- Unsecured revolving credit remains the most loss-intensive major asset class on the balance sheet of a diversified retail bank. Unlike a term loan, a credit card account has no contractual amortization schedule, a borrower-controlled drawdown option, and a balance that can grow materially in the months immediately preceding default. Any credible loss forecasting framework for the asset class must therefore model not… (`lit_md/champion.md:25`)
- The regulatory and accounting literature has converged on a multiplicative decomposition of expected loss, (`lit_md/champion.md:27`)
- <code>EL = PD \times EAD \times LGD,</code> (`lit_md/champion.md:29`)
- which we adopt without modification. The contribution of this paper is not the decomposition itself but the disciplined treatment of each factor for a revolving retail portfolio, and the demonstration that a segment-level implementation is sufficient for the uses to which the model is put: allowance estimation under CECL, loss forecasting in the annual capital plan, and portfolio-level pricing floors. (`lit_md/champion.md:31`)
- Three design commitments distinguish CLRM from the alternatives reviewed in Section 2. (`lit_md/champion.md:33`)
- **Segment-level estimation.** The unit of observation is a (segment, cohort) cell rather than an account-month. Segments are defined ex ante from variables that the business already uses to manage the portfolio, so that every model output can be traced to a population a line-of-business owner recognizes. (`lit_md/champion.md:35`)
- **Discrete annual horizon with cohort stacking.** PD is estimated on twelve-month cohorts rather than on a monthly hazard. This sacrifices timing resolution in exchange for a direct, auditable mapping between the estimation target and the reported twelve-month loss rate. (`lit_md/champion.md:35`)
- Section 2 situates the model in the literature. Section 3 describes the data and the segmentation scheme. Section 4 gives the specification of each factor. Section 5 reports estimation results, Section 6 the validation evidence, and Section 7 the limitations that motivate the challenger program. (`lit_md/champion.md:39`)

### 3.3 Default definition ↔ Box 1 — What HELIX does not change

_relation: weak — score 0.9062_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>An account is treated as defaulted in a cohort if, within twelve months of cohort origin, any of the following occurs: (i) contractual charge-off at 180 days past due; (ii) bankruptcy charge-off; (iii) enrollment in a long-term hardship program with a contractual rate concession exceeding 500 basis points. Definition (iii) contributes 8.4% of defaults and was added in version 4.0 following a 2021 finding by Model Ris…<br><sub>lit_md/champion.md:88</sub></td><td>0.9964</td><td><blockquote>HELIX retains the definition of default (180 days past due, bankruptcy, or long-term hardship with rate concession), the exclusion of private-label and small-business portfolios, and the 36-month recovery observation window. These are held fixed deliberately so that the comparison against the incumbent is attributable to specification rather than to scope.</blockquote><br><sub>lit_md/challenger.md:56</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>An account is treated as defaulted in a cohort if, within twelve months</del> <strong>&gt; HELIX retains the definition</strong> of <del>cohort origin, any of the following occurs: (i) contractual charge-off at 180</del> <strong>default (180</strong> days past <del>due; (ii) bankruptcy charge-off; (iii) enrollment in a</del> <strong>due, bankruptcy, or</strong> long-term hardship <del>program</del> with <del>a contractual</del> rate <del>concession exceeding 500 basis points. Definition (iii) contributes 8.4%</del> <strong>concession), the exclusion</strong> of <del>defaults</del> <strong>private-label</strong> and <del>was added in version 4.0 following a 2021 finding by Model Risk Management</del> <strong>small-business portfolios, and the 36-month recovery observation window. These are held fixed deliberately so</strong> that <del>hardship enrollments were materially under-captured.</del> <strong>the comparison against the incumbent is attributable to specification rather than to scope.</strong></td></tr>
<tr><td colspan="3"><em>numeric changes:</em> 180 → (180</td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- Cohorts are formed quarterly, so the panel contains 60 quarterly cohorts × 48 segments = 2,880 cells, of which 2,844 exceed the 250-account minimum size threshold and enter estimation. (`lit_md/champion.md:90`)

### 4.1 Loss rate decomposition ↔ Executive Summary

_relation: merge (moved) — score 0.9758_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>Let $s$ index segments and $t$ index quarterly cohorts. Define the twelve-month loss rate for segment $s$ in cohort $t$ as the ratio of realized net credit losses to the beginning balance:<br><sub>lit_md/champion.md:98</sub></td><td>0.9882</td><td>HELIX estimates credit card credit losses account by account and month by month over the full behavioural life of each account, rather than producing a single twelve-month loss rate for a risk segment. Loss is assembled as a discounted sum over monthly survival-weighted default events:<br><sub>lit_md/challenger.md:17</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>Let $s$ index segments</del> <strong>HELIX estimates credit card credit losses account by account</strong> and <del>$t$ index quarterly cohorts. Define</del> <strong>month by month over</strong> the <strong>full behavioural life of each account, rather than producing a single</strong> twelve-month loss rate for <del>segment $s$ in cohort $t$</del> <strong>a risk segment. Loss is assembled</strong> as <del>the ratio of realized net credit losses to the beginning balance:</del> <strong>a discounted sum over monthly survival-weighted default events:</strong></td></tr>
<tr><td><code>LR_{s,t} = \frac{\sum_{i \in s,t} D_{i} \cdot E_{i} \cdot (1 - R_{i})}{\sum_{i \in s,t} B_{i}},</code><br><sub>lit_md/champion.md:100</sub></td><td>0.9223</td><td><code>\text{Loss}_i = \sum_{m=1}^{M_i} S_i(m-1) \, h_i(m) \, \widehat{EAD}_i(m) \, \widehat{LGD}_i(m) \, (1+r)^{-m/12}.</code><br><sub>lit_md/challenger.md:19</sub></td></tr>
<tr><td>where $D_i$ is the default indicator, $E_i$ the exposure at default, $R_i$ the ultimate recovery rate and $B_i$ the beginning balance. Taking expectations segment by segment and replacing the ratio of expectations with the product of factor estimates yields the working form of the model:<br><sub>lit_md/champion.md:102</sub></td><td>0.973</td><td>The three factors are the same as in any expected-loss framework — a default probability, an exposure, and a loss severity — but each is a *function of account age and of a macroeconomic path* rather than a segment constant.<br><sub>lit_md/challenger.md:21</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>where $D_i$</del> <strong>The three factors are the same as in any expected-loss framework - a default probability, an exposure, and a loss severity - but each</strong> is <del>the default indicator, $E_i$ the exposure at default, $R_i$ the ultimate recovery rate</del> <strong>a *function of account age</strong> and <del>$B_i$ the beginning balance. Taking expectations</del> <strong>of a macroeconomic path* rather than a</strong> segment <del>by segment and replacing the ratio of expectations with the product of factor estimates yields the working form of the model:</del> <strong>constant.</strong></td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- <code>\widehat{LR}_{s,t} = \widehat{PD}_{s,t} \times \widehat{CCF}_{s} \times \frac{L_{s,t}}{B_{s,t}} \times \widehat{LGD}_{s},</code> (`lit_md/champion.md:104`)
- where $L_{s,t}$ is the aggregate committed line and the ratio $L_{s,t}/B_{s,t}$ converts the exposure factor from a line basis to a balance basis. Portfolio loss rate is the balance-weighted sum across segments. (`lit_md/champion.md:106`)
- The replacement of $E[D \cdot E \cdot (1-R)]$ with $E[D] \cdot E[E] \cdot E[1-R]$ is exact only under factor independence. Section 6.3 quantifies the induced bias. (`lit_md/champion.md:108`)
_Challenger content in this section pair with no counterpart here:_
- Headline findings on the 2015–2023 panel: (`lit_md/challenger.md:23`)
- Monthly hazard estimated by gradient-boosted trees attains an out-of-time AUC of **0.847** on the next-12-month default indicator, against **0.803** for a reproduction of the incumbent segment logit on the same sample. (`lit_md/challenger.md:25`)
- Lifetime loss rate for the 2023Q4 book is **8.94%** of outstanding balance at a 24-month behavioural life assumption, decomposing into 4.11% in the first twelve months and 4.83% thereafter. (`lit_md/challenger.md:25`)
- Exposure is simulated rather than scaled: the fitted balance path reproduces the observed pre-default run-up with a mean absolute error of 3.2% of limit, against 7.9% for a fixed credit conversion factor. (`lit_md/challenger.md:25`)
- Severity is estimated as a *discounted* recovery curve. Discounting at the effective interest rate raises portfolio LGD from 0.851 (nominal) to **0.879**. (`lit_md/challenger.md:25`)
- Forecast volatility is materially higher: the month-over-month standard deviation of the portfolio lifetime loss rate is 31 basis points, against 9 basis points for the incumbent. (`lit_md/challenger.md:25`)
- The last bullet is the crux of the promotion decision and is treated at length in Part III. (`lit_md/challenger.md:31`)

### 4.2 Probability of default ↔ Default hazard

_relation: weak — score 0.9152_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td><table class="lc-nested"><thead><tr><th>Symbol</th><th>Definition</th><th>Source</th></tr></thead><tbody><tr><td>$\Delta u_t$</td><td>Four-quarter change in national unemployment rate</td><td>BLS</td></tr><tr><td>$hpi_t$</td><td>Four-quarter log change in national house price index</td><td>FHFA</td></tr><tr><td>$dsr_t$</td><td>Household debt service ratio, level</td><td>Federal Reserve H.8</td></tr><tr><td>$pay_{s,t}$</td><td>Segment mean payment rate (payments ÷ beginning balance)</td><td>Internal</td></tr><tr><td>$\Delta util_{s,t}$</td><td>Segment mean four-quarter change in utilization</td><td>Internal</td></tr></tbody></table><br><sub>lit_md/champion.md:118</sub></td><td>0.929</td><td><table class="lc-nested"><thead><tr><th>Family</th><th>Features</th><th>Examples</th></tr></thead><tbody><tr><td>Delinquency dynamics</td><td>11</td><td>current bucket, worst bucket in 6m, cure count in 12m</td></tr><tr><td>Payment behaviour</td><td>9</td><td>payment/minimum ratio, 3m and 12m means, trend slope</td></tr><tr><td>Balance and utilization</td><td>8</td><td>utilization level, 6m change, cash-advance share</td></tr><tr><td>Bureau attributes</td><td>7</td><td>refreshed score, external trade delinquency, inquiry velocity</td></tr><tr><td>Account structure</td><td>5</td><td>months on book, limit, product, rate, promotional-balance flag</td></tr><tr><td>Macro (path-conditioned)</td><td>4</td><td>unemployment level and 12m change, debt service ratio, retail sales growth</td></tr></tbody></table><br><sub>lit_md/challenger.md:84</sub></td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- PD is estimated by pooled logistic regression on the cohort panel, with segment fixed effects and macroeconomic covariates: (`lit_md/champion.md:112`)
- <code>\ln\left(\frac{PD_{s,t}}{1 - PD_{s,t}}\right) = \alpha_s + \beta_1 \Delta u_{t} + \beta_2 \, hpi_{t} + \beta_3 \, dsr_{t} + \beta_4 \, pay_{s,t} + \beta_5 \, \Delta util_{s,t} + \varepsilon_{s,t}</code> (`lit_md/champion.md:114`)
- with covariates defined as follows: (`lit_md/champion.md:116`)
- Observations are weighted by cell account count. The macro covariate set was selected by exhaustive search over a 14-variable candidate library subject to (i) sign consistency with credit intuition, (ii) pairwise correlation below 0.70, and (iii) variance inflation below 5. House price appreciation enters despite the unsecured nature of the product; Delacroix and Whitmore (2011) attribute this to a collateral-substit… (`lit_md/champion.md:126`)
_Challenger content in this section pair with no counterpart here:_
- The hazard is estimated on an account-month panel of 41.8 million rows (2015-01 through 2021-12 for development, 2022-01 through 2023-12 held out of time). The estimator is a gradient-boosted tree ensemble on the binary next-month default indicator, with months-on-book entered as a feature so that the baseline hazard shape is learned rather than imposed. (`lit_md/challenger.md:80`)
- Feature families, with counts after selection: (`lit_md/challenger.md:82`)
- Hyperparameters were tuned by five-fold grouped cross-validation with accounts, not rows, as the grouping unit — a detail that matters, since row-wise folds leak an account's own future and inflated AUC by 0.03 in an early iteration of this work. (`lit_md/challenger.md:93`)
- **Macro conditioning.** Macro features enter as contemporaneous values on the projected path. For forecasting, a macro path is supplied exogenously (baseline, adverse, severely adverse) and the hazard is re-evaluated month by month along that path. The model is therefore point-in-time by construction; no through-the-cycle adjustment is applied. (`lit_md/challenger.md:95`)
- **Interpretability control.** Because a boosted ensemble is not inspectable coefficient by coefficient, monotonic constraints are imposed on eight features where credit intuition gives an unambiguous direction (utilization ↑, delinquency bucket ↑, payment ratio ↓, refreshed score ↓, unemployment ↑, debt service ratio ↑, cash-advance share ↑, inquiry velocity ↑). Constraining these costs 0.004 AUC and is judged worth… (`lit_md/challenger.md:97`)

### 4.3 Exposure at default ↔ Exposure simulation

_relation: merge — score 0.9916_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td><code>EAD_i = B_i + CCF_s \cdot (L_i - B_i).</code><br><sub>lit_md/champion.md:132</sub></td><td>0.9788</td><td><code>\Delta B_i(m) = \underbrace{\pi_i(m) \cdot (L_i - B_i(m-1))}_{\text{purchase/drawdown}} - \underbrace{\rho_i(m) \cdot B_i(m-1)}_{\text{payment}},</code><br><sub>lit_md/challenger.md:103</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>$$EAD_i</del> <strong>$$\Delta B_i(m)</strong> = <del>B_i + CCF_s</del> <strong>\underbrace{\pi_i(m)</strong> \cdot (L_i - <del>B_i).$$</del> <strong>B_i(m-1))}_{\text{purchase/drawdown}} - \underbrace{\rho_i(m) \cdot B_i(m-1)}_{\text{payment}},$$</strong></td></tr>
<tr><td>$CCF_s$ is estimated as the ratio of realized additional drawdown to available line over the twelve months preceding charge-off, pooled within segment and winsorized at the 1st and 99th percentiles. The estimator is the *fixed-horizon* variant: for each defaulted account, the reference date is exactly twelve months before the charge-off date, and accounts whose line was reduced by the bank during the window are exclu…<br><sub>lit_md/champion.md:134</sub></td><td>0.9841</td><td>Critically, $\pi$ and $\rho$ are fitted on the *pre-default* trajectory of accounts that subsequently defaulted as well as on survivors, with the default indicator excluded from the feature set to avoid look-ahead. The resulting paths reproduce the empirical run-up: simulated utilization rises from a median 0.63 twelve months before default to 0.97 in the default month, against observed 0.61 and 0.96.<br><sub>lit_md/challenger.md:107</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>$CCF_s$ is estimated</del> <strong>Critically, $\pi$ and $\rho$ are fitted on the *pre-default* trajectory of accounts that subsequently defaulted</strong> as <strong>well as on survivors, with</strong> the <del>ratio of realized additional drawdown</del> <strong>default indicator excluded from the feature set</strong> to <del>available line over</del> <strong>avoid look-ahead. The resulting paths reproduce</strong> the <del>twelve months preceding charge-off, pooled within segment and winsorized at the 1st and 99th percentiles. The estimator is the *fixed-horizon* variant: for each defaulted account, the reference date is exactly</del> <strong>empirical run-up: simulated utilization rises from a median 0.63</strong> twelve months before <strong>default to 0.97 in</strong> the <del>charge-off date,</del> <strong>default month, against observed 0.61</strong> and <del>accounts whose line was reduced by the bank during the window are excluded to avoid attributing management action to borrower behaviour. This exclusion removes 11.2% of defaults and is a known conservatism: excluded accounts had a mean realized drawdown below the retained population.</del> <strong>0.96.</strong></td></tr>
<tr><td colspan="3"><em>numeric changes:</em> 11.2% → 0.96.</td></tr>
<tr><td>CCF is capped at 1.00 and floored at 0.00. No macroeconomic conditioning is applied to CCF; a 2022 study found the through-the-cycle variation in segment CCF to be within the estimation standard error for all but the &gt;90% utilization band.<br><sub>lit_md/champion.md:136</sub></td><td>0.9728</td><td><table class="lc-nested"><caption>Table — exposure accuracy, out-of-time defaults</caption><thead><tr><th>Method</th><th>MAE (% of limit)</th><th>Bias (% of limit)</th><th>Correlation with realized EAD</th></tr></thead><tbody><tr><td>Fixed CCF by utilization band</td><td>7.9</td><td>−1.4</td><td>0.781</td></tr><tr><td>Fixed CCF by full segment cross</td><td>7.1</td><td>−1.1</td><td>0.804</td></tr><tr><td>HELIX simulated path</td><td>3.2</td><td>+0.3</td><td>0.918</td></tr></tbody></table><br><sub>lit_md/challenger.md:109</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <strong>| Method | MAE (% of limit) | Bias (% of limit) | Correlation with realized EAD | |---|---|---|---| | Fixed</strong> CCF <del>is capped at 1.00 and floored at 0.00. No macroeconomic conditioning is applied to CCF; a 2022 study found the through-the-cycle variation in</del> <strong>by utilization band | 7.9 | -1.4 | 0.781 | | Fixed CCF by full</strong> segment <del>CCF to be within the estimation standard error for all but the &gt;90% utilization band.</del> <strong>cross | 7.1 | -1.1 | 0.804 | | HELIX simulated path | 3.2 | +0.3 | 0.918 |</strong></td></tr>
<tr><td colspan="3"><em>numeric changes:</em> 1.00 → 7.9, 0.00. → -1.4, 2022 → 0.781</td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- For a revolving line, exposure at default is decomposed into drawn and undrawn components: (`lit_md/champion.md:130`)
_Challenger content in this section pair with no counterpart here:_
- HELIX does not use a credit conversion factor. Instead the balance path is simulated forward from a two-part model: (`lit_md/challenger.md:101`)
- where the drawdown intensity $\pi$ and the payment rate $\rho$ are each fitted by quantile regression forests on the same feature set as the hazard, then evaluated at the conditional median. Balances are floored at zero and capped at $1.05 L_i$ to allow for over-limit fees. (`lit_md/challenger.md:105`)
- The improvement is concentrated in the 25–60% utilization population, where a band-constant CCF cannot distinguish a transactor drifting into revolving behaviour from a stable low-utilization revolver. (`lit_md/challenger.md:117`)

### 4.4 Loss given default ↔ Loss severity

_relation: merge (moved) — score 0.9842_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>LGD is modelled as one minus the ultimate recovery rate, where recovery is nominal cash collected within 36 months of charge-off, inclusive of debt-sale proceeds net of agency commissions:<br><sub>lit_md/champion.md:140</sub></td><td>0.9966</td><td><table class="lc-nested"><caption>Table — severity by resolution channel, out-of-time charge-offs</caption><thead><tr><th>Channel</th><th>Share of charge-offs</th><th>Nominal recovery</th><th>Mean months to 80% of recovery</th><th>Discounted LGD</th></tr></thead><tbody><tr><td>Internal collections</td><td>34%</td><td>21.1%</td><td>9.4</td><td>0.812</td></tr><tr><td>Agency placement</td><td>41%</td><td>13.8%</td><td>17.2</td><td>0.881</td></tr><tr><td>Debt sale</td><td>19%</td><td>8.2%</td><td>1.0</td><td>0.919</td></tr><tr><td>Bankruptcy</td><td>6%</td><td>4.9%</td><td>22.6</td><td>0.960</td></tr><tr><td>**Weighted**</td><td>**100%**</td><td>**14.9%**</td><td>**13.1**</td><td>**0.879**</td></tr></tbody></table><br><sub>lit_md/challenger.md:132</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <strong>| Channel | Share of charge-offs | Nominal recovery | Mean months to 80% of recovery | Discounted</strong> LGD <del>is modelled as one minus the ultimate recovery rate, where recovery is nominal cash collected within 36 months of charge-off, inclusive of debt-sale proceeds net of agency commissions:</del> <strong>| |---|---|---|---|---| | Internal collections | 34% | 21.1% | 9.4 | 0.812 | | Agency placement | 41% | 13.8% | 17.2 | 0.881 | | Debt sale | 19% | 8.2% | 1.0 | 0.919 | | Bankruptcy | 6% | 4.9% | 22.6 | 0.960 | | </strong>Weighted<strong> | </strong>100%<strong> | </strong>14.9%<strong> | </strong>13.1<strong> | </strong>0.879<strong> |</strong></td></tr>
<tr><td colspan="3"><em>numeric changes:</em> 36 → 34%</td></tr>
<tr><td><code>R_i \in (0,1), \qquad R_i \sim \text{Beta}(\mu_i \phi, (1-\mu_i)\phi), \qquad \text{logit}(\mu_i) = \gamma_0 + \gamma_1 \, \text{chan}_i + \gamma_2 \ln EAD_i + \gamma_3 \, \text{bk}_i + \gamma_4 \, \text{stage}_i.</code><br><sub>lit_md/champion.md:142</sub></td><td>0.9186</td><td><code>LGD_i(m) = 1 - \sum_{k=1}^{36} w_{i,k} \, \hat{R}_i \, (1+r_i)^{-k/12},</code><br><sub>lit_md/challenger.md:128</sub></td></tr>
<tr><td>Covariates are the resolution channel (internal collections, agency placement, debt sale), log exposure at default, a bankruptcy flag, and the delinquency stage at charge-off. Recoveries are *not* discounted in the incumbent model; the nominal treatment is inherited from the pre-2015 regulatory reporting convention and is the subject of a standing finding (Section 7, item 3).<br><sub>lit_md/champion.md:144</sub></td><td>0.9634</td><td>**Total nominal recovery**, by beta regression on resolution channel, exposure, bankruptcy flag and refreshed bureau score at charge-off.<br><sub>lit_md/challenger.md:123</sub></td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- Segment LGD is the exposure-weighted mean of fitted account values. No macro conditioning is applied. (`lit_md/champion.md:146`)
_Challenger content in this section pair with no counterpart here:_
- Severity is built from a *recovery timing curve* rather than an ultimate recovery ratio. For each charged-off account, monthly collections are observed for up to 36 months. Two components are estimated: (`lit_md/challenger.md:121`)
- **Timing profile**, by a Dirichlet regression allocating total recovery across 36 monthly buckets, with the same covariates. (`lit_md/challenger.md:123`)
- Discounted severity is then (`lit_md/challenger.md:126`)
- with $w_{i,k}$ the fitted timing weights. Discounting at the account's effective interest rate rather than a portfolio rate is a deliberate choice: severity is used in pricing as well as in allowance, and a portfolio rate would cross-subsidize low-rate products. (`lit_md/challenger.md:130`)
- The 2.8 percentage point gap between nominal and discounted portfolio LGD is not a modelling refinement; it is a direct correction of an understatement in the incumbent, worth approximately 12 basis points of twelve-month loss rate and 26 basis points of lifetime loss rate. (`lit_md/challenger.md:142`)

### 4.5 Aggregation and stress overlay ↔ The factor-correlation problem

_relation: weak (moved) — score 0.9189_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>Portfolio loss rate is the balance-weighted aggregate of segment loss rates. Because the factors are estimated separately, the multiplicative form understates loss in stressed conditions, where PD, EAD and LGD deteriorate jointly. CLRM addresses this with an explicit overlay: under any scenario in which projected $\Delta u_t$ exceeds 200 basis points, segment LGD is increased by a scenario-specific additive factor $\lambda(\Delta u)$…<br><sub>lit_md/champion.md:150</sub></td><td>0.9836</td><td>The product $PD \times EAD \times LGD$ of separately estimated factor means is not the mean of the product. Under stress all three factors deteriorate together, and the product form understates loss. The incumbent handles this with a judgmental additive overlay applied when projected unemployment change exceeds 200 basis points. HELIX instead conditions all three factors on the same macroeconomic path, so that the co…<br><sub>lit_md/challenger.md:52</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>Portfolio loss rate</del> <strong>The product $PD \times EAD \times LGD$ of separately estimated factor means</strong> is <strong>not</strong> the <del>balance-weighted aggregate</del> <strong>mean</strong> of <del>segment loss rates. Because</del> the <strong>product. Under stress all three</strong> factors <del>are estimated separately,</del> <strong>deteriorate together, and</strong> the <del>multiplicative</del> <strong>product</strong> form understates <del>loss in stressed conditions, where PD, EAD and LGD deteriorate jointly. CLRM addresses</del> <strong>loss. The incumbent handles</strong> this with <del>an explicit overlay: under any scenario in which</del> <strong>a judgmental additive overlay applied when</strong> projected <del>$\Delta u_t$</del> <strong>unemployment change</strong> exceeds 200 basis <del>points, segment LGD</del> <strong>points. HELIX instead conditions all three factors on the same macroeconomic path, so that the covariance</strong> is <del>increased</del> <strong>generated</strong> by <del>a scenario-specific additive factor $\lambda(\Delta u)$ calibrated to</del> the <del>2009-2010 realized recovery shortfall, and CCF in the &gt;90% utilization band is raised by 4 percentage points. The overlay is documented as a</del> model <del>adjustment</del> rather than <del>as an estimated parameter and is re-approved annually.</del> <strong>supplied by committee.</strong></td></tr>
</tbody>
</table>


### 5.2 CCF estimates ↔ Exposure simulation

_relation: merge — score 0.948_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td><table class="lc-nested"><caption>Table 3. Estimated credit conversion factors by utilization band</caption><thead><tr><th>Utilization band</th><th>CCF</th><th>95% CI</th><th>Defaults in sample</th></tr></thead><tbody><tr><td>0–25%</td><td>0.184</td><td>[0.171, 0.197]</td><td>41,208</td></tr><tr><td>25–60%</td><td>0.327</td><td>[0.311, 0.343]</td><td>78,611</td></tr><tr><td>60–90%</td><td>0.541</td><td>[0.522, 0.560]</td><td>112,945</td></tr><tr><td>&gt;90%</td><td>0.806</td><td>[0.781, 0.831]</td><td>96,330</td></tr></tbody></table><br><sub>lit_md/champion.md:177</sub></td><td>0.985</td><td><table class="lc-nested"><caption>Table — exposure accuracy, out-of-time defaults</caption><thead><tr><th>Method</th><th>MAE (% of limit)</th><th>Bias (% of limit)</th><th>Correlation with realized EAD</th></tr></thead><tbody><tr><td>Fixed CCF by utilization band</td><td>7.9</td><td>−1.4</td><td>0.781</td></tr><tr><td>Fixed CCF by full segment cross</td><td>7.1</td><td>−1.1</td><td>0.804</td></tr><tr><td>HELIX simulated path</td><td>3.2</td><td>+0.3</td><td>0.918</td></tr></tbody></table><br><sub>lit_md/challenger.md:109</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> | <del>Utilization band</del> <strong>Method</strong> | <del>CCF</del> <strong>MAE (% of limit)</strong> | <del>95% CI</del> <strong>Bias (% of limit)</strong> | <del>Defaults in sample</del> <strong>Correlation with realized EAD</strong> | |---|---|---|---| | <del>0-25%</del> <strong>Fixed CCF by utilization band</strong> | <del>0.184</del> <strong>7.9</strong> | <del>[0.171, 0.197]</del> <strong>-1.4</strong> | <del>41,208</del> <strong>0.781</strong> | | <del>25-60%</del> <strong>Fixed CCF by full segment cross</strong> | <del>0.327</del> <strong>7.1</strong> | <del>[0.311, 0.343]</del> <strong>-1.1</strong> | <del>78,611</del> <strong>0.804</strong> | | <del>60-90%</del> <strong>HELIX simulated path</strong> | <del>0.541</del> <strong>3.2</strong> | <del>[0.522, 0.560]</del> <strong>+0.3</strong> | <del>112,945</del> <strong>0.918</strong> | <del>| &gt;90% | 0.806 | [0.781, 0.831] | 96,330 |</del></td></tr>
<tr><td colspan="3"><em>numeric changes:</em> 0.184 → 7.9, 41,208 → 0.781, 0.327 → 7.1, 78,611 → 0.804, 0.541 → 3.2, 112,945 → 0.918</td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- The monotone increase in CCF with utilization reproduces the run-up pattern of Ferreira-Lopes (2014). Note that the &gt;90% band CCF of 0.806 applies to a small remaining undrawn amount, so its contribution to portfolio EAD is modest despite the large coefficient. (`lit_md/champion.md:186`)
_Challenger content in this section pair with no counterpart here:_
- HELIX does not use a credit conversion factor. Instead the balance path is simulated forward from a two-part model: (`lit_md/challenger.md:101`)
- <code>\Delta B_i(m) = \underbrace{\pi_i(m) \cdot (L_i - B_i(m-1))}_{\text{purchase/drawdown}} - \underbrace{\rho_i(m) \cdot B_i(m-1)}_{\text{payment}},</code> (`lit_md/challenger.md:103`)
- where the drawdown intensity $\pi$ and the payment rate $\rho$ are each fitted by quantile regression forests on the same feature set as the hazard, then evaluated at the conditional median. Balances are floored at zero and capped at $1.05 L_i$ to allow for over-limit fees. (`lit_md/challenger.md:105`)
- Critically, $\pi$ and $\rho$ are fitted on the *pre-default* trajectory of accounts that subsequently defaulted as well as on survivors, with the default indicator excluded from the feature set to avoid look-ahead. The resulting paths reproduce the empirical run-up: simulated utilization rises from a median 0.63 twelve months before default to 0.97 in the default month, against observed 0.61 and 0.96. (`lit_md/challenger.md:107`)
- The improvement is concentrated in the 25–60% utilization population, where a band-constant CCF cannot distinguish a transactor drifting into revolving behaviour from a stable low-utilization revolver. (`lit_md/challenger.md:117`)

### 5.3 LGD estimates ↔ Loss severity

_relation: merge — score 0.9636_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td><table class="lc-nested"><caption>Table 4. Beta regression on ultimate recovery rate</caption><thead><tr><th>Variable</th><th>Coefficient</th><th>Std. error</th></tr></thead><tbody><tr><td>Intercept</td><td>−1.9104</td><td>0.0662</td></tr><tr><td>Agency placement (vs. internal)</td><td>−0.4188</td><td>0.0241</td></tr><tr><td>Debt sale (vs. internal)</td><td>−0.7733</td><td>0.0309</td></tr><tr><td>$\ln EAD$</td><td>−0.1526</td><td>0.0188</td></tr><tr><td>Bankruptcy flag</td><td>−0.9014</td><td>0.0455</td></tr><tr><td>Stage at charge-off (180+ vs. other)</td><td>−0.2107</td><td>0.0233</td></tr><tr><td>Precision $\phi$</td><td>4.81</td><td>0.09</td></tr></tbody></table><br><sub>lit_md/champion.md:190</sub></td><td>0.9816</td><td>**Total nominal recovery**, by beta regression on resolution channel, exposure, bankruptcy flag and refreshed bureau score at charge-off.<br><sub>lit_md/challenger.md:123</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>| Variable | Coefficient | Std. error | |---|---|---| | Intercept | -1.9104 | 0.0662 | | Agency placement (vs. internal) | -0.4188 | 0.0241 | | Debt sale (vs. internal) | -0.7733 | 0.0309 | | $\ln EAD$ | -0.1526 | 0.0188 | | Bankruptcy</del> <strong>**Total nominal recovery</strong>, by beta regression on resolution channel, exposure, bankruptcy<strong> flag ~~| -0.9014 | 0.0455 | | Stage~~ </strong>and refreshed bureau score<strong> at ~~charge-off (180+ vs. other) | -0.2107 | 0.0233 | | Precision $\phi$ | 4.81 | 0.09 |~~ </strong>charge-off.**</td></tr>
<tr><td>Implied portfolio LGD is 0.853, i.e. a mean ultimate recovery of 14.7 cents on the dollar. Bankruptcy charge-offs recover 5.1 cents; internally worked non-bankruptcy accounts recover 21.3 cents.<br><sub>lit_md/champion.md:202</sub></td><td>0.9892</td><td><table class="lc-nested"><caption>Table — severity by resolution channel, out-of-time charge-offs</caption><thead><tr><th>Channel</th><th>Share of charge-offs</th><th>Nominal recovery</th><th>Mean months to 80% of recovery</th><th>Discounted LGD</th></tr></thead><tbody><tr><td>Internal collections</td><td>34%</td><td>21.1%</td><td>9.4</td><td>0.812</td></tr><tr><td>Agency placement</td><td>41%</td><td>13.8%</td><td>17.2</td><td>0.881</td></tr><tr><td>Debt sale</td><td>19%</td><td>8.2%</td><td>1.0</td><td>0.919</td></tr><tr><td>Bankruptcy</td><td>6%</td><td>4.9%</td><td>22.6</td><td>0.960</td></tr><tr><td>**Weighted**</td><td>**100%**</td><td>**14.9%**</td><td>**13.1**</td><td>**0.879**</td></tr></tbody></table><br><sub>lit_md/challenger.md:132</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>Implied portfolio</del> <strong>| Channel | Share of charge-offs | Nominal recovery | Mean months to 80% of recovery | Discounted</strong> LGD <del>is 0.853, i.e. a mean ultimate recovery of 14.7 cents on the dollar.</del> <strong>| |---|---|---|---|---| | Internal collections | 34% | 21.1% | 9.4 | 0.812 | | Agency placement | 41% | 13.8% | 17.2 | 0.881 | | Debt sale | 19% | 8.2% | 1.0 | 0.919 | |</strong> Bankruptcy <del>charge-offs recover 5.1 cents; internally worked non-bankruptcy accounts recover 21.3 cents.</del> <strong>| 6% | 4.9% | 22.6 | 0.960 | | </strong>Weighted<strong> | </strong>100%<strong> | </strong>14.9%<strong> | </strong>13.1<strong> | </strong>0.879<strong> |</strong></td></tr>
<tr><td colspan="3"><em>numeric changes:</em> 0.853, → 34%, 14.7 → 21.1%, 5.1 → 6%, 21.3 → 4.9%</td></tr>
</tbody>
</table>

_Challenger content in this section pair with no counterpart here:_
- Severity is built from a *recovery timing curve* rather than an ultimate recovery ratio. For each charged-off account, monthly collections are observed for up to 36 months. Two components are estimated: (`lit_md/challenger.md:121`)
- **Timing profile**, by a Dirichlet regression allocating total recovery across 36 monthly buckets, with the same covariates. (`lit_md/challenger.md:123`)
- Discounted severity is then (`lit_md/challenger.md:126`)
- <code>LGD_i(m) = 1 - \sum_{k=1}^{36} w_{i,k} \, \hat{R}_i \, (1+r_i)^{-k/12},</code> (`lit_md/challenger.md:128`)
- with $w_{i,k}$ the fitted timing weights. Discounting at the account's effective interest rate rather than a portfolio rate is a deliberate choice: severity is used in pricing as well as in allowance, and a portfolio rate would cross-subsidize low-rate products. (`lit_md/challenger.md:130`)
- The 2.8 percentage point gap between nominal and discounted portfolio LGD is not a modelling refinement; it is a direct correction of an understatement in the incumbent, worth approximately 12 basis points of twelve-month loss rate and 26 basis points of lifetime loss rate. (`lit_md/challenger.md:142`)

### 6.2 Calibration and backtest ↔ Results

_relation: weak (moved) — score 0.9104_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td><table class="lc-nested"><caption>Table 6. Holdout backtest of annualized net loss rate</caption><thead><tr><th>Period</th><th>Predicted</th><th>Realized</th><th>Error (bps)</th></tr></thead><tbody><tr><td>2021</td><td>2.29%</td><td>2.11%</td><td>+18</td></tr><tr><td>2022</td><td>2.96%</td><td>3.08%</td><td>−12</td></tr><tr><td>2023</td><td>3.58%</td><td>3.41%</td><td>+17</td></tr><tr><td>Mean absolute error</td><td></td><td></td><td>14</td></tr></tbody></table><br><sub>lit_md/champion.md:230</sub></td><td>0.999</td><td><table class="lc-nested"><caption>Table — backtest of realized twelve-month losses, out-of-time</caption><thead><tr><th>Period</th><th>Incumbent predicted</th><th>HELIX predicted</th><th>Realized</th><th>HELIX error (bps)</th></tr></thead><tbody><tr><td>2022H1</td><td>2.81%</td><td>2.94%</td><td>3.02%</td><td>−8</td></tr><tr><td>2022H2</td><td>3.11%</td><td>3.19%</td><td>3.14%</td><td>+5</td></tr><tr><td>2023H1</td><td>3.44%</td><td>3.31%</td><td>3.28%</td><td>+3</td></tr><tr><td>2023H2</td><td>3.72%</td><td>3.57%</td><td>3.53%</td><td>+4</td></tr></tbody></table><br><sub>lit_md/challenger.md:174</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> | Period | <del>Predicted</del> <strong>Incumbent predicted | HELIX predicted</strong> | Realized | <del>Error</del> <strong>HELIX error</strong> (bps) | <del>|---|---|---|---|</del> <strong>|---|---|---|---|---|</strong> | <del>2021</del> <strong>2022H1</strong> | <del>2.29%</del> <strong>2.81%</strong> | <del>2.11%</del> <strong>2.94%</strong> | <del>+18</del> <strong>3.02% | -8</strong> | | <del>2022</del> <strong>2022H2</strong> | <del>2.96%</del> <strong>3.11%</strong> | <del>3.08%</del> <strong>3.19%</strong> | <del>-12</del> <strong>3.14% | +5</strong> | | <del>2023</del> <strong>2023H1</strong> | <del>3.58%</del> <strong>3.44%</strong> | <del>3.41%</del> <strong>3.31%</strong> | <del>+17</del> <strong>3.28% | +3</strong> | | <del>Mean absolute error</del> <strong>2023H2</strong> | <strong>3.72%</strong> | <strong>3.57%</strong> | <del>14</del> <strong>3.53%</strong> | <strong>+4 |</strong></td></tr>
<tr><td colspan="3"><em>numeric changes:</em> 2.29% → 2.81%, 2.11% → 2.94%, +18 → 3.02%, 2.96% → 3.11%, 3.08% → 3.19%, -12 → 3.14%, 3.58% → 3.44%, 3.41% → 3.31%, +17 → 3.28%, 14 → 3.53%</td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- A binomial test of predicted against realized default counts fails to reject calibration at the 5% level in 44 of 48 segments. The four failures are all in the &lt;620 score band, where the model over-predicts default — a pattern attributable to the 2021–2022 period of unusually strong consumer liquidity. (`lit_md/champion.md:239`)
_Challenger content in this section pair with no counterpart here:_
- <table class="lc-nested"><caption>Table — lifetime loss rate build-up, 2023Q4 book, baseline macro path</caption><thead><tr><th>Behavioural cohort</th><th>Balance share</th><th>12m loss rate</th><th>Lifetime loss rate</th><th>Mean behavioural life (months)</th></tr></thead><tbody><tr><td>Transactor</td><td>21.4%</td><td>0.61%</td><td>1.02%</td><td>14.1</td></tr><tr><td>Light revolver</td><td>28.9%</td><td>2.14%</td><td>4.77%</td><td>31.6</td></tr><tr><td>Heavy revolver</td><td>34.7%</td><td>5.38%</td><td>12.91%</td><td>34.8</td></tr><tr><td>Deteriorating</td><td>11.2%</td><td>13.92%</td><td>21.06%</td><td>18.3</td></tr><tr><td>Delinquent at reporting date</td><td>3.8%</td><td>42.71%</td><td>46.18%</td><td>9.2</td></tr><tr><td>**Portfolio**</td><td>**100%**</td><td>**4.11%**</td><td>**8.94%**</td><td>**27.4**</td></tr></tbody></table> (`lit_md/challenger.md:150`)
- Note that the behavioural cohorts above are a *reporting* view constructed after estimation for communication purposes; they are not an estimation unit. Nothing in HELIX is fitted at cohort level. (`lit_md/challenger.md:161`)
- <table class="lc-nested"><caption>Table — out-of-time discrimination, next-12-month default</caption><thead><tr><th>Model</th><th>AUC</th><th>Gini</th><th>KS</th></tr></thead><tbody><tr><td>Incumbent segment logit (reproduced on this panel)</td><td>0.803</td><td>0.606</td><td>0.443</td></tr><tr><td>HELIX hazard, monotone-constrained</td><td>0.847</td><td>0.694</td><td>0.521</td></tr><tr><td>HELIX hazard, unconstrained</td><td>0.851</td><td>0.702</td><td>0.527</td></tr><tr><td>HELIX hazard, no macro features</td><td>0.844</td><td>0.688</td><td>0.517</td></tr></tbody></table> (`lit_md/challenger.md:163`)
- Macro features contribute little to *ranking* — the relative ordering of accounts is nearly unchanged — but they carry nearly all of the *level* response across the 2020 stress period, which is the property that matters for scenario forecasting. (`lit_md/challenger.md:172`)

### 6.3 Independence-assumption bias ↔ The factor-correlation problem

_relation: merge (moved) — score 0.9418_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>To quantify the bias from factor separability, we computed the realized loss rate directly as $\sum D_i E_i (1-R_i) / \sum B_i$ and compared it to the product of realized factor means. The product form understates realized loss by 6 to 9 basis points in benign quarters and by 41 basis points in 2009Q4, the worst quarter in the sample. The stress overlay of Section 4.5 contributes 55 basis points at a 200 bps unemploy…<br><sub>lit_md/champion.md:243</sub></td><td>0.995</td><td>The product $PD \times EAD \times LGD$ of separately estimated factor means is not the mean of the product. Under stress all three factors deteriorate together, and the product form understates loss. The incumbent handles this with a judgmental additive overlay applied when projected unemployment change exceeds 200 basis points. HELIX instead conditions all three factors on the same macroeconomic path, so that the co…<br><sub>lit_md/challenger.md:52</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>To quantify</del> <strong>The product $PD \times EAD \times LGD$ of separately estimated factor means is not</strong> the <del>bias from factor separability, we computed</del> <strong>mean of</strong> the <del>realized loss rate directly as $\sum D_i E_i (1-R_i) / \sum B_i$</del> <strong>product. Under stress all three factors deteriorate together,</strong> and <del>compared it to</del> the <del>product of realized factor means. The</del> product form understates <del>realized loss</del> <strong>loss. The incumbent handles this with a judgmental additive overlay applied when projected unemployment change exceeds 200 basis points. HELIX instead conditions all three factors on the same macroeconomic path, so that the covariance is generated</strong> by <del>6 to 9 basis points in benign quarters and</del> <strong>the model rather than supplied</strong> by <del>41 basis points in 2009Q4, the worst quarter in the sample. The stress overlay of Section 4.5 contributes 55 basis points at a 200 bps unemployment shock, so the overlay is conservative relative to the measured bias at that severity. We have not tested severities beyond the 2009 experience.</del> <strong>committee.</strong></td></tr>
</tbody>
</table>


### 7. Limitations and Known Findings ↔ Executive Summary

_relation: split (moved) — score 0.971_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>**No lifetime horizon.** CLRM produces a twelve-month loss rate. Lifetime expected credit loss for accounting purposes is derived by applying an externally specified multiple to the twelve-month output. This is an acknowledged weakness and the primary driver of the challenger program.<br><sub>lit_md/champion.md:253</sub></td><td>0.9753</td><td>HELIX estimates credit card credit losses account by account and month by month over the full behavioural life of each account, rather than producing a single twelve-month loss rate for a risk segment. Loss is assembled as a discounted sum over monthly survival-weighted default events:<br><sub>lit_md/challenger.md:17</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>**No lifetime horizon.** CLRM produces</del> <strong>HELIX estimates credit card credit losses account by account and month by month over the full behavioural life of each account, rather than producing</strong> a <strong>single</strong> twelve-month loss <del>rate. Lifetime expected credit loss</del> <strong>rate</strong> for <del>accounting purposes</del> <strong>a risk segment. Loss</strong> is <del>derived by applying an externally specified multiple to the twelve-month output. This is an acknowledged weakness and the primary driver of the challenger program.</del> <strong>assembled as a discounted sum over monthly survival-weighted default events:</strong></td></tr>
<tr><td>**Segment drift.** Segment definitions are refit on a multi-year cycle. Between refits, population shift within bands is monitored but not corrected. The population stability index on the behaviour score distribution reached 0.14 in 2023Q4, above the 0.10 warning threshold.<br><sub>lit_md/champion.md:253</sub></td><td>0.8054</td><td>Monthly hazard estimated by gradient-boosted trees attains an out-of-time AUC of **0.847** on the next-12-month default indicator, against **0.803** for a reproduction of the incumbent segment logit on the same sample.<br><sub>lit_md/challenger.md:25</sub></td></tr>
<tr><td>**Undiscounted recoveries.** Nominal treatment of collections overstates recovery value and therefore understates LGD. At a 6% discount rate and the observed collection timing profile, discounted LGD would be approximately 0.878 rather than 0.853, raising portfolio loss rate by roughly 12 basis points.<br><sub>lit_md/champion.md:253</sub></td><td>0.9956</td><td>Severity is estimated as a *discounted* recovery curve. Discounting at the effective interest rate raises portfolio LGD from 0.851 (nominal) to **0.879**.<br><sub>lit_md/challenger.md:25</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>**Undiscounted recoveries.** Nominal treatment of collections overstates</del> <strong>Severity is estimated as a *discounted</strong>* recovery <del>value and therefore understates LGD. At a 6% discount</del> <strong>curve. Discounting at the effective interest</strong> rate <del>and the observed collection timing profile, discounted</del> <strong>raises portfolio</strong> LGD <del>would be approximately 0.878 rather than 0.853, raising portfolio loss rate by roughly 12 basis points.</del> <strong>from 0.851 (nominal) to </strong>0.879<strong>.</strong></td></tr>
<tr><td colspan="3"><em>numeric changes:</em> 0.878 → 0.851</td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- **CCF exclusion conservatism.** Excluding line-reduced accounts from CCF estimation is conservative in direction but of unquantified magnitude. (`lit_md/champion.md:253`)
- **Overlay rather than joint estimation.** Factor correlation is handled judgmentally. A jointly estimated alternative would be preferable if it could be made stable. (`lit_md/champion.md:253`)
_Challenger content in this section pair with no counterpart here:_
- <code>\text{Loss}_i = \sum_{m=1}^{M_i} S_i(m-1) \, h_i(m) \, \widehat{EAD}_i(m) \, \widehat{LGD}_i(m) \, (1+r)^{-m/12}.</code> (`lit_md/challenger.md:19`)
- The three factors are the same as in any expected-loss framework — a default probability, an exposure, and a loss severity — but each is a *function of account age and of a macroeconomic path* rather than a segment constant. (`lit_md/challenger.md:21`)
- Headline findings on the 2015–2023 panel: (`lit_md/challenger.md:23`)
- Lifetime loss rate for the 2023Q4 book is **8.94%** of outstanding balance at a 24-month behavioural life assumption, decomposing into 4.11% in the first twelve months and 4.83% thereafter. (`lit_md/challenger.md:25`)
- Exposure is simulated rather than scaled: the fitted balance path reproduces the observed pre-default run-up with a mean absolute error of 3.2% of limit, against 7.9% for a fixed credit conversion factor. (`lit_md/challenger.md:25`)
- Forecast volatility is materially higher: the month-over-month standard deviation of the portfolio lifetime loss rate is 31 basis points, against 9 basis points for the incumbent. (`lit_md/challenger.md:25`)
- The last bullet is the crux of the promotion decision and is treated at length in Part III. (`lit_md/challenger.md:31`)

### 7. Limitations and Known Findings ↔ The aggregation problem

_relation: split (moved) — score 0.971_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>**Segment drift.** Segment definitions are refit on a multi-year cycle. Between refits, population shift within bands is monitored but not corrected. The population stability index on the behaviour score distribution reached 0.14 in 2023Q4, above the 0.10 warning threshold.<br><sub>lit_md/champion.md:253</sub></td><td>0.9998</td><td>**Population shift is invisible.** When the composition of a segment drifts, a segment-constant PD is stale by construction. The incumbent's own documentation reports a population stability index of 0.14 on the score distribution, above its warning threshold, with no correction mechanism.<br><sub>lit_md/challenger.md:47</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>**Segment drift.** Segment definitions are refit on</del> <strong>**Population shift is invisible.</strong> When the composition of<strong> a ~~multi-year cycle. Between refits, population shift within bands~~ </strong>segment drifts, a segment-constant PD<strong> is ~~monitored but not corrected.~~ </strong>stale by construction.<strong> The </strong>incumbent's own documentation reports a<strong> population stability index </strong>of 0.14<strong> on the ~~behaviour~~ score ~~distribution reached 0.14 in 2023Q4,~~ </strong>distribution,<strong> above ~~the 0.10~~ </strong>its<strong> warning ~~threshold.~~ </strong>threshold, with no correction mechanism.**</td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- **No lifetime horizon.** CLRM produces a twelve-month loss rate. Lifetime expected credit loss for accounting purposes is derived by applying an externally specified multiple to the twelve-month output. This is an acknowledged weakness and the primary driver of the challenger program. (`lit_md/champion.md:253`)
- **Undiscounted recoveries.** Nominal treatment of collections overstates recovery value and therefore understates LGD. At a 6% discount rate and the observed collection timing profile, discounted LGD would be approximately 0.878 rather than 0.853, raising portfolio loss rate by roughly 12 basis points. (`lit_md/champion.md:253`)
- **CCF exclusion conservatism.** Excluding line-reduced accounts from CCF estimation is conservative in direction but of unquantified magnitude. (`lit_md/champion.md:253`)
- **Overlay rather than joint estimation.** Factor correlation is handled judgmentally. A jointly estimated alternative would be preferable if it could be made stable. (`lit_md/champion.md:253`)
_Challenger content in this section pair with no counterpart here:_
- Segment-level estimation is unbiased for the segment mean and biased for anything else. Two consequences matter in practice: (`lit_md/challenger.md:45`)
- **Within-segment heterogeneity is lost.** In the incumbent's 700–739 score band at 25–60% utilization, the account-level fitted twelve-month PD under HELIX ranges from 0.4% to 11.6% with an interquartile range of 1.9 percentage points. The incumbent assigns 2.84% to every account in the band. (`lit_md/challenger.md:47`)

### 7. Limitations and Known Findings ↔ Loss severity

_relation: split — score 0.9867_

<table class="lc-pair">
<thead><tr><th>Champion</th><th>sim</th><th>Challenger</th></tr></thead>
<tbody>
<tr><td>**Undiscounted recoveries.** Nominal treatment of collections overstates recovery value and therefore understates LGD. At a 6% discount rate and the observed collection timing profile, discounted LGD would be approximately 0.878 rather than 0.853, raising portfolio loss rate by roughly 12 basis points.<br><sub>lit_md/champion.md:253</sub></td><td>0.9952</td><td>The 2.8 percentage point gap between nominal and discounted portfolio LGD is not a modelling refinement; it is a direct correction of an understatement in the incumbent, worth approximately 12 basis points of twelve-month loss rate and 26 basis points of lifetime loss rate.<br><sub>lit_md/challenger.md:142</sub></td></tr>
<tr><td colspan="3"><em>diff:</em> <del>**Undiscounted recoveries.** Nominal treatment</del> <strong>The 2.8 percentage point gap between nominal and discounted portfolio LGD is not a modelling refinement; it is a direct correction</strong> of <del>collections overstates recovery value and therefore understates LGD. At a 6% discount</del> <strong>an understatement in the incumbent, worth approximately 12 basis points of twelve-month loss</strong> rate and <del>the observed collection timing profile, discounted LGD would be approximately 0.878 rather than 0.853, raising portfolio</del> <strong>26 basis points of lifetime</strong> loss <del>rate by roughly 12 basis points.</del> <strong>rate.</strong></td></tr>
<tr><td colspan="3"><em>numeric changes:</em> 6% → 12, 0.878 → 26</td></tr>
</tbody>
</table>

_Champion content in this section pair with no counterpart here (may be matched elsewhere — see coverage):_
- **No lifetime horizon.** CLRM produces a twelve-month loss rate. Lifetime expected credit loss for accounting purposes is derived by applying an externally specified multiple to the twelve-month output. This is an acknowledged weakness and the primary driver of the challenger program. (`lit_md/champion.md:253`)
- **Segment drift.** Segment definitions are refit on a multi-year cycle. Between refits, population shift within bands is monitored but not corrected. The population stability index on the behaviour score distribution reached 0.14 in 2023Q4, above the 0.10 warning threshold. (`lit_md/champion.md:253`)
- **CCF exclusion conservatism.** Excluding line-reduced accounts from CCF estimation is conservative in direction but of unquantified magnitude. (`lit_md/champion.md:253`)
- **Overlay rather than joint estimation.** Factor correlation is handled judgmentally. A jointly estimated alternative would be preferable if it could be made stable. (`lit_md/champion.md:253`)
_Challenger content in this section pair with no counterpart here:_
- Severity is built from a *recovery timing curve* rather than an ultimate recovery ratio. For each charged-off account, monthly collections are observed for up to 36 months. Two components are estimated: (`lit_md/challenger.md:121`)
- **Total nominal recovery**, by beta regression on resolution channel, exposure, bankruptcy flag and refreshed bureau score at charge-off. (`lit_md/challenger.md:123`)
- **Timing profile**, by a Dirichlet regression allocating total recovery across 36 monthly buckets, with the same covariates. (`lit_md/challenger.md:123`)
- Discounted severity is then (`lit_md/challenger.md:126`)
- <code>LGD_i(m) = 1 - \sum_{k=1}^{36} w_{i,k} \, \hat{R}_i \, (1+r_i)^{-k/12},</code> (`lit_md/challenger.md:128`)
- with $w_{i,k}$ the fitted timing weights. Discounting at the account's effective interest rate rather than a portfolio rate is a deliberate choice: severity is used in pricing as well as in allowance, and a portfolio rate would cross-subsidize low-rate products. (`lit_md/challenger.md:130`)
- <table class="lc-nested"><caption>Table — severity by resolution channel, out-of-time charge-offs</caption><thead><tr><th>Channel</th><th>Share of charge-offs</th><th>Nominal recovery</th><th>Mean months to 80% of recovery</th><th>Discounted LGD</th></tr></thead><tbody><tr><td>Internal collections</td><td>34%</td><td>21.1%</td><td>9.4</td><td>0.812</td></tr><tr><td>Agency placement</td><td>41%</td><td>13.8%</td><td>17.2</td><td>0.881</td></tr><tr><td>Debt sale</td><td>19%</td><td>8.2%</td><td>1.0</td><td>0.919</td></tr><tr><td>Bankruptcy</td><td>6%</td><td>4.9%</td><td>22.6</td><td>0.960</td></tr><tr><td>**Weighted**</td><td>**100%**</td><td>**14.9%**</td><td>**13.1**</td><td>**0.879**</td></tr></tbody></table> (`lit_md/challenger.md:132`)


## Only in champion

| Heading | Size (chars) | Best match anywhere | Excerpt |
|---|---|---|---|
| 2. Related Work (`lit_md/champion.md:43`) | 2259 | 0.9504 | Three strands of work bear on the specification choices made here. |
| 3.1 Portfolio description (`lit_md/champion.md:59`) | 619 | 0.7772 | The estimation sample is the general-purpose credit card book of Meridian Bancorp, excluding the private-label co-brand partnerships (which are modelled separately) and excluding small-business cards. Table 1 summarizes the portfolio as of the final estimation quarter. |
| 3.2 Segmentation scheme (`lit_md/champion.md:76`) | 666 | 0.8293 | CLRM partitions the portfolio into 48 segments formed by the cross of: |
| 5.1 PD estimates (`lit_md/champion.md:156`) | 1055 | 0.8632 | \| Variable \| Coefficient \| Std. error \| t-stat \|<br>\|---\|---\|---\|---\|<br>\| $\Delta u_t$ (unemployment change) \| 0.1842 \| 0.0211 \| 8.73 \|<br>\| $hpi_t$ (log HPI change) \| −1.0937 \| 0.2604 \| −4.20 \|<br>\| $dsr_t$ (debt service ratio) \| 0.2715 \| 0.0893 \| 3.04 \|<br>\| $pay_{s,t}$ (payment rate) \| −3.4021 \| 0.4118 \| −8.26 \|<br>\| $\Delta util_{s,t}$ (utilization change) \| 2.1166 \| 0.3072 \| 6.89 \|<br>\| Segment fixed effects \| 48 estimated \| — \| —… |
| 5.4 Assembled loss rate (`lit_md/champion.md:204`) | 717 | 0.8971 | \| Score band \| Balance share \| PD \| EAD/Balance \| LGD \| Loss rate \|<br>\|---\|---\|---\|---\|---\|---\|<br>\| &lt;620 \| 8.1% \| 14.82% \| 1.12 \| 0.871 \| 14.46% \|<br>\| 620–659 \| 11.4% \| 8.91% \| 1.14 \| 0.866 \| 8.80% \|<br>\| 660–699 \| 17.9% \| 5.27% \| 1.17 \| 0.858 \| 5.29% \|<br>\| 700–739 \| 22.6% \| 2.84% \| 1.21 \| 0.850 \| 2.92% \|<br>\| 740–779 \| 20.8% \| 1.33% \| 1.26 \| 0.844 \| 1.41% \|<br>\| 780+ \| 19.2% \| 0.51% \| 1.34 \| 0.836 \| 0.57% \|<br>\| **Portfolio** \| **100%**… |
| 6.1 Discriminatory power (`lit_md/champion.md:224`) | 259 | 0.7155 | On the 2021Q1–2023Q4 holdout, the segment-level PD ranking achieves a Gini coefficient of 0.601 (development: 0.612) and a Kolmogorov–Smirnov statistic of 0.442. Degradation of 1.1 Gini points is within the 5-point tolerance in the bank's validation standard. |
| 6.4 Sensitivity (`lit_md/champion.md:245`) | 248 | 0.655 | A ±10% relative shock to each factor produces the following loss-rate elasticities: PD 1.00, CCF 0.18, LGD 1.00. Loss rate is thus far more sensitive to PD and LGD than to the exposure factor, which supports the decision not to macro-condition CCF. |
| 8. Conclusion (`lit_md/champion.md:261`) | 633 | 0.9382 | CLRM v4.2 delivers a twelve-month credit card loss rate that is accurate to within 20 basis points on holdout, decomposable into factors that line-of-business owners can interrogate, and stable enough to be used in allowance and capital planning without month-over-month reconciliation burden. Its principal weaknesses are its fixed twelve-month horizon, its reliance on judgmental overlays for factor correlation, and i… |
| Appendix A. Delinquent-Account Roll-Rate Treatment (`lit_md/champion.md:289`) | 644 | 0.7954 | Accounts 30 or more days past due at cohort origin are excluded from the logistic PD regression and assigned a PD from an empirical roll-rate matrix estimated on trailing eight quarters. The matrix gives the probability of migrating from each delinquency bucket to charge-off within twelve months: |
| Appendix B. Variable Dictionary (`lit_md/champion.md:303`) | 559 | 0.8922 | \| Field \| Definition \|<br>\|---\|---\|<br>\| Beginning balance $B_i$ \| Statement balance at cohort origin, excluding accrued unbilled interest \|<br>\| Committed line $L_i$ \| Contractual credit limit at cohort origin \|<br>\| Payment rate \| Trailing three-month mean of payments received divided by beginning balance \|<br>\| Utilization \| Beginning balance divided by committed line, capped at 1.50 \|<br>\| Behaviour score \| Internal score, refresh… |
| 3. Data (`lit_md/champion.md:57`) | 1959 | 0.7324 | The estimation sample is the general-purpose credit card book of Meridian Bancorp, excluding the private-label co-brand partnerships (which are modelled separately) and excluding small-business cards. Table 1 summarizes the portfolio as of the final estimation quarter. |
| 4. Methodology (`lit_md/champion.md:94`) | 4951 | 0.7447 | Let $s$ index segments and $t$ index quarterly cohorts. Define the twelve-month loss rate for segment $s$ in cohort $t$ as the ratio of realized net credit losses to the beginning balance: |
| 5. Model Estimation Results (`lit_md/champion.md:154`) | 2835 | 0.6977 | \| Variable \| Coefficient \| Std. error \| t-stat \|<br>\|---\|---\|---\|---\|<br>\| $\Delta u_t$ (unemployment change) \| 0.1842 \| 0.0211 \| 8.73 \|<br>\| $hpi_t$ (log HPI change) \| −1.0937 \| 0.2604 \| −4.20 \|<br>\| $dsr_t$ (debt service ratio) \| 0.2715 \| 0.0893 \| 3.04 \|<br>\| $pay_{s,t}$ (payment rate) \| −3.4021 \| 0.4118 \| −8.26 \|<br>\| $\Delta util_{s,t}$ (utilization change) \| 2.1166 \| 0.3072 \| 6.89 \|<br>\| Segment fixed effects \| 48 estimated \| — \| —… |
| 6. Validation (`lit_md/champion.md:222`) | 1569 | 0.7084 | On the 2021Q1–2023Q4 holdout, the segment-level PD ranking achieves a Gini coefficient of 0.601 (development: 0.612) and a Kolmogorov–Smirnov statistic of 0.442. Degradation of 1.1 Gini points is within the 5-point tolerance in the bank's validation standard. |

## Only in challenger

| Heading | Size (chars) | Best match anywhere | Excerpt |
|---|---|---|---|
| Notation and assembly (`lit_md/challenger.md:62`) | 748 | 0.8984 | For account $i$ at months-on-book $m$ under macro path $\mathcal{M}$: |
| Behavioural life (`lit_md/challenger.md:144`) | 606 | 0.6283 | A revolving account has no maturity, so the lifetime sum requires a horizon. HELIX sets $M_i$ endogenously as the month at which cumulative survival $S_i(m)$ falls below 0.05, capped at 120 months. Attrition hazard $a_i(m)$ is estimated by an analogous boosted model on the voluntary-closure indicator. The resulting balance-weighted mean behavioural life is 27.4 months, against the incumbent's implied 26.2 months (fro… |
| Where HELIX is worse than the incumbent (`lit_md/challenger.md:187`) | 1402 | 0.8498 | We state these plainly, because the validation decision should not turn on discovering them later. |
| Where the incumbent is not salvageable (`lit_md/challenger.md:197`) | 265 | 0.6144 | Against the above, three incumbent weaknesses cannot be fixed within its framework: the lifetime scalar, the absence of any within-segment differentiation, and the judgmental factor-correlation overlay. Each of these is a specification limit, not a calibration gap. |
| Recommendation (`lit_md/challenger.md:201`) | 479 | 0.6961 | We recommend HELIX be run in parallel for four consecutive quarters with monthly reporting of (a) portfolio lifetime and twelve-month loss rates against the incumbent, (b) the volatility decomposition of Part III item 1, and (c) segment-level reconciliation to the incumbent using the reporting view of Part II. We do not recommend promotion in this cycle. The volatility finding is real and unresolved, and we would rat… |
| Required controls if promoted (`lit_md/challenger.md:205`) | 513 | 0.6622 | \| Control \| Frequency \| Threshold \|<br>\|---\|---\|---\|<br>\| Feature drift (PSI, each of 44 features) \| Monthly \| 0.10 warn / 0.25 breach \|<br>\| Hazard calibration by decile \| Monthly \| Hosmer–Lemeshow p &gt; 0.01 \|<br>\| Exposure path backtest against realized EAD \| Quarterly \| MAE &lt; 5% of limit \|<br>\| Recovery timing curve refit \| Annual \| — \|<br>\| Monotonic constraint audit \| Each refit \| All 8 constraints present \|<br>\| Macro-path reconcili… |
| Annex 1 · Data lineage (`lit_md/challenger.md:241`) | 884 | 0.6755 | \| Feed \| Source system \| Grain \| History available \| New for HELIX \|<br>\|---\|---\|---\|---\|---\|<br>\| Account master \| CARDCORE \| Account-month \| 2011-01 \| No \|<br>\| Statement and payment detail \| CARDCORE \| Account-month \| 2013-06 \| No \|<br>\| Collections detail \| RECOVER2 \| Account-month-agency \| 2015-01 \| Yes \|<br>\| Bureau refresh \| Vendor tape \| Account-month \| 2015-01 \| Yes \|<br>\| Promotional balances \| PROMOTAPE \| Account-month \| 20… |
| Annex 2 · Reconciliation to the incumbent (`lit_md/challenger.md:254`) | 696 | 0.9358 | Decomposition of the difference between the incumbent's twelve-month portfolio loss rate (4.07%) and HELIX's (4.11%): |
| Annex 3 · Reproducibility (`lit_md/challenger.md:270`) | 289 | 0.379 | All results in this paper are produced by pipeline `helix-rc3`, commit tag `rc3-final`, against snapshot `panel_2015_2023_v7`. Random seeds are fixed at 20240917 for all stochastic components. Re-running the pipeline end to end reproduces every figure in Part II to the reported precision. |
| Part I — Why a Lifetime Account-Level Framework (`lit_md/challenger.md:35`) | 2318 | 0.7535 | A twelve-month loss rate answers a question that neither the accounting standard nor the pricing desk actually asks. Accounting requires expected credit losses over the expected life of the exposure; pricing requires the net present value of a relationship. The incumbent framework answers both by multiplying a twelve-month number by a judgmental lifetime factor, currently 2.18. That factor is a single scalar applied… |
| Part II — The Framework (`lit_md/challenger.md:60`) | 7702 | 0.7493 | For account $i$ at months-on-book $m$ under macro path $\mathcal{M}$: |
| Part III — Governance, Weaknesses and the Promotion Question (`lit_md/challenger.md:185`) | 2659 | 0.6479 | We state these plainly, because the validation decision should not turn on discovering them later. |
| Annexes (`lit_md/challenger.md:239`) | 1869 | 0.6441 | \| Feed \| Source system \| Grain \| History available \| New for HELIX \|<br>\|---\|---\|---\|---\|---\|<br>\| Account master \| CARDCORE \| Account-month \| 2011-01 \| No \|<br>\| Statement and payment detail \| CARDCORE \| Account-month \| 2013-06 \| No \|<br>\| Collections detail \| RECOVER2 \| Account-month-agency \| 2015-01 \| Yes \|<br>\| Bureau refresh \| Vendor tape \| Account-month \| 2015-01 \| Yes \|<br>\| Promotional balances \| PROMOTAPE \| Account-month \| 20… |

## Numeral cross-index

225 numerals extracted from champion, 162 from challenger.

### Agreements

| Quantity | Champion | Challenger | Δ | Evidence |
|---|---|---|---|---|
| above distribution index population score stability | 0.14 (`7. Limitations and Known Findings`) | 0.14 (`The aggregation problem`) | 0.0 | 24.14 |
| exceeds overlay projected | 200 bps (`4.5 Aggregation and stress overlay`) | 200 bps (`The factor-correlation problem`) | 0.0 | 13.8 |
| balance baseline build-up loss portfolio rate | 100% (`5.4 Assembled loss rate`) | 100% (`Results`) | 0.0 | 12.58 |
| bankruptcy due past | 180 day (`3.3 Default definition`) | 180 day (`Box 1 — What HELIX does not change`) | 0.0 | 10.54 |
| approximately lgd loss portfolio rate | 12 bps (`7. Limitations and Known Findings`) | 12 bps (`Loss severity`) | 0.0 | 10.29 |
| discounted lgd portfolio rate | 0.853 (`7. Limitations and Known Findings`) | 0.851 (`Executive Summary`) | 0.00234 | 7.87 |
| overlay unemployment | 200 bps (`6.3 Independence-assumption bias`) | 200 bps (`The factor-correlation problem`) | 0.0 | 7.43 |
| month rate recovery | 36 (`2. Related Work`) | 36 (`Box 1 — What HELIX does not change`) | 0.0 | 6.21 |
| backtest predicted table | 3.58% (`6.2 Calibration and backtest`) | 3.57% (`Results`) | 0.00279 | 6.15 |
| discounted lgd | 0.878 (`7. Limitations and Known Findings`) | 0.879 (`Loss severity`) | 0.00114 | 5.67 |
| band score utilization | 700 (`3.2 Segmentation scheme`) | 700 (`The aggregation problem`) | 0.0 | 4.84 |
| lgd portfolio rate | 0.851 (`5.4 Assembled loss rate`) | 0.851 (`Executive Summary`) | 0.0 | 4.73 |
| lgd portfolio rate | 0.878 (`7. Limitations and Known Findings`) | 0.879 (`Executive Summary`) | 0.00114 | 4.73 |
| recovery ultimate | 36 month (`4.4 Loss given default`) | 36 month (`Loss severity`) | 0.0 | 4.65 |
| recovery ultimate | 36 month (`Appendix B. Variable Dictionary`) | 36 month (`Loss severity`) | 0.0 | 4.65 |
| against realized | 5% (`6.2 Calibration and backtest`) | 5% (`Required controls if promoted`) | 0.0 | 4.63 |
| basis loss | 9 bps (`6.3 Independence-assumption bias`) | 9 bps (`Executive Summary`) | 0.0 | 4.54 |
| lgd portfolio | 0.853 (`5.3 LGD estimates`) | 0.851 (`Executive Summary`) | 0.00234 | 3.81 |
| ccf table | 0.806 (`5.2 CCF estimates`) | 0.804 (`Exposure simulation`) | 0.00248 | 3.55 |
| loss portfolio rate | 4.07% (`5.4 Assembled loss rate`) | 4.07% (`Annex 2 · Reconciliation to the incumbent`) | 0.0 | 3.45 |
| loss portfolio rate | 8.91% (`5.4 Assembled loss rate`) | 8.94% (`Where HELIX is worse than the incumbent`) | 0.00336 | 3.45 |
| band score | 700 (`5.4 Assembled loss rate`) | 700 (`The aggregation problem`) | 0.0 | 3.38 |
| share table | 100% (`5.4 Assembled loss rate`) | 100% (`Loss severity`) | 0.0 | 3.22 |
| band utilization | 25 (`5.2 CCF estimates`) | 25 (`The aggregation problem`) | 0.0 | 2.89 |
| loss rate | 8.91% (`5.4 Assembled loss rate`) | 8.94% (`Executive Summary`) | 0.00336 | 2.16 |

### Disagreements

| Quantity | Champion | Challenger | Δ | Evidence |
|---|---|---|---|---|
| above distribution index population score stability | 0.10 (`7. Limitations and Known Findings`) | 0.14 (`The aggregation problem`) | 0.28571 | 24.14 |
| balance baseline build-up loss rate share | 11.4% (`5.4 Assembled loss rate`) | 11.2% (`Results`) | 0.01754 | 11.29 |
| months rises run-up utilization | 0.95 (`2. Related Work`) | 0.97 (`Exposure simulation`) | 0.02062 | 10.82 |
| absolute error reproduces | 3.41% (`Abstract`) | 3.2% (`Executive Summary`) | 0.06158 | 10.48 |
| basis loss points | 41 bps (`6.3 Independence-assumption bias`) | 31 bps (`Executive Summary`) | 0.2439 | 7.87 |
| basis loss points | 41 bps (`6.3 Independence-assumption bias`) | 26 bps (`Loss severity`) | 0.36585 | 7.87 |
| discounted lgd portfolio rate | 0.878 (`7. Limitations and Known Findings`) | 0.851 (`Executive Summary`) | 0.03075 | 7.87 |
| baseline build-up loss portfolio rate table | 4.07% (`5.4 Assembled loss rate`) | 4.11% (`Results`) | 0.00973 | 7.29 |
| basis points | 55 bps (`6.3 Independence-assumption bias`) | 31 bps (`Executive Summary`) | 0.43636 | 6.63 |
| band ccf table utilization | 0.806 (`5.2 CCF estimates`) | 0.781 (`Exposure simulation`) | 0.03102 | 6.44 |
| backtest predicted table | 2.96% (`6.2 Calibration and backtest`) | 2.94% (`Results`) | 0.00676 | 6.15 |
| baseline build-up loss rate table | 5.29% (`5.4 Assembled loss rate`) | 5.38% (`Results`) | 0.01673 | 6.0 |
| ccf ead | 0.90 (`Appendix A. Delinquent-Account Roll-Rate Treatment`) | 0.804 (`Exposure simulation`) | 0.10667 | 5.86 |
| band ccf utilization | 0.806 (`5.2 CCF estimates`) | 0.781 (`Exposure simulation`) | 0.03102 | 5.82 |
| discounted lgd | 0.853 (`7. Limitations and Known Findings`) | 0.879 (`Loss severity`) | 0.02958 | 5.67 |
| months rises | 0.95 (`2. Related Work`) | 0.96 (`Exposure simulation`) | 0.01042 | 5.65 |
| backtest realized table | 3.08% (`6.2 Calibration and backtest`) | 3.14% (`Results`) | 0.01911 | 5.46 |
| predicted realized | 5% (`6.2 Calibration and backtest`) | 3.72% (`Results`) | 0.256 | 5.32 |
| nominal recovery | 6% (`7. Limitations and Known Findings`) | 4.9% (`Loss severity`) | 0.18333 | 5.29 |
| default gini | 0.612 (`Abstract`) | 0.606 (`Results`) | 0.0098 | 5.26 |
| run-up utilization | 0.806 (`5.2 CCF estimates`) | 0.97 (`Exposure simulation`) | 0.16907 | 5.17 |
| loss mean rate table | 14 (`6.2 Calibration and backtest`) | 14.1 (`Results`) | 0.00709 | 5.16 |
| balance loss rate | 8.1% (`5.4 Assembled loss rate`) | 8.94% (`Executive Summary`) | 0.09396 | 4.85 |
| band score utilization | 779 (`3.2 Segmentation scheme`) | 739 (`The aggregation problem`) | 0.05135 | 4.84 |
| backtest realized | 3.41% (`6.2 Calibration and backtest`) | 5% (`Required controls if promoted`) | 0.318 | 4.84 |
| lgd portfolio rate | 0.858 (`5.4 Assembled loss rate`) | 0.851 (`Executive Summary`) | 0.00816 | 4.73 |
| lgd portfolio rate | 0.853 (`7. Limitations and Known Findings`) | 0.879 (`Executive Summary`) | 0.02958 | 4.73 |
| basis rate | 8.4% (`3.3 Default definition`) | 8.94% (`Where HELIX is worse than the incumbent`) | 0.0604 | 4.21 |
| loss rate twelve-month | 20 bps (`8. Conclusion`) | 26 bps (`Loss severity`) | 0.23077 | 4.15 |
| month rate | 36 (`2. Related Work`) | 24 (`Executive Summary`) | 0.33333 | 3.92 |

### Champion internal inconsistencies

| Quantity | A | B | Δ |
|---|---|---|---|
| achieves coefficient gini segment-level | 0.612 (`Abstract`) | 0.601 (`6.1 Discriminatory power`) | 0.01797 |
| error std. | 0.0893 (`5.1 PD estimates`) | 0.09 (`5.3 LGD estimates`) | 0.00778 |
| lgd | 0.851 (`5.4 Assembled loss rate`) | 0.853 (`7. Limitations and Known Findings`) | 0.00234 |
| gini holdout | 0.598 (`5.1 PD estimates`) | 0.601 (`6.1 Discriminatory power`) | 0.00499 |
| behaviour score | 712 (`3.1 Portfolio description`) | 700 (`3.2 Segmentation scheme`) | 0.01685 |
| score | 712 (`3.1 Portfolio description`) | 700 (`5.4 Assembled loss rate`) | 0.01685 |
| lgd | 0.853 (`5.3 LGD estimates`) | 0.851 (`5.4 Assembled loss rate`) | 0.00234 |
| score | 779 (`3.2 Segmentation scheme`) | 780 (`5.4 Assembled loss rate`) | 0.00128 |
### Challenger internal inconsistencies

| Quantity | A | B | Δ |
|---|---|---|---|
| auc default hazard | 0.847 (`Executive Summary`) | 0.844 (`Results`) | 0.00354 |
| portfolio | 4.11% (`Results`) | 4.07% (`Annex 2 · Reconciliation to the incumbent`) | 0.00973 |
| segment | 0.804 (`Exposure simulation`) | 0.803 (`Results`) | 0.00124 |
| segment | 0.803 (`Executive Summary`) | 0.804 (`Exposure simulation`) | 0.00124 |
| twelve-month | 2.84% (`The aggregation problem`) | 2.81% (`Results`) | 0.01056 |

## Citation overlap

9 champion citations, 8 challenger citations, Jaccard 0.1333.

**Shared (2):**
- kessler:2020 — Kessler, M., Duan, Y., and Rahimi, S. (2020). Gradient boosting versus scorecards for card default: accuracy, stability and governance. *Journal of Applied Credit Analytics*, 12(4), 415-448.
- nwosu:2019 — Nwosu, C. (2019). Discounting post-default collections in unsecured retail portfolios. *Journal of Credit Risk Modelling*, 15(1), 1-24.

**Champion-only (7):**
- Altman, E. (1968). Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. *Journal of Finance*, 23(4), 589-609.
- Brakefield, D., and Sotomayor, L. (2013). Beta regression for recovery rates on charged-off unsecured consumer debt. *Journal of Credit Risk Modelling*, 9(2), 33-61.
- Delacroix, H., and Whitmore, J. (2011). Behavioural predictors of revolving credit default at short horizons. *Review of Retail Finance*, 14(3), 201-229.
- Ferreira-Lopes, A. (2014). Exposure run-up on committed revolving retail lines. *Quantitative Banking Studies*, 6(1), 77-104.
- Marchetti, G. (2016). Aggregation loss in segment-level retail credit scoring. *European Journal of Risk Measurement*, 19(2), 155-180.
- Thomas, L. (2000). A survey of credit and behavioural scoring. *International Journal of Forecasting*, 16(2), 149-172.
- Zhou, K., and Aaltonen, R. (2009). Credit conversion factors for committed corporate facilities. *Banking and Capital Review*, 4(2), 121-149.

**Challenger-only (6):**
- Aziz, N., and Lindqvist, P. (2018). *Discrete-time survival models for revolving consumer credit.* Nordic Journal of Financial Econometrics, 7(2), 88-119.
- Cerqueira, T., and Wasserman, H. (2021). *Gradient boosting under monotonic constraints for regulated credit models.* Journal of Applied Credit Analytics, 13(1), 52-79.
- Hosmer, D., and Lemeshow, S. (1980). Goodness of fit tests for the multiple logistic regression model. *Communications in Statistics*, 9(10), 1043-1069.
- Ostrowska, J., Baptiste, R., and Kuroda, M. (2022). *Simulated exposure paths versus credit conversion factors for committed retail lines.* Quantitative Banking Studies, 14(3), 233-268.
- Sengupta, A. (2017). Dirichlet regression for recovery cash-flow timing. *Review of Credit Portfolio Management*, 11(4), 301-327.
- Van Der Meulen, B. (2015). Behavioural life estimation for open-ended consumer facilities. *European Journal of Risk Measurement*, 18(1), 44-72.

## Terminology diff

**Champion-only terms:** t, variable, std, stage, clrm, origin, measure, ead/balance, segments, e, treatment, line, field, beginning, commitments, dpd, 2, committed, symbol, t-stat, uses, holdout, logistic, contractual, 48
**Challenger-only terms:** helix, m, path, life, month, features, up, new, control, auc, frequency, effect, object, meaning, two, them, later, k, history, grain, findings, family, headline, feed, state
## Table pairs

### `left:s021:b01` ↔ `right:s014:b07`

score 0.4952, header jaccard 0.7143, confidence 0.0
_declined: row labels do not align (positional diffing would invent changes)_
### `left:s018:b01` ↔ `right:s014:b01`

score 0.3346, header jaccard 0.25, confidence 0.1667
_declined: row labels do not align (positional diffing would invent changes)_

