import rodan
__version__ = "1.1.6"

import logging
logger = logging.getLogger('rodan')

from rodan.jobs import module_loader

module_loader('rodan.jobs.pil-rodan.red_filtering')
module_loader('rodan.jobs.pil-rodan.to_png')
module_loader('rodan.jobs.pil-rodan.to_tiff')
module_loader('rodan.jobs.pil-rodan.to_jpeg2000')
module_loader('rodan.jobs.pil-rodan.resize')
