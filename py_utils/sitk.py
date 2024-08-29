from collections.abc import Sequence
from typing import Any, Union

import numpy as np
import SimpleITK as sitk

from python_utils.types import Pathlike

__all__ = [
    "load_sitk",
    "get_metadata_from_sitk",
    "load_sitk_as_array",
    "write_sitk",
    "world_to_voxel_coords",
    "normalize",
    "h_flip",
    "v_flip",
    "get_physical_center",
    "resample_3d_image_spacing",
    "resample",
    "change_image_direction",
    "from_array_to_sitk_image",
    "set_origin_direction_spacing",
]


def load_sitk(path: Pathlike, **kwargs: Any) -> sitk.Image:
    """Functional interface to load image with sitk.

    Args:
        path: path to file to load

    Returns:
        sitk.Image: loaded sitk image
    """
    return sitk.ReadImage(str(path), **kwargs)


def get_metadata_from_sitk(sitk_image: sitk.Image) -> dict[str, Any]:
    return {
        key: sitk_image.GetMetaData(key)
        for key in sitk_image.GetMetaDataKeys()
    }


def load_sitk_as_array(
    path: Pathlike,
    return_meta: bool = False,
    **kwargs: Any,
) -> Union[np.ndarray, tuple[np.ndarray, dict[str, Any]]]:
    """Functional interface to load sitk image and convert it to an array.

    Args:
        path: path to file to load

    Returns:
        np.ndarray: loaded image data
        dict: loaded meta data
    """
    img_itk = load_sitk(path, **kwargs)
    array: np.ndarray = sitk.GetArrayFromImage(img_itk)
    if return_meta:
        meta = get_metadata_from_sitk(img_itk)
        return array, meta
    return array


def write_sitk(
    img: Union[sitk.Image, np.ndarray],
    path: Pathlike,
    src_img: Union[sitk.Image, None] = None,
    direction: Union[tuple[float, ...], None] = None,
    origin: Union[tuple[float, ...], None] = None,
    spacing: Union[tuple[float, ...], None] = None,
) -> None:
    """Functional interface to write an image with sitk.

    Args:
        img (Union[sitk.Image, np.ndarray]): Image or numpy array to write
        path (Pathlike): path to file to load
        src_img (Union[sitk.Image, None]): Image to copy Information from. Default to None.
        origin (Union[tuple[float, ...], None], optional): Coordinates [x,y] or [x,y,z] of the origin vector. Defaults to None.
        direction (Union[tuple[float, ...], None], optional): 1D vector of direction matrix in row major :
            [o11, o12, o21, o22] (2D) or [o11, o12, 13, o21, o22, o23, o31, o32, o33] (3D).
            Defaults to None.
        spacing (Union[tuple[float, ...], None], optional): Spacing vector. Should have length 2 (2 dim) or 3 (3 dim). Defaults to None.
    Returns:
        None
    """
    if isinstance(img, np.ndarray):
        img = sitk.GetImageFromArray(img)

    if src_img:
        img.CopyInformation(src_img)

    set_origin_direction_spacing(
        img,
        origin=origin,
        direction=direction,
        spacing=spacing,
    )

    sitk.WriteImage(img, path)


def world_to_voxel_coords(
    world_coords: np.ndarray,
    origin: Sequence[Union[int, float]],
    spacing: Sequence[Union[int, float]],
) -> np.ndarray:
    """Convert coordinate from world to voxels coordinates.

    This function is from the LUNA tutorial :
    https://luna16.grand-challenge.org/Tutorial/

    Args:
        world_coord (np.ndarray): coordinate in world reference
        origin (Sequence[Union[int, float]]): origin of the sitk image
        spacing (Sequence[Union[int, float]]): spacing of the sitk image

    Returns:
        voxel_coord (np.ndarray): coordinates in voxel reference
    """
    stretched_voxel_coords = np.absolute(world_coords - origin)
    voxel_coord = stretched_voxel_coords / spacing

    return voxel_coord


def normalize(
    image: sitk.Image,
    min_percentile: float,
    max_percentile: float,
    output_min: int,
    output_max: int,
) -> sitk.Image:
    """Limit Image to {min,max}_percentile and rescale to output_{min,max} values.

    Args:
        image (sitk.Image): Image to normalize
        min_percentile (float): Lower percentile to which to limit the image
        max_percentile (float): Upper percentile to which to limit the image
        output_min (int): Min value to which to rescale the output Image
        output_max (int): Max value to which to rescale the output Image

    Returns:
        sitk.Image: Normalized image
    """
    window_rescale = sitk.IntensityWindowingImageFilter()
    image_array = sitk.GetArrayFromImage(image)
    window_min = np.percentile(image_array, min_percentile)
    window_max = np.percentile(image_array, max_percentile)
    return window_rescale.Execute(
        image,
        window_min,
        window_max,
        output_min,
        output_max,
    )


