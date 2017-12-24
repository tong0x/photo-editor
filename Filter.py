import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from PIL import Image, ImageFilter

# the effect input is 'blur', 'sharpen', or 'unsharp'. They determine which filter is to be used
def filter(image_matrix, effect):
    
    image_object = Image.fromarray(image_matrix)
    
    # define sharpen and blur kernels
    sharpen_kernel = np.asarray([0, -1/3, 0, -1/3, 3, -1/3, 0, -1/3, 0])
    blur_kernel = np.asarray([1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9])
    unsharp_mask_kernel = (-1/256)* np.asarray([1, 4, 6, 4, 1, 4, 16, 24, 16, 4, 6, 24, -476, 24, 6, 4, 16, 24, 16, 4, 1, 4, 6, 4, 1])
    
    # convolve with kernels
    if effect == 'sharpen':
        img_sharpen = image_object.filter(ImageFilter.Kernel((3, 3), sharpen_kernel, scale=None))
        final_img = img_sharpen
        
        
    elif effect == 'blur':
        img_blur = image_object.filter(ImageFilter.Kernel((3, 3), blur_kernel, scale=None))
        final_img = img_blur
        
    elif effect == 'unsharp':
        img_unsharp = image_object.filter(ImageFilter.Kernel((5, 5), unsharp_mask_kernel, scale=None))
        final_img = img_unsharp
    
    # display image
#==============================================================================
#     final_img.show()
#     im = plt.imshow(final_img, cmap='gray')
#     plt.show()
#==============================================================================

    # return an image object of the filtered image, which can be feedback into the input again
    return np.asarray(final_img)

# for testing
#==============================================================================
# 
# image = 'Bikesgray.jpg'
# im = Image.open(image)
# im_arr = np.asarray(im)
# f1 = filter(im_arr, 'blur')
# f2 = filter(f1, 'unsharp')
# f3 = filter(f2, 'blur')
# f4 = filter(f3, 'unsharp')
# 
# 
#==============================================================================
