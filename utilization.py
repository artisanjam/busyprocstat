'''Measures and reports on CPU utilization by parsing /proc/stat.'''
from time import sleep

# Configurable constants
SAMPLE_INTERVAL_SECONDS = 1
REPORT_INTERVAL_SECONDS = 5
UTILIZATION_WARNING_PCT = 90

# Messages
STANDARD_REPORT = \
        'CPU Utilization: {utilization:.2f}%'
UTILIZATION_WARNING = \
        'WARNING: CPU Utilization is {utilization:.2f}%'

def sample_procstat(procstat_file):
    '''Convert total CPU usage from procstat into a tuple.'''
    line = procstat_file.readline()
    procstat_file.seek(0)
    return [int(field) for field in line.split()[1:]]

def get_usage_idle(fields):
    '''Return aggregate of usage and idle time in a tuple.'''
    usage = sum(fields[0:3]) + sum(fields[5:8])
    idle = sum(fields[3:5])
    return (usage, idle)

def get_deltas(sample, last_sample):
    '''Measure changes between sample and last_sample.

    return changes as tuple (delta_usage, delta_idle)
    '''
    usage, idle  = get_usage_idle(sample)
    last_usage, last_idle = get_usage_idle(last_sample)
    delta_usage = (usage - last_usage)
    delta_idle = (idle - last_idle)
    return (delta_usage, delta_idle)

def test_utilization(deltas):
    '''Calculate utilization from changes in CPU accounting.'''
    utilization = deltas[0] / (deltas[0] + deltas[1])
    utilization_pct = utilization * 100
    if utilization_pct >= UTILIZATION_WARNING_PCT:
        print(UTILIZATION_WARNING.format(utilization=utilization_pct))
    return utilization_pct

def main():
    '''Prints CPU utilization periodically.'''
    with open('/proc/stat', 'r') as procstat:
        last_sample = sample_procstat(procstat)
        sleep(SAMPLE_INTERVAL_SECONDS)
        while True:
            waited = 0
            while waited < REPORT_INTERVAL_SECONDS:
                sample = sample_procstat(procstat)

                # Calculate change over two previous samples
                deltas = get_deltas(sample, last_sample)
                last_sample = sample
                utilization_pct = test_utilization(deltas)
                sleep(SAMPLE_INTERVAL_SECONDS)
                waited += SAMPLE_INTERVAL_SECONDS

            # Simplification: prints last utilization according to
            # SAMPLE_INTERVAL_SECONDS not aggregate utilization
            # over REPORT_INTERVAL_SECONDS
            print(STANDARD_REPORT.format(utilization=utilization_pct))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Expected closure; emit a newline
        print()
