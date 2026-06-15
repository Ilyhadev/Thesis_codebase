# Jitter types and pWCET relevance

This note defines jitter types useful for the current FreeRTOS + STM32F103 + MPU6050 experiments.

## 1. Release jitter

Deviation of a periodic task start from its ideal release time.

```text
J_release = actual_start_time - expected_start_time
```

Use in this project:

- `I2CReadTask` periodic wake-up accuracy.
- Shows how precisely FreeRTOS releases a periodic task.

Why it matters for pWCET:

- If a task starts late, its execution can overlap with other jobs differently.
- This changes interference patterns and can move rare worst-case combinations closer together.

## 2. Execution-time jitter

Variation of task execution time.

```text
J_C = C_max - C_min
```

Use in this project:

- I2C task varies because FIFO state and blocking I2C transactions vary.
- CPU-only tasks have smaller `J_C`; peripheral tasks have larger `J_C`.

Why it matters for pWCET:

- pWCET is about the tail of the execution-time distribution.
- Large `J_C` means rare long executions exist and must be included in probabilistic bounds.

## 3. Response-time jitter

Variation of total job response time.

```text
R = finish_time - release_time
J_R = R_max - R_min
```

Use in this project:

- Captures execution plus preemption, blocking, queue effects, and peripheral waiting.

Why it matters for pWCET:

- Deadlines depend on response time, not only pure CPU time.
- A task can have stable `C` but unstable `R` due to interference.

## 4. Activation latency jitter

Variation in delay between data becoming ready and a dependent task starting.

```text
J_activation = task_start_time - data_ready_time
```

Use in this project:

- `ProcessDataTask` after I2C sample is queued.
- `UartSendTask` after processed data is queued.

Why it matters for pWCET:

- In pipelines, worst-case end-to-end latency depends on handoff delays between stages.
- pWCET of the full chain must include queue wake-up and scheduling latency.

## 5. Inter-arrival jitter

Variation in time between consecutive input events or samples.

```text
J_arrival = actual_inter_arrival_time - nominal_inter_arrival_time
```

Use in this project:

- MPU6050 sample production is independent from the MCU scheduler.
- FIFO can convert small sample timing differences into burst arrivals.

Why it matters for pWCET:

- Bursts can create rare high-load windows.
- These bursts can increase execution-time and response-time tails.

## 6. Blocking jitter

Variation caused by time spent waiting for a shared resource or peripheral.

Use in this project:

- Blocking HAL I2C calls.
- UART used by monitor.
- Queue operations if buffers fill.

Why it matters for pWCET:

- Blocking time is often input/state dependent.
- Rare peripheral or buffer states can dominate the worst-case tail.

## Why pWCET instead of a fixed margin

A simple approach is to take the maximum observed execution time and multiply it by a fixed safety factor, for example:

```text
WCET_estimate = 2 * max_observed_C
```

This is easy to understand, but it can reserve too many resources for a border that is not statistically justified. pWCET gives a probabilistic bound instead:

```text
P(C > bound) < target_probability
```

This allows the bound to match task criticality. A safety-critical task can require an extremely small exceedance probability, while a non-critical task can use a less strict bound and leave more CPU capacity for other work.

pWCET does not remove safety margins. It makes them explicit and quantifiable.

## Summary

For this project:

```text
Release jitter       -> when task starts
Execution-time jitter -> how long task executes
Response-time jitter  -> how long job takes from start to finish
Activation jitter     -> how late next pipeline stage starts
Inter-arrival jitter  -> how irregular external samples arrive
Blocking jitter       -> how variable waiting on shared/peripheral resources is
```

For pWCET, jitter matters because it describes the variability that creates the distribution tail. Average execution time is not enough: rare FIFO bursts, blocking I2C transfers, queue delays, and unlucky task phasing are exactly the events that shape probabilistic worst-case execution time.
