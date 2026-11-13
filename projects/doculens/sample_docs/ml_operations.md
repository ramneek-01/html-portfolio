# ML Operations Notes

Machine learning systems require ongoing monitoring after deployment. Data drift occurs when the distribution of incoming features changes over time. Concept drift occurs when the relationship between features and the target changes. A monitoring workflow should track input quality, missing values, prediction distributions, latency, and delayed ground-truth metrics. Alerts should have an owner and a documented response procedure.

A model evaluation report should record the dataset window, split strategy, baseline, chosen metrics, and known limitations. Time-dependent data should use chronological evaluation rather than random shuffling.
