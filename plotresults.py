import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
from collections import defaultdict
from conftest import NUM_SAMPLES, VERSIONS, DAYS

TOTAL = NUM_SAMPLES * len(VERSIONS) * len(DAYS)
columns = range(0, TOTAL)
tests = ['test_board_LED', 'test_converter_LED', 'test_pow_generated']
data = defaultdict(lambda: [0] * TOTAL)

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

fig, ((ax1, ax3, ax5, ax7), (ax2, ax4, ax6, ax8)) = plt.subplots(2, 4)
ax_arr = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]
fig.suptitle('Test iterations')


start = 0
end = NUM_SAMPLES
for x in range(TOTAL // NUM_SAMPLES):
    ax = ax_arr[end // NUM_SAMPLES - 1]
    ax.set_title(f'Version : {x//2}, Round: {x%2}')
    y_offset = np.zeros(NUM_SAMPLES)
    for i, t in enumerate(tests):

        data_x = columns[start:end]
        data_y = data[t][start:end]
        ax.bar(data_x, data_y, label=t, bottom=y_offset)
        y_offset += 1

    start += NUM_SAMPLES
    end += NUM_SAMPLES

plt.legend()
plt.show()
