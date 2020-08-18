from celery.utils.log import get_task_logger
from PIL import Image
from rodan.jobs.base import RodanTask


IDEAL_SSH_PX = 64.   # SSH from old Salzinnes images
Image.MAX_IMAGE_PIXELS = 1000000000 # We have to deal with very large images, but keep some decompression bomb protection


logger = get_task_logger(__name__)


class resize(RodanTask):
    name = 'Resize Image'
    author = 'Juliette Regimbal'
    description = 'Resize an image'
    settings = {
        'title': 'Options',
        'type': 'object',
        'properties': {
            'Scale Value': {
                'type': 'number',
                'default': 1,
                'minimum': 0,
                'exclusiveMinimum': True
            },
            'Action': {
                'enum': ['Staff Scale Height', 'Ratio'],
                'type': 'string',
                'default': 'Ratio',
                'description': 'The way to interpret the provided value. If staff size height, then scale the image such that it meets an ideal staff size height for layer training and classification. If a ratio, scale by that ratio (i.e. 0.5 reduces dimensions by half).'
            }
        },
        'job_queue': 'Python2',
    }
    enabled = True
    category = 'PIL - Manipulation'
    interactive = False

    input_port_types = [
        {'name': 'Image', 'minimum': 1, 'maximum': 1, 'resource_types': lambda mime: mime.startswith('image/')}
    ]
    output_port_types = [
        {'name': 'Resized PNG Image', 'minimum': 1, 'maximum': 1, 'resource_types': ['image/rgb+png']},
        {'name': 'Inverse Scale Ratio', 'minimum': 0, 'maximum': 1, 'resource_types': ['text/plain']},
    ]

    def run_my_task(self, inputs, settings, outputs):
        infile = inputs['Image'][0]['resource_path']
        outfile = outputs['Resized PNG Image'][0]['resource_path']

        image = Image.open(infile)
        logger.info(settings['Action'])
        if self.settings['properties']['Action']['enum'][settings['Action']] != 'Ratio':
            ratio = IDEAL_SSH_PX / float(settings['Scale Value'])
        else:
            ratio = settings['Scale Value']

        logger.info("Resize to {}".format(str(ratio)))

        width, height = image.size
        width = int(width * ratio)
        height = int(height * ratio)
        image = image.resize((width, height))
        image.save(outfile, 'PNG')

        if len(outputs['Inverse Scale Ratio']) > 0:
            inverse = 1 / ratio
            with open(outputs['Inverse Scale Ratio'][0]['resource_path'], 'w') as f:
                f.write(str(inverse))

    def test_my_task(self, testcase):
        pass
