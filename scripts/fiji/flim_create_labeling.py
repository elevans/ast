#@ OpEnvironment ops
#@ ConvertService cs
#@ UIService ui
#@ Img (label = "Input image:", autofill = false) img
#@ String (visibility=MESSAGE, value="<b>[ Set threshold level ]</b>", required=false) ths_msg
#@ Integer (label = "Threshold value:", min = 0, value = 1) ths
#@ String (visibility=MESSAGE, value="<b>[ Enter size range (labels within this range are retained) ]</b>", required=false) filter_msg
#@ Integer (label="Minimum size (pixels):", min=0, value=0) min_size
#@ Integer max_size(label="Maximum size (pixels):", value=0) max_size
#@ String (visibility=MESSAGE, value="<b>[ Output settings ]</b>", required=false) output_msg
#@ Boolean (label = "Show label image:", value = false) show

from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement
from net.imglib2.roi import Regions
from net.imglib2.roi.labeling import ImgLabeling, LabelRegions
from net.imglib2.type.logic import BitType
from net.imglib2.type.numeric.integer import UnsignedShortType

def binarize(image, threshold_value):
    """Create a binary image with the given threshold.

    :param image:

        An input image.

    :param threshold_value:

        The threshold value top apply.

    :return:

        The input image binarized with the given
        threshold value.
    """
    t = ops.op("convert.uint16").input(ths).apply()
    binary_img = ops.op("create.img").input(img, BitType()).apply()
    ops.op("threshold.apply").input(img, t).output(binary_img).compute()

    return binary_img


def label(image, connected_type = "four"):
    """Create an ImgLabeling from the input binary image.

    :param: image:

        An input binary image (BitType).

    :param connected_type:

        Define wether four or eight connected structuring
        element is applied.

    :return:

        An ImgLabeling.
    """
    if connected_type == "four":
        se = StructuringElement.FOUR_CONNECTED
    elif connected_type == "eight":
        se = StructuringElement.EIGHT_CONNECTED
    else:
        se = StructuringElement.FOUR_CONNECTED

    return ops.op("labeling.cca").input(image, se).apply()


def set_zero(sample):
    """Set a sample region's pixel values to 0.

    :param:

        A sample region.
    """
    # get the sample region's cursor
    c = sample.cursor()
    # set all pixels within the sample region to 0
    while c.hasNext():
        c.fwd()
        c.get().set(0)


def size_filter(labeling, min_size, max_size):
    """Apply a size filter to an ImgLabeling.

    :param labeling:

        An ImgLabeling to filter.

    :param min_size:

        Minimum size of object to retain.

    :param max_size:

        Maximum size of object to retain.

    :return:

        Size filtered ImgLabeling.
    """
    label_img = labeling.getIndexImg()
    regs = LabelRegions(labeling)
    for r in regs:
        sample = Regions.sample(r, label_img)
        size = sample.size()
        #size = ops.op("stats.size").input(sample).apply()
        if size <= float(min_size) or size >= float(max_size):
            set_zero(sample)

    return cs.convert(label_img, ImgLabeling)

# get label/mask over good data
binary = binarize(img, ths)
labeling = label(binary)
labeling = size_filter(labeling, min_size, max_size)
label_img = labeling.getIndexImg()

# zero out only the non mask pixels
c = img.cursor()
ra = label_img.randomAccess()
while c.hasNext():
    c.fwd()
    ra.setPosition(c)
    if ra.get().getRealDouble() <= 0.0:
        c.get().set(0)

if show:
    ui.show("result", label_img)

print("[INFO]: Done...")