def h_flip(image: sitk.Image) -> sitk.Image:
    """Flip Image horizontally (around the vertical axis).

    Args:
        image (sitk.Image): Image to flip

    Returns:
        sitk.Image: Horizontally flipped image
    """
    image_np = sitk.GetArrayViewFromImage(image)
    image_np = np.flip(image_np, 0)
    image_flipped = sitk.GetImageFromArray(image_np)
    image_flipped.CopyInformation(image)
    return image_flipped


def v_flip(image: sitk.Image) -> sitk.Image:
    """Flip Image vertically (around the horizontal axis).

    Args:
        image (sitk.Image): Image to flip

    Returns:
        sitk.Image: Vertically flipped image
    """
    image_np = sitk.GetArrayViewFromImage(image)
    image_np = np.flip(image_np, 1)
    image_flipped = sitk.GetImageFromArray(image_np)
    image_flipped.CopyInformation(image)
    return image_flipped


def set_origin_direction_spacing(
    image: sitk.Image,
    origin: Union[tuple[float, ...], None] = None,
    direction: Union[tuple[float, ...], None] = None,
    spacing: Union[tuple[float, ...], None] = None,
) -> None:
    """Set origin, direction and spacing of a SimpleITK image.

    Updates are done inplace via the C++ lib. The functions do not return anything.

    Args:
        image (sitk.Image): Image
        origin (Union[tuple[float, ...]], None, optional): Coordinates [x,y] or [x,y,z] of the origin vector. Defaults to None.
        direction (Union[tuple[float, ...]], None, optional): 1D vector of direction matrix in row major :
            [o11, o12, o21, o22] (2D) or [o11, o12, 13, o21, o22, o23, o31, o32, o33] (3D).
            Defaults to None.
        spacing (Union[tuple[float, ...]], None, optional): Spacing vector. Should have length 2 (2 dim) or 3 (3 dim). Defaults to None.
    """
    # function returns None
    if origin:
        image.SetOrigin(origin)
    if direction:
        image.SetDirection(direction)
    if spacing:
        image.SetSpacing(spacing)


def get_physical_center(
    img: sitk.Image,
) -> list[float]:

    """This function returns the physical center point of a 3d sitk image.

    It returns the physical center point of the image.
    """
    width, height, depth = img.GetSize()
    return img.TransformIndexToPhysicalPoint(
        (
            int(np.ceil(width / 2)),
            int(np.ceil(height / 2)),
            int(np.ceil(depth / 2)),
        ),
    )


def resample_3d_image_spacing(
    image: sitk.Image,
    new_spacing: np.array,
) -> sitk.Image:

    spacing_x, spacing_y, spacing_z = new_spacing
    spacing_orig_x, spacing_orig_y, spacing_orig_z = image.GetSpacing()
    size = image.GetSize()
    fact_x = spacing_orig_x / spacing_x
    fact_y = spacing_orig_y / spacing_y
    fact_z = spacing_orig_z / spacing_z
    size_x = int(round(size[0] * fact_x))
    size_y = int(round(size[1] * fact_y))
    size_z = int(round(size[2] * fact_z))

    origin = image.GetOrigin()
    # Direction cosine matrix (vector like type representing matrix in row major order) - direction of each of the axes corresponding to the matrix columns.
    direction = image.GetDirection()

    f = sitk.ResampleImageFilter()
    f.SetOutputDirection(direction)
    f.SetOutputOrigin(origin)
    f.SetOutputSpacing((spacing_x, spacing_y, spacing_z))
    f.SetSize((size_x, size_y, size_z))
    f.SetInterpolator(sitk.sitkBSpline)
    result = f.Execute(image)

    return result


def resample(
    image: sitk.Image,
    transform: sitk.Transform,  # An sitk transform (ex. resizing, rotation, etc.
    interpolator: sitk.Transform = sitk.sitkLinear,
    default_value: int = -1024,
) -> sitk.Image:

    reference_image = image

    return sitk.Resample(
        image,
        reference_image,
        transform,
        interpolator,
        default_value,
    )


def change_image_direction(
    image: sitk.Image,
    new_direction=[1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, -1.0],
) -> sitk.Image:
    euler_transform = sitk.Euler3DTransform()
    image_center = get_physical_center(image)
    euler_transform.SetCenter(image_center)
    euler_transform.SetMatrix(new_direction)

    resampled_image = resample(image, euler_transform)
    return resampled_image


def from_array_to_sitk_image(
    array: np.array,
    sitk_image: sitk.Image,
    output_filename: Pathlike,
):

    image = sitk.GetImageFromArray(array)
    image.SetSpacing(sitk_image.GetSpacing())
    image.SetOrigin(sitk_image.GetOrigin())
    sitk.WriteImage(image, output_filename)
