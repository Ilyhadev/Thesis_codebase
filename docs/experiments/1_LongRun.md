# Результат 1

Пример работы одной задачи и вызова задачи монитора раз в 3 часа.

Задача имела период в 100 ms и workload = 40000 состояла из:
```C
void PeriodicTask(void *argument) {
    TaskParams_t *p = (TaskParams_t *)argument;

    TickType_t xLastWakeTime = xTaskGetTickCount();
    uint64_t theoretical_us = get_micros64();

    while (1) {
    	uint64_t release_us = get_micros64();
        int32_t  jitter_us  = (int32_t)(release_us - theoretical_us);

        /* Start fresh measurement for this job */
        task_cpu_cycles[p->idx] = 0;

        for (volatile uint32_t i = 0; i < p->workload_loops; i++){
        	if (i % (rand() % 10 + 1) == 0) {
        	        volatile uint32_t dummy = i * 2;
            }
        }

        uint64_t finish_us = get_micros64();
        uint32_t response_us = (uint32_t)(finish_us - release_us);



        /* Update stats */
        if (jitter_us < stats[p->idx].min_jitter_us) stats[p->idx].min_jitter_us = jitter_us;
        if (jitter_us > stats[p->idx].max_jitter_us) stats[p->idx].max_jitter_us = jitter_us;
        stats[p->idx].sum_jitter_us += jitter_us;
        stats[p->idx].job_count++;
        if (response_us > stats[p->idx].max_response_us) stats[p->idx].max_response_us = response_us;
        if (response_us > (p->period_ms * 1000UL)){
        	stats[p->idx].deadline_misses++;
        }
        /* Pure execution time C = all CPU slices + current slice */
        uint32_t current_slice = DWT->CYCCNT - task_cpu_start_cycles;
        uint32_t pure_c_us     = (task_cpu_cycles[p->idx] + current_slice) / 64U;

        if (pure_c_us > stats[p->idx].max_pure_c_us)     stats[p->idx].max_pure_c_us = pure_c_us;
        if (pure_c_us < stats[p->idx].min_pure_c_us)     stats[p->idx].min_pure_c_us = pure_c_us;
        stats[p->idx].sum_pure_c_us += pure_c_us;

        vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(p->period_ms));
        theoretical_us += (uint64_t)p->period_ms * 1000ULL;
    }
}
```


---

Данные:
```bash
(.venv)  ilia@AsusTuf  ~/Desktop/vsCode/Embedded-work/TinyMLExperiments/motion_detector/helpers  python3 TestSerialRead.py
Listening on /dev/ttyUSB0
Press Ctrl+C to stop

Received 70
b'100k loops = 21970 us\n=== All tasks created - starting scheduler ===\r\n'
Received 138
b'Task 0 | Jobs:22102 | Jitter min/avg/max: 1/10/11 us | Max R: 69124 us | Max C: 69130 us | Min C: 69083 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22100 | Jitter min/avg/max: 11/11/11 us | Max R: 69123 us | Max C: 69129 us | Min C: 69083 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22100 | Jitter min/avg/max: 11/11/11 us | Max R: 69123 us | Max C: 69129 us | Min C: 69083 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22101 | Jitter min/avg/max: 11/11/11 us | Max R: 69123 us | Max C: 69129 us | Min C: 69083 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22100 | Jitter min/avg/max: 11/11/11 us | Max R: 69126 us | Max C: 69132 us | Min C: 69083 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22100 | Jitter min/avg/max: 11/11/11 us | Max R: 69125 us | Max C: 69131 us | Min C: 69080 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22101 | Jitter min/avg/max: 11/11/11 us | Max R: 69123 us | Max C: 69129 us | Min C: 69080 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22100 | Jitter min/avg/max: 11/11/11 us | Max R: 69123 us | Max C: 69129 us | Min C: 69080 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22100 | Jitter min/avg/max: 11/11/11 us | Max R: 69124 us | Max C: 69130 us | Min C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22101 | Jitter min/avg/max: 11/11/11 us | Max R: 69126 us | Max C: 69132 us | Min C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22100 | Jitter min/avg/max: 11/11/11 us | Max R: 69120 us | Max C: 69126 us | Min C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22101 | Jitter min/avg/max: 11/11/11 us | Max R: 69124 us | Max C: 69130 us | Min C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22101 | Jitter min/avg/max: 11/11/11 us | Max R: 69122 us | Max C: 69128 us | Min C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
Received 96
b'Task 0 | Jobs:22100 | Jitter min/avg/max: 11/11/11 us | Max R: 69124 us | Max C: 69130 us | Min '
Received 43
b'C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22101 | Jitter min/avg/max: 11/11/11 us | Max R: 69121 us | Max C: 69127 us | Min C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
Received 64
b'Task 0 | Jobs:22101 | Jitter min/avg/max: 11/11/11 us | Max R: 6'
Received 75
b'9122 us | Max C: 69128 us | Min C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22100 | Jitter min/avg/max: 11/11/11 us | Max R: 69122 us | Max C: 69128 us | Min C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22101 | Jitter min/avg/max: 11/11/11 us | Max R: 69123 us | Max C: 69128 us | Min C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
Received 139
b'Task 0 | Jobs:22101 | Jitter min/avg/max: 11/11/11 us | Max R: 69122 us | Max C: 69128 us | Min C: 69077 us | Avg C: 69106 us | Misses: 0\r\n'
^C
Stopped
```

## Вывод
Release jitter довольно хорошо обрабатывается механизмами FreeRTOS и держится в районе 11 микросекунд. Однако даже минимальное усложнение в логике самой задачи уже вызвало execution jitter в 55 микросекунд: "Max C: 69132 us | Min C: 69077 us" - из одного из 3-ех часовых замеров.