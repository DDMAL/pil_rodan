import rodan
__version__ = rodan.__version__

import logging
logger = logging.getLogger('rodan')

from rodan.jobs import module_loader

module_loader('rodan.jobs.pil-rodan.red_filtering')
module_loader('rodan.jobs.pil-rodan.to_png')
module_loader('rodan.jobs.pil-rodan.to_tiff')
module_loader('rodan.jobs.pil-rodan.to_jpeg2000')
