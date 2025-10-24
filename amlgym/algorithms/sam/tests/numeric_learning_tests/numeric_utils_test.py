"""Tests for numeric_utils.py"""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

from sam_learning.core.numeric_learning.numeric_utils import (
    extract_numeric_linear_coefficient,
    construct_projected_variable_strings,
    extended_gram_schmidt,
    create_monomials,
    create_polynomial_string,
    reduce_complementary_conditions_from_convex_hull,
    remove_complex_linear_dependencies,
)


def test_extract_numeric_linear_coefficient_does_not_output_infinity_for_zero_division():
    """Test that the function does not output infinity for zero division."""
    try:
        extract_numeric_linear_coefficient(pd.Series([1, 2, 3]), pd.Series([0, 0, 0]))
    except ZeroDivisionError:
        assert False


def test_extract_numeric_linear_coefficient_outputs_correct_coefficient_when_division_is_legal():
    """Test that the function outputs the correct coefficient when the division is legal."""
    assert extract_numeric_linear_coefficient(pd.Series([1, 2, 3]), pd.Series([1, 2, 3])) == 1


def test_construct_projected_variable_strings_returns_correct_strings_representing_the_projected_format():
    function_variables = ["(x)", "(y)", "(z)"]
    X = np.array([[-1, -1, 1], [-2, -1, 3], [-3, -2, 23], [1, 1, 31], [2, 1, 12], [3, 2, 7]])
    pca = PCA(n_components=2)
    pca.fit(X)

    pca_variable_strings = construct_projected_variable_strings(function_variables, pca.mean_, pca.components_)
    print(pca_variable_strings)
    assert len(pca_variable_strings) == 2  # 2 components


def test_construct_projected_variable_strings_returns_correct_strings_representing_the_projected_format_example_for_nsam_paper():
    function_variables = ["(x)", "(y)", "(z)", "w"]
    X = np.array([[1, 0, 17, 3], [5, 5, 7, 3], [2, 4, 9, 7]])
    shift = np.array([-1, 2, 3, 12])

    pca_variable_strings = construct_projected_variable_strings(function_variables, shift, X)
    print(f"x' = {pca_variable_strings[0]}")
    print(f"y' = {pca_variable_strings[1]}")
    print(f"z' = {pca_variable_strings[2]}")

    diagonal_eye = [list(vector) for vector in np.eye(X.shape[1])]
    orthnormal_span = extended_gram_schmidt(diagonal_eye, [[1, 0, 17, 3], [5, 5, 7, 3], [2, 4, 9, 7]])
    print(f"orthnormal_span = {orthnormal_span}")


def test_construct_projected_variable_strings_returns_correct_strings_representing_the_projected_format_when_components_are_equal_to_variables():
    function_variables = ["(x)", "(y)", "(z)"]
    X = np.array([[-1, -1, 1], [-2, -1, 3], [-3, -2, 23], [1, 1, 31], [2, 1, 12], [3, 2, 7]])
    pca = PCA(n_components=3)
    pca.fit(X)

    pca_variable_strings = construct_projected_variable_strings(function_variables, pca.mean_, pca.components_)
    assert len(pca_variable_strings) == 3  # 3 components
    print(pca_variable_strings)


def test_construct_projected_variable_strings_returns_correct_numbers_according_to_construction_calculation_for_simple_case():
    function_variables = ["(x)", "(y)", "(z)"]
    mean = np.array([2, 2, 2])
    pca_components = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    pca_variable_strings = construct_projected_variable_strings(function_variables, mean, pca_components)
    assert len(pca_variable_strings) == 3  # 3 components
    assert pca_variable_strings[0] == "(- (x) 2)"
    assert pca_variable_strings[1] == "(- (y) 2)"
    assert pca_variable_strings[2] == "(- (z) 2)"
    print(pca_variable_strings)


def test_construct_pca_variable_strings_returns_correct_numbers_according_to_construction_calculation_for_complex_case():
    function_variables = ["(x)", "(y)", "(z)"]
    mean = np.array([2, 2, 2])
    pca_components = np.array([[1, 8, 32.5], [12, 1, 33], [3, 2, 1]])

    pca_variable_strings = construct_projected_variable_strings(function_variables, mean, pca_components)
    assert len(pca_variable_strings) == 3  # 3 components
    assert pca_variable_strings[0] == "(+ (- (x) 2) (+ (* (- (y) 2) 8) (* (- (z) 2) 32.5)))"
    assert pca_variable_strings[1] == "(+ (* (- (x) 2) 12) (+ (- (y) 2) (* (- (z) 2) 33)))"
    assert pca_variable_strings[2] == "(+ (* (- (x) 2) 3) (+ (* (- (y) 2) 2) (- (z) 2)))"


