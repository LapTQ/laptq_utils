import numpy as np
from tqdm import tqdm


class KMeans:

    def __init__(self, **kwargs):
        self.n_clusters = kwargs["n_clusters"]
        self.max_iter = kwargs.get("max_iter", 300)
        self.tol = kwargs.get("tol", 1e-4)
        self.random_state = kwargs.get("random_state", None)
        self.fn__distance = kwargs["fn__distance"]
        self.fn__update_centroids = kwargs["fn__update_centroids"]

    def fit(self, X):

        self.cluster_centers_ = self._init__centroids(X)

        for _ in tqdm(range(self.max_iter), desc="KMeans Clustering"):

            labels = self._assign_labels(X)
            new_centroids = self._update_centroids(X, labels)

            if self.fn__distance(self.cluster_centers_, new_centroids).all() < self.tol:
                break

            self.cluster_centers_ = new_centroids

        return self

    def _init__centroids(self, X):
        np.random.seed(self.random_state)
        centroids = X[np.random.choice(X.shape[0], self.n_clusters, replace=False)]
        return centroids

    def _assign_labels(self, X):
        distances = self.fn__distance(X, self.cluster_centers_)
        argmin = np.argmin(distances, axis=1)
        return argmin

    def _update_centroids(self, X, labels):
        new_centroids = np.zeros_like(self.cluster_centers_)
        for i in range(self.n_clusters):
            new_centroids[i] = self.fn__update_centroids(X[labels == i])
        return new_centroids
