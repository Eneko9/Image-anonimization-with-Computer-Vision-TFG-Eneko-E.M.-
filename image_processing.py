import cv2
import numpy as np

def gaussBlur(img, kernel_size):
    # Apply Gaussian blur
    blur = cv2.GaussianBlur(img, (kernel_size, kernel_size), cv2.BORDER_DEFAULT)
    return blur
def medianBlur(img, kernel_size):
    # Apply a median blur
    img_blur = cv2.medianBlur(img, kernel_size)
    return img_blur

def bilateralFiter(img, diameter, sigmaColor, sigmaSpace):
    # Apply a bilateral filter with a diameter of 9, a sigmaColor of 75, and a sigmaSpace of 75
    img_filtered = cv2.bilateralFilter(img, diameter, sigmaColor, sigmaSpace)
    return img_filtered

def thresholding(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold with a threshold value of 127
    ret, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    return thresh

def histEquialization(img):
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(grayimg)
    return equ

def local_contrast_normalization(image, patch_size, epsilon=0.0001, scale=1):
    # Convertir la imagen en escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Dividir la imagen en parches
    height, width = gray_image.shape
    patches = []
    for i in range(0, height, patch_size):
        for j in range(0, width, patch_size):
            patch = gray_image[i:i+patch_size, j:j+patch_size]
            patches.append(patch)

    # Calcular la media y la desviación estándar de cada parche
    patch_means = [np.mean(patch) for patch in patches]
    patch_stddevs = [np.std(patch) for patch in patches]

    # Aplicar la normalización local de contraste en cada parche
    output_patches = []
    for i, patch in enumerate(patches):
        mean = patch_means[i]
        stddev = patch_stddevs[i]
        output_patch = ((patch - mean) / max(stddev, epsilon)) * scale + mean
        output_patches.append(output_patch)

    # Unir los parches para obtener la imagen de salida
    output_image = np.zeros_like(gray_image)
    index = 0
    for i in range(0, height, patch_size):
        for j in range(0, width, patch_size):
            output_image[i:i+patch_size, j:j+patch_size] = output_patches[index]
            index += 1

    return output_image

def contrast_stretching(image):
    # Convertir la imagen en escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calcular el valor mínimo y máximo de los píxeles en la imagen
    min_value = float(np.min(gray_image))
    max_value = float(np.max(gray_image))

    # Aplicar la fórmula de estiramiento de contraste en cada píxel de la imagen
    output_image = ((gray_image - min_value) / (max_value - min_value)) * 255

    # Convertir la imagen de salida a formato de 8 bits sin signo (uint8)
    output_image = cv2.convertScaleAbs(output_image)

    return output_image

def contrast_stretching_color(image):
    # Convertir la imagen de BGR a HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Dividir la imagen en sus canales de color
    hue, saturation, value = cv2.split(hsv_image)

    print("Valor mínimo antes del estiramiento del contraste:", np.min(value))
    print("Valor máximo antes del estiramiento del contraste:", np.max(value))

    if (hue.shape == saturation.shape == value.shape) and (hue.dtype == saturation.dtype == value.dtype):
        # Calcular el valor mínimo y máximo de los píxeles en el canal de valor (V)
        min_value = float(np.min(value))
        max_value = float(np.max(value))

        # Aplicar la fórmula de estiramiento de contraste en el canal de valor (V)
        value_stretched = ((value - min_value) / (max_value - min_value)) * 255


        # Convertir el canal de valor estirado a un formato de píxeles sin signo de 8 bits
        value_stretched = cv2.convertScaleAbs(value_stretched)

        # Combinar los canales de color para formar la imagen de salida
        hsv_image_stretched = cv2.merge([hue, saturation, value_stretched])

        print("Valor mínimo después del estiramiento del contraste:", np.min(value_stretched))
        print("Valor máximo después del estiramiento del contraste:", np.max(value_stretched))

        # Convertir la imagen de salida de HSV a BGR
        output_image = cv2.cvtColor(hsv_image_stretched, cv2.COLOR_HSV2BGR)
    else:
        # Si los canales de color no tienen el mismo tamaño o profundidad, se devuelve la imagen original
        print("Error")

    return output_image

def gammaAdjust(image,gamma):

    # Convertir a espacio de color RGB
    img2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Aplicar ajuste Gamma
    img_gamma = np.power(img2 / float(np.max(img2)), gamma)
    img_gamma = img_gamma * 255

    # Convertir de vuelta a BGR para mostrarla con OpenCV
    img_gamma = cv2.cvtColor(img_gamma.astype('uint8'), cv2.COLOR_RGB2BGR)

    return img_gamma