# Logging

You will usually want to log which units (e.g., users) are exposed to your experiment.

Logging this information enables monitoring your experiment and improving your analysis of the results. In particular, many experiments might only change your service for a very small portion of users; keeping track of these users will make your analysis more precise.

PlanOut provides hooks for your logging code so that you can log whenever a unit is exposed to an experiment.

## Overriding the logExposure method
