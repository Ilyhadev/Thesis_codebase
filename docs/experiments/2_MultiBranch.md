# Результат 2

Пример работы одной задачи и вызова задачи монитора раз в 30 секунд.

Было создано две задачи PeriodicTask:
- osPriorityAboveNormal, period_ms = 13, workload_loops = 3000;
- osPriorityNormal, period_ms = 40, workload_loops = 1000;
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
        	} else if (rand() % 3) {
        		volatile uint32_t dummy = i * 2;
        	} else if (rand() % 2) {
        		volatile uint32_t dummy = i * 2;
        		volatile uint32_t dummy2 = i * 2;
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

Данные
```bash
(.venv)  ilia@AsusTuf  ~/Desktop/vsCode/Embedded-work/TinyMLExperiments/motion_detector/helpers  python3 TestSerialRead.py
Listening on /dev/ttyUSB0
Press Ctrl+C to stop

Received 70
b'100k loops = 21878 us\n=== All tasks created - starting scheduler ===\r\n'
Received 273
b'Task 0 | Jobs:2309 | Jitter min/avg/max: 4/12/16 us | Max R: 9161 us | Max C: 9169 us | Min C: 8857 us | Avg C: 9030 us | Misses: 0\r\nTask 1 | Jobs:751 | Jitter min/avg/max: -100/3425/9057 us | Max R: 12300 us | Max C: 3113 us | Min C: 2957 us | Avg C: 3030 us | Misses: 0\r\n'
Received 272
b'Task 0 | Jobs:2307 | Jitter min/avg/max: 9/12/16 us | Max R: 9432 us | Max C: 9444 us | Min C: 8857 us | Avg C: 9028 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -97/3402/9059 us | Max R: 12271 us | Max C: 3144 us | Min C: 2952 us | Avg C: 3029 us | Misses: 0\r\n'
Received 272
b'Task 0 | Jobs:2306 | Jitter min/avg/max: 9/12/16 us | Max R: 9463 us | Max C: 9471 us | Min C: 8857 us | Avg C: 9031 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -97/3414/9072 us | Max R: 12887 us | Max C: 3132 us | Min C: 2945 us | Avg C: 3029 us | Misses: 0\r\n'
Received 272
b'Task 0 | Jobs:2307 | Jitter min/avg/max: 9/12/21 us | Max R: 9449 us | Max C: 9458 us | Min C: 8845 us | Avg C: 9030 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -97/3432/9029 us | Max R: 12281 us | Max C: 3107 us | Min C: 2943 us | Avg C: 3029 us | Misses: 0\r\n'
Received 192
b'Task 0 | Jobs:2307 | Jitter min/avg/max: 9/12/16 us | Max R: 9405 us | Max C: 9414 us | Min C: 8845 us | Avg C: 9030 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -98/3409/9046 us | '
Received 80
b'Max R: 12340 us | Max C: 3192 us | Min C: 2937 us | Avg C: 3029 us | Misses: 0\r\n'
Received 224
b'Task 0 | Jobs:2306 | Jitter min/avg/max: 9/12/16 us | Max R: 9441 us | Max C: 9450 us | Min C: 8845 us | Avg C: 9032 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -100/3403/9044 us | Max R: 12875 us | Max C: 3110 u'
Received 49
b's | Min C: 2937 us | Avg C: 3029 us | Misses: 0\r\n'
Received 224
b'Task 0 | Jobs:2307 | Jitter min/avg/max: 9/12/16 us | Max R: 9424 us | Max C: 9433 us | Min C: 8845 us | Avg C: 9031 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -99/3435/9060 us | Max R: 12269 us | Max C: 3161 us'
Received 48
b' | Min C: 2937 us | Avg C: 3030 us | Misses: 0\r\n'
Received 224
b'Task 0 | Jobs:2307 | Jitter min/avg/max: 9/12/16 us | Max R: 9441 us | Max C: 9449 us | Min C: 8845 us | Avg C: 9030 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -100/3418/9052 us | Max R: 12261 us | Max C: 3958 u'
Received 49
b's | Min C: 2921 us | Avg C: 3032 us | Misses: 0\r\n'
Received 128
b'Task 0 | Jobs:2307 | Jitter min/avg/max: 9/12/16 us | Max R: 9453 us | Max C: 9461 us | Min C: 8845 us | Avg C: 9032 us | Misses'
Received 144
b': 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -97/3398/9066 us | Max R: 12533 us | Max C: 3164 us | Min C: 2921 us | Avg C: 3030 us | Misses: 0\r\n'
Received 224
b'Task 0 | Jobs:2306 | Jitter min/avg/max: 9/12/16 us | Max R: 9434 us | Max C: 9443 us | Min C: 8845 us | Avg C: 9032 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -97/3436/9064 us | Max R: 12265 us | Max C: 3128 us'
Received 48
b' | Min C: 2921 us | Avg C: 3029 us | Misses: 0\r\n'
Received 272
b'Task 0 | Jobs:2307 | Jitter min/avg/max: 9/12/16 us | Max R: 9420 us | Max C: 9429 us | Min C: 8845 us | Avg C: 9031 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -97/3422/9062 us | Max R: 12276 us | Max C: 3148 us | Min C: 2921 us | Avg C: 3029 us | Misses: 0\r\n'
Received 272
b'Task 0 | Jobs:2307 | Jitter min/avg/max: 9/12/16 us | Max R: 9442 us | Max C: 9451 us | Min C: 8845 us | Avg C: 9033 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -97/3403/9037 us | Max R: 12273 us | Max C: 3166 us | Min C: 2921 us | Avg C: 3030 us | Misses: 0\r\n'
Received 272
b'Task 0 | Jobs:2306 | Jitter min/avg/max: 9/12/16 us | Max R: 9415 us | Max C: 9423 us | Min C: 8845 us | Avg C: 9032 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -97/3425/9041 us | Max R: 12281 us | Max C: 3132 us | Min C: 2921 us | Avg C: 3029 us | Misses: 0\r\n'
Received 272
b'Task 0 | Jobs:2307 | Jitter min/avg/max: 9/12/16 us | Max R: 9489 us | Max C: 9497 us | Min C: 8845 us | Avg C: 9033 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -97/3429/9055 us | Max R: 12252 us | Max C: 3139 us | Min C: 2921 us | Avg C: 3029 us | Misses: 0\r\n'
Received 256
b'Task 0 | Jobs:2307 | Jitter min/avg/max: 9/12/16 us | Max R: 9454 us | Max C: 9462 us | Min C: 8818 us | Avg C: 9032 us | Misses: 0\r\nTask 1 | Jobs:750 | Jitter min/avg/max: -97/3408/9048 us | Max R: 12257 us | Max C: 3166 us | Min C: 2921 us | Avg C: 3030 '
Received 16
b'us | Misses: 0\r\n
```

## Вывод
В случае с более частым мониторингом задач и более сложным ветвлением инструкций данные по jitter второй задачи оказались намного интереснее. Комбинация Release jitter + execution jitter заставило FreeRTOS вмешиваться агрессивнее (отрицательный минимальный jitter). Приоритетная задача вызывает больше прерываний на 2 задаче + специально сделанное случайное ветвления симулирующее настоящие задачи (например получение кватерниона по сети -> проверка на нормальность => если нормальный то задача заканчивается быстрее, если нет то намного дольше).
