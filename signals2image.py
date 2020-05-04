import matplotlib.pyplot as plt
import cv2


def array2img(array, directory='.'):
    for count, i in enumerate(array):
        filename = directory + '/' + str(count) + '.png'
        sig2img(i, filename)


def sig2img(sig, img_path, resize=True):
    """
    plot the signal and save the image.

    :param sig: List[float]
    :param img_path: str. path/to/save/the/img
    :param resize: Bool, resize or not.
    :return: None
    """

    fig = plt.figure(frameon=False)

    plt.plot(sig)
    plt.xticks([]), plt.yticks([])

    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    fig.savefig(img_path)

    if resize:
        im_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        im_gray = cv2.resize(im_gray, (128, 128), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(img_path, im_gray)
