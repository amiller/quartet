import numpy as np
import UnionFind
import MinimumSpanningTree
from rtmodel import pointmodel
from rtmodel.rangeimage import RangeImage
from rtmodel.camera import kinect_camera

def compute_all_mappings(points_in_sets, nodes=range(5)):
    # TODO: estimate the nodes from the values in points_in_sets?
    # Measure the error associated with each pairwise estimation
    adj = dict(enumerate([dict(enumerate([float('inf') for v in nodes])) for u in nodes]))
    mats = [[None for v in nodes] for u in nodes]
    for points_in_set in points_in_sets:
        for cam0,depth0,points0 in points_in_set:
            for cam1,depth1,points1 in points_in_set:
                mat,mse = estimate_rotation((depth0, points0), (depth1, points1))
                if mse < adj[cam0][cam1]:
                    adj[cam0][cam1] = mse
                    mats[cam0][cam1] = mat

    # Find the shortest paths tree (in the sense of additive MSE)
    tree = MinimumSpanningTree.MinimumSpanningTree(adj)

    # Populate the shortest paths matrix O(n^3) is fine when n=5
    final = [[None for v in nodes] for u in nodes]
    for u in nodes: final[u][u] = np.eye(4)
    import copy
    for root in nodes:
        edges = copy.copy(tree)
        while edges:
            for e0,e1 in edges:
                if final[root][e0] is not None and final[root][e1] is None:
                    final[root][e1] = np.linalg.inv(np.dot(np.linalg.inv(mats[e0][e1]), np.linalg.inv(final[root][e0])))
                    edges.remove((e0,e1))
                    break
                if final[root][e1] is not None and final[root][e0] is None:
                    final[root][e0] = np.linalg.inv(np.dot(np.linalg.inv(mats[e1][e0]), np.linalg.inv(final[root][e1])))
                    edges.remove((e0,e1))
                    break
    return final

def estimate_rotation((depth0, points0), (depth1, points1)):
    def metric_points(depth, points):
        assert len(points) == 3
        assert depth.dtype == np.uint16
        rimg = RangeImage(depth, kinect_camera())
        rimg.compute_points()
        pts = []
        for x,y in points:
            pts.append(rimg.xyz[y,x,:])
        pts = np.concatenate((pts,pts))
        assert pts.shape == (6,3)
        return pts

    import transformations
    v0 = metric_points(depth0, points0)
    v1 = metric_points(depth1, points1)
    mat = transformations.affine_matrix_from_points(v0.T,v1.T,shear=False,scale=False)
    err = (np.dot(mat[:3,:3],v0.T).T + mat[:3,3].T) - v1
    mse = np.mean(np.power(err,2))
    mat = np.linalg.inv(mat)
    return mat, mse
