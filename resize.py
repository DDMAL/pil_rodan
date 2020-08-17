from PIL import Image
from rodan.jobs.base import RodanTask


IDEAL_SSH_PX = 64   # SSH from old Salzinnes images


class Resize(RodanTask):
    name = "Resize Image"
    author = "Juliette Regimbal"
    description = "Resize an image"
    settings = {
        "job_queue": "Python2",
        "title": "Resizing Parameters",
        "type": "object",
        "required": ["Value Type", "Value"],
        "properties": {
            "Value Type": {
                "type": "string",
                "enum": ["Staff Size Height (px)", "Ratio"],
                "description": "The way to interpret the provided value. If staff size height, then scale the image such that it meets an ideal staff size height for layer training and classification. If a ratio, scale by that ratio (i.e. 0.5 reduces dimensions by half)."
            },
            "Value": {
                "type": "number",
                "exclusiveMinimum": 0
            }
        }
    }
    enabled = "True"
    category = "PIL - Manipulation"
    interactive = False

    input_port_types = (
        {"name": "Image", "minimum": 1, "maximum": 1, "resource_types": lambda mime: mime.startswith("image/")}
    )
    output_port_types = (
        {"name": "Resized PNG Image", "minimum": 1, "maximum": 1, "resource_types": ["image/rgb+png"]}
    )

    def run_my_task(self, inputs, settings, outputs):
        infile = inputs["Image"][0]["resource_path"]
        outfile = outputs["Resized PNG Image"][0]["resource_path"]

        image = Image.open(infile)
        if settings["Value Type"] != "Ratio":
            ratio = IDEAL_SSH_PX / settings["Value"]
        else:
            ratio = settings["Value"]

        width, height = image.size
        width = width * ratio
        height = height * ratio
        image = image.resize((width, height))
        image.save(outfile, "PNG")