def test_extended_gram_schmidt_on_no_shift_base_returns_correct_lower_dimensional_points():
    projections = extended_gram_schmidt([[0, 0, 0], [0, 1, 0], [1, 0, 0]])
    assert len(projections) == 2
    assert projections == [[0, 1, 0], [1, 0, 0]]


def test_extended_gram_schmidt_on_no_shift_base_returns_correct_lower_dimensional_points_with_correct_rational_values():
    projections = extended_gram_schmidt([[0, 0, 0], [0, 1, 1], [0, 1, -1]])
    normalized_projection = []
    for vector in projections:
        normalized_projection.append([round(val, 3) for val in vector])

    assert len(projections) == 2
    assert normalized_projection == [[0, 0.707, 0.707], [0, 0.707, -0.707]]


def test_extended_gram_schmidt_on_no_shift_when_given_orthonormal_partial_base_returns_complementary_base_to_points():
    projections = extended_gram_schmidt([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[0, 1, 0], [1, 0, 0]])
    assert len(projections) == 1
    assert projections == [[0, 0, 1]]


def test_extended_gram_schmidt_on_no_shift_with_base_correctly_returns_the_missing_vector():
    projections = extended_gram_schmidt([[0, 0, 0], [0, 1, 1], [0, 1, -1]])
    extended_standard_base = np.concatenate((np.eye(3), np.array(projections)), axis=0).tolist()
    complementary_projection = extended_gram_schmidt(extended_standard_base, projections)
    assert len(complementary_projection) == 1
    assert complementary_projection == [[1, 0, 0]]


def test_extended_gram_schmidt_on_no_shift_with_base_correctly_returns_the_missing_vector_with_more_complicated_setting():
    projections = extended_gram_schmidt([[0, 0, 0], [0, 1, 1], [0, 1, -1]])
    extended_standard_base = [[18, 2, 19], [2, 7, 1], [29, 31, -1]]
    complementary_projection = extended_gram_schmidt(extended_standard_base, projections)
    assert len(complementary_projection) == 1
    assert complementary_projection == [[1.0, -9.868649107779169e-17, 0.0]]


def test_extended_gram_schmidt_on_no_shift_with_base_with_more_rows_than_columns_still_returns_2x2_output():
    projections = extended_gram_schmidt([[-19.0, 32.0], [14.0, 52.0], [28.0, 12.0], [-7.0, 13.0]])
    assert len(projections) == 2
    assert all([len(vector) == 2 for vector in projections])
    assert np.sum(np.array(projections) - np.array([[-0.510538754155436, 0.859854743840735], [0.859854743840735, 0.510538754155436]])) < 0.0001
    print(projections)


def test_extended_gram_schmidt_when_one_variable_is_a_constant_extract_the_constant_and_return_orthonormal_base():
    # no need to add a non-zero constant since subtracting from the first sample will result in a zero vector
    projections = extended_gram_schmidt([[8, 2, 0], [72, 33, 0], [11, 8, 0], [1, 1, 0], [17, 13, 0]])
    assert len(projections) == 2


def test_extended_gram_schmidt_with_no_base_returns_correct_orthonormal_matrix():
    projections = extended_gram_schmidt([[1, 1, 1], [2, 1, 0], [5, 1, 3]])
    assert len(projections) == 3
    assert (
        np.sum(
            np.array(projections)
            - np.array(
                [
                    [0.577350269189626, 0.577350269189626, 0.577350269189626],
                    [0.707106781186548, 0, -0.707106781186548],
                    [0.408248290463863, -0.816496580927726, 0.408248290463863],
                ]
            )
        )
        < 0.0001
    )


def test_extended_gram_schmidt_with_paper_example_returns_correct_values():
    projections = extended_gram_schmidt([[0, 0, 0], [-1, 1, 0], [-1, 0, 1]])
    print(projections)
    assert len(projections) == 2


def test_reduce_complementary_conditions_from_convex_hull_basis_can_eliminate_values_when_computing_complementary_basis_with_constant_value():
    test_values = [[np.random.randint(0, 100), np.random.randint(0, 100), 0] for _ in range(10)]
    projections = extended_gram_schmidt(test_values)
    diagonal_eye = [list(vector) for vector in np.eye(3)]
    complementary_basis = extended_gram_schmidt(diagonal_eye, projections)
    result = reduce_complementary_conditions_from_convex_hull(projections, complementary_basis)
    assert result == projections


