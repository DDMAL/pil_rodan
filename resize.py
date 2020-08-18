from PIL import Image
from rodan.jobs.base import RodanTask


IDEAL_SSH_PX = 64   # SSH from old Salzinnes images
Image.MAX_IMAGE_PIXELS = 1000000000 # We have to deal with very large images, but keep some decompression bomb protection


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
        {'name': 'Resized PNG Image', 'minimum': 1, 'maximum': 1, 'resource_types': ['image/rgb+png']}
    ]

    def run_my_task(self, inputs, settings, outputs):
        infile = inputs['Image'][0]['resource_path']
        outfile = outputs['Resized PNG Image'][0]['resource_path']

        image = Image.open(infile)
        if settings['Action'] != 'Ratio':
            ratio = IDEAL_SSH_PX / settings['Scale Value']
        else:
            ratio = settings['Scale Value']

        width, height = image.size
        width = int(width * ratio)
        height = int(height * ratio)
        image = image.resize((width, height))
        image.save(outfile, 'PNG')

    def test_my_task(self, testcase):
        pass
