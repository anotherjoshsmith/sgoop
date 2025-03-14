import numpy as np
from sgoop.analysis import gaussian_density_estimation
from sgoop.analysis import histogram_density_estimation
from sgoop.analysis import find_closest_points
from sgoop.analysis import avg_neighbor_transitions
from sgoop.analysis import probability_matrix
from sgoop.analysis import sorted_eigenvalues
from sgoop.analysis import spectral_gap


def test_gaussian_denisty_estimation():
    samples = np.array([0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
    weights = None

    # bandwidth too small for Gaussians to overlap
    actual = gaussian_density_estimation(samples, weights, samples[:5], bw=0.001)
    assert np.all(actual[actual == actual[0]])

    # bandwidth large enough for Gaussians to overlap
    actual = gaussian_density_estimation(samples, weights, samples[:5], bw=0.5)
    expected = np.array([[0.18122683, 0.20282322, 0.20287675, 0.20282322, 0.18122683]])
    assert np.allclose(actual, expected)

    # weighted samples with overlapping Gaussians
    weights = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5])
    actual = gaussian_density_estimation(samples, weights, samples[:5], bw=0.5)
    expected = np.array([0.06764343, 0.13525117, 0.20287675, 0.27039527, 0.29481024])
    assert np.allclose(actual, expected)


def test_histogram_density_estimation():
    samples = np.array([0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
    weights = None
    bins = 3

    # unweighted histogram (probability mass function)
    actual_hist, actual_edges = histogram_density_estimation(samples, weights, bins)
    expected_hist = np.array([0.3, 0.15, 0.3])
    expected_edges = np.array([0.0, 1.33333333, 2.66666667, 4.0])
    assert np.allclose(actual_hist, expected_hist)
    assert np.allclose(actual_edges, expected_edges)

    # weighted histogram (probability mass function)
    weights = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5])
    actual_hist, actual_edges = histogram_density_estimation(samples, weights, bins)
    expected_hist = np.array([0.15, 0.15, 0.45])
    expected_edges = np.array([0.0, 1.33333333, 2.66666667, 4.0])
    assert np.allclose(actual_hist, expected_hist)
    assert np.allclose(actual_edges, expected_edges)


def test_find_closest_points():
    sequence = np.array([0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
    points = np.array([0.7, 1.4, 2.1, 2.8])
    actual = find_closest_points(sequence, points)
    expected = np.array([0, 0, 2, 3, 3, 0, 0, 2, 3, 3])

    assert len(actual) == len(sequence)
    assert np.allclose(actual, expected)


def test_avg_neighbor_transitions():
    sequence = np.array([0, 0, 2, 3, 3, 0, 0, 2, 3, 3])
    # calc transitions for 1 nearest neighbor
    actual = avg_neighbor_transitions(sequence, 1)
    expected = 0.6666666666666666
    assert np.allclose(actual, expected)

    actual = avg_neighbor_transitions(sequence, 5)
    expected = 1.0
    assert np.allclose(actual, expected)


def test_probability_matrix():
    p = np.array([0.06764343, 0.13525117, 0.20287675, 0.27039527, 0.29481024])
    # test that diagonal elements are nonnegative
    matrix = probability_matrix(p, 1)
    actual_diag_0 = np.diagonal(matrix)
    assert np.all(actual_diag_0 > 0.0)
    # test off diagonal elements negative and equal to expected
    actual_diag_1 = np.diagonal(matrix, offset=1)
    expected_diag_1 = np.array(
        [-0.45458505479, -0.52484037126, -0.55678746909, -0.61560355788]
    )
    assert np.all(actual_diag_1 < 0.0)
    assert np.allclose(actual_diag_1, expected_diag_1)


def test_sorted_eigenvalues():
    matrix = np.array(
        [
            [0.908930, -0.454585, 0.0, 0.0, 0.0],
            [-0.908930, 1.24184, -0.524840, 0.0, 0.0],
            [0.0, -0.787260, 1.26692, -0.556787, 0.0],
            [0.0, 0.0, -0.742089, 1.22797, -0.615603],
            [0.0, 0.0, 0.0, -0.671188, 0.615603],
        ]
    )
    # test that eigenvalues are calculated as expected
    actual = sorted_eigenvalues(matrix)
    expected = np.array(
        [-3.96933961e-06, 3.17075011e-01, 9.51439139e-01, 1.68900194e00, 2.30375088e00]
    )
    assert np.allclose(actual, expected)
    assert np.isclose(np.exp(-actual[0]), 1.0)


def test_spectral_gap():
    eigenvalues = np.array(
        [-3.96933961e-06, 3.17075011e-01, 9.51439139e-01, 1.68900194e00, 2.30375088e00]
    )

    actual = spectral_gap(eigenvalues, 2)
    expected = 0.3420912746899744
    assert np.allclose(actual, expected)
