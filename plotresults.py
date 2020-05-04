import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
from collections import defaultdict
from conftest import NUM_SAMPLES

columns = range(0, NUM_SAMPLES)
tests = ['test_board_LED', 'test_converter_LED', 'test_LEDS_match', 'test_pow_generated']
data = defaultdict(lambda: [0] * NUM_SAMPLES)


root = ET.parse('result.xml').getroot()
test_cases = root.findall('.//testcase')
for t in test_cases:
    fail = t.findall('./failure')
    if fail:
        for f in fail:
            name = t.attrib['name'].split('[')
            test_name = name[0]
            if len(name) > 1:
                device = int(''.join([s for s in name[1] if s.isdigit()]))
                data[test_name][device] = 1


y_offset = np.zeros(NUM_SAMPLES)
for i, t in enumerate(tests):
    plt.bar(columns, data[t], label=t, bottom=y_offset)
    y_offset += data[t]

plt.legend()
plt.show()