def test_reduce_complementary_conditions_from_convex_hull_basis_can_eliminate_values_when_computing_complementary_basis_with_linear_dependent_value():
    test_values = [[i, 2 * i, np.random.randint(0, 100)] for i in range(10)]
    projections = extended_gram_schmidt(test_values)
    diagonal_eye = [list(vector) for vector in np.eye(3)]
    complementary_basis = extended_gram_schmidt(diagonal_eye, projections)
    result = reduce_complementary_conditions_from_convex_hull(projections, complementary_basis)
    for index, projection in enumerate(result):
        assert projection[0] == 0
        assert projection[1] == 0.5 * projections[index][0] + projections[index][1]


def test_create_monomials_creates_correct_monomials_when_given_polynom_degree_one():
    test_functions = ["(fuel-cost )", "(load_limit ?z)", "(current_load ?z)"]
    monomials = create_monomials(test_functions, polynom_degree=1)
    assert len(monomials) == 3 + 3
    assert sum([len(monomial) for monomial in monomials]) == 3 + 3 * 2


def test_create_monomials_creates_correct_monomials_when_given_polynom_degree_zero():
    test_functions = ["(fuel-cost )", "(load_limit ?z)", "(current_load ?z)"]
    monomials = create_monomials(test_functions, polynom_degree=0)
    assert len(monomials) == 3


def test_create_monomials_creates_correct_monomials_when_given_polynom_degree_two():
    test_functions = ["(fuel-cost )", "(load_limit ?z)", "(current_load ?z)"]
    monomials = create_monomials(test_functions, polynom_degree=2)
    assert len(monomials) == 3 + 3 + 3
    print(monomials)


def test_create_polynomial_string_when_calling_with_a_single_function_returns_the_function_string():
    monomial = ["(fuel-cost )"]
    polynomial_string = create_polynomial_string(monomial)
    assert polynomial_string == "(fuel-cost )"


def test_create_polynomial_string_when_calling_with_two_functions_returns_the_multiplication_of_the_two_functions():
    monomial = ["(fuel-cost )", "(load_limit ?z)"]
    polynomial_string = create_polynomial_string(monomial)
    assert polynomial_string == "(* (fuel-cost ) (load_limit ?z))"


def test_create_polynomial_string_when_calling_with_three_functions_returns_the_multiplication_of_the_three_functions():
    monomial = ["(fuel-cost )", "(load_limit ?z)", "(current_load ?z)"]
    polynomial_string = create_polynomial_string(monomial)
    assert polynomial_string == "(* (fuel-cost ) (* (load_limit ?z) (current_load ?z)))"


def test_remove_complex_linear_dependencies_returns_correct_conditions_and_reduced_dataframe_when_one_feature_in_the_dataframe_is_constant_value():
    test_data = pd.DataFrame({"a": [1, 1, 1, 1], "b": [1, 3, 3, 4], "c": [1, 2, 3, 4]})
    reduced_data, conditions = remove_complex_linear_dependencies(test_data)
    assert len(conditions) == 1
    assert conditions[0] == "(= a 1)"
    assert len(reduced_data.columns) == 2
    assert "a" not in reduced_data.columns


def test_remove_complex_linear_dependencies_returns_correct_conditions_and_reduced_dataframe_when_one_feature_equals_the_assignment_of_two_others_and_a_const():
    test_data = pd.DataFrame({"a": [1, 2, 3, 4], "b": [1, 3, 3, 4], "c": [3, 6, 7, 9]})
    reduced_data, conditions = remove_complex_linear_dependencies(test_data)
    assert len(conditions) == 1
    assert conditions[0] == "(= a (+ (* b -1) (+ c -1)))"
    assert len(reduced_data.columns) == 2
    assert "a" not in reduced_data.columns


def test_remove_complex_linear_dependencies_returns_correct_conditions_and_reduced_dataframe_when_one_feature_equals_the_assignment_of_two_others_and_a_const_and_there_is_a_const_column():
    test_data = pd.DataFrame({"a": [1, 2, 3, 4], "b": [1, 3, 3, 4], "c": [3, 6, 7, 9], "d": [1, 1, 1, 1]})
    reduced_data, conditions = remove_complex_linear_dependencies(test_data)
    assert len(conditions) == 2
    assert set(conditions) == {"(= a (+ (* b -1) (+ c -1)))", "(= d 1)"}
    assert len(reduced_data.columns.tolist()) == 2
    assert "a" not in reduced_data.columns.tolist()


def test_remove_complex_linear_dependencies_when_all_columns_are_constant_values_returns_empty_dataframe_and_the_pddl_constraint_that_checks_the_column_name_is_equal_to_the_constant():
    test_data = pd.DataFrame({"a": [1, 1, 1, 1], "b": [1, 1, 1, 1], "c": [1, 1, 1, 1]})
    reduced_data, conditions = remove_complex_linear_dependencies(test_data)
    assert len(conditions) == 3
    assert conditions == ["(= a 1)", "(= b 1)", "(= c 1)"]
    assert len(reduced_data.columns) == 0
