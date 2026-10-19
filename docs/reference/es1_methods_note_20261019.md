# ES-1 Methods Note (non-authoritative)

Status: **REFERENCE — GOVERNS NOTHING.** Illustrates methods that could
satisfy the requirements of
[PD-005 (ES-1, proposed)](../decisions/principal_decision_005_es1_evaluation_standard.md).
None is constitutional; each is replaceable by declaration under R-10.
This note is corrected to match the doctrine, never the reverse.

| Requirement | Candidate methods | What each cannot estimate |
| --- | --- | --- |
| R-3 effective observations | Cluster scored events by shared shock (same market move within the horizon), by overlapping horizons, and by common exposure; count clusters, or compute an effective sample size from the autocorrelation of the scored series and from a dependence-preserving block bootstrap | Dependence through channels not in the declared closure; the cluster boundary is a judgment and is declared |
| R-4 multiplicity | Deflated performance expectations for the best of `T_total` dependent trials (correlation among variants estimated from their Historical Reconstruction series); a Bayesian family prior shrinking each variant toward the family mean; a holdout that was never searched, labelled Historical Reconstruction | Trials never recorded; the method assumes the family is complete, which R-4's reconciliation checks but cannot prove |
| R-5 payoff and downside | Bayesian updating with a declared prior on the scored quantity; posterior predictive intervals; empirical quantiles, worst-`k`, expected shortfall at declared levels; peaks-over-threshold with a stated threshold and exponent interval where the sample allows, reported with the interval and a refusal when it does not; Monte Carlo by block bootstrap or by a declared dependence structure | Tails beyond the sample; a stable tail exponent from a short record; parameter stability across regimes |
| R-6 stress | Historical analogue windows replayed on the subject's declared rules; synthetic liquidity shocks (spread and depth multipliers, exit horizon); discontinuities at declared, unfitted multiples; joint scenarios over the population's declared exposures | Events with no analogue; the correct multiplier; the population's hidden common exposures |
| R-7 contribution | Correlation of decision-implied series; shared instruments and factor loadings; co-loss under the stress set; marginal change in portfolio drawdown and tail loss at the proposed size | Latent crowding outside the population (other market participants) |
| R-8 change | Posterior predictive checks of the realized series against the committed predictive distribution; sequential tests with declared levels; conformal intervals for distribution-free coverage; a surprise statistic for single outcomes against the committed tail bound | Whether a departure is decay or an ordinary draw; the method flags, the Principal decides |
| Agent Design contribution | Forward-resolved research per unit consumed; estimate error of `SELECTION` records; coverage against cadence; later fate of rejected candidates | The value of research that prevented a bad decision no one proposed |

Illustrative calibration of §8 case A: for 1,000 variants with average
pairwise correlation 0.6 over 120 months, the expected maximum Sharpe
under no edge is about 1.4 by the deflated-Sharpe calculation; the
figure is an illustration of the method, not a constant of ES-1.
