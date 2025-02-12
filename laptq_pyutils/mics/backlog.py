from abc import ABC, abstractmethod
import cv2
import numpy as np


class FGEnhancer(ABC):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.enable = kwargs["enable"]

    def process(self, mask):
        if not self.enable:
            return mask

        self.mask = mask
        self._process()

        return self.mask

    @abstractmethod
    def _process(self):
        pass


class FGEnhancerThreshold(FGEnhancer):
    def _process(self):

        type_ = self.kwargs["type_"]
        threshold = self.kwargs["threshold"]

        if type_ == cv2.THRESH_BINARY + cv2.THRESH_OTSU:
            threshold = 0

        _, self.mask = cv2.threshold(self.mask, threshold, 255, type_)


class FGEnhancerThresholdMorphology(FGEnhancerThreshold):

    def _process(self):
        super()._process()

        self.morph()

    def morph(self):

        kernel_size = self.kwargs["kernel_size"]
        iterations__opening = self.kwargs["iterations__opening"]
        iterations__closing = self.kwargs["iterations__closing"]

        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.mask = cv2.morphologyEx(
            self.mask, cv2.MORPH_OPEN, kernel, iterations=iterations__opening
        )
        self.mask = cv2.morphologyEx(
            self.mask, cv2.MORPH_CLOSE, kernel, iterations=iterations__closing
        )


class FGEnhancerMorphologyThreshold(FGEnhancerThreshold):

    def _process(self):
        self.morph()
        
        super()._process()


    def morph(self):

        kernel_size = self.kwargs["kernel_size"]
        iterations__opening = self.kwargs["iterations__opening"]
        iterations__closing = self.kwargs["iterations__closing"]

        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.mask = cv2.morphologyEx(
            self.mask, cv2.MORPH_OPEN, kernel, iterations=iterations__opening
        )
        self.mask = cv2.morphologyEx(
            self.mask, cv2.MORPH_CLOSE, kernel, iterations=iterations__closing
        )


def to__bgr(img):
    if len(img.shape) == 3:
        return img
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


class ForegroundMasker:

    def __init__(self, background__creator, foreground__creator):
        self.background__creator = background__creator
        self.foreground__creator = foreground__creator

    def apply(self, img):
        background = self.background__creator.process(img)
        foreground = self.foreground__creator.process(background, img)

        return background, foreground


def detect_from_mask(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    list__obj__box_x1y1wh__fg = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        list__obj__box_x1y1wh__fg.append([x, y, w, h])
    return list__obj__box_x1y1wh__fg