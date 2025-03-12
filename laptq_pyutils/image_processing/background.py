import cv2
from tqdm import tqdm
from abc import ABC, abstractmethod
import numpy as np
import torch

from laptq_pyutils.log import load_logger


LOGGER = load_logger()


class BackgroundCreatorBase(ABC):

    def process(self, img):

        self._process(img)

        return self.background

    @abstractmethod
    def _process(self, img, **kwargs):
        pass


class BackgroundCreatorAddWeighted(BackgroundCreatorBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.weight = kwargs["weight"]  # 0.95
        self.background = None

    def _process(self, img):

        if self.background is None:
            self.background = img
            return

        self.background = cv2.addWeighted(
            self.background, self.weight, img, 1 - self.weight, 0
        )


class BackgroundCreatorFirstKFrames(BackgroundCreatorBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.k = kwargs["k"]

        self.background = None
        self.list__seeding_background = []

    def _process(self, img):

        if len(self.list__seeding_background) < self.k:
            self.list__seeding_background.append(img)

            self.background = np.mean(self.list__seeding_background, axis=0).astype(
                np.uint8
            )


class BackgroundCreatorMovingMedian(BackgroundCreatorBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.k = kwargs["k"]
        self.backend = kwargs["backend"]
        self.device = kwargs.get("device", None)
        self.list__seeding_background = None

        assert self.backend in ["numpy", "torch"]
        if self.backend == "torch":
            assert self.device is not None, "Please provide device for torch backend."

    def _process(self, img):

        LOGGER.bind(classname=self.__class__.__name__).warning(
            "This class is not optimized. It runs very slow."
        )

        if self.backend == "numpy":
            self._process_numpy(img)
        elif self.backend == "torch":
            self._process_torch(img)

    def _process_numpy(self, img):

        if self.list__seeding_background is None:
            self.list__seeding_background = []

        if len(self.list__seeding_background) == self.k:
            self.list__seeding_background.pop(0)
        self.list__seeding_background.append(img)

        self.background = np.median(self.list__seeding_background, axis=0).astype(
            np.uint8
        )

    def _process_torch(self, img):

        if self.list__seeding_background is None:
            self.list__seeding_background = torch.empty(
                (self.k, *img.shape), dtype=torch.float32
            ).to(self.device)
            self.index__earliest = 0
            self.count = 0

        self.list__seeding_background[self.index__earliest] = torch.from_numpy(img).to(
            self.device
        )
        self.index__earliest = (self.index__earliest + 1) % self.k

        if self.count < self.k:
            self.count += 1

        self.background = (
            torch.median(self.list__seeding_background[: self.count], dim=0)
            .values.cpu()
            .numpy()
            .astype(np.uint8)
        )


class BackgroundSubtractorBase(ABC):

    def process(self, background, img):

        return self._process(background, img)

    @abstractmethod
    def _process(self, background, img):
        pass


class BackgroundSubtractorGrayDiff(BackgroundSubtractorBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _process(self, background, img):

        bg_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(bg_gray, img_gray)

        return diff


createBackgroundSubtractorMOG2 = cv2.createBackgroundSubtractorMOG2
createBackgroundSubtractorKNN = cv2.createBackgroundSubtractorKNN
