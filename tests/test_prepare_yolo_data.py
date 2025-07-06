import pytest
from src.data.prepare_yolo_data import convert_bbox_to_yolo_format

def test_convert_bbox_to_yolo_format():
    """
    Tests the bounding box conversion logic.
    """
    # Define a sample bounding box [xmin, ymin, xmax, ymax] and image dimensions
    img_width = 1000
    img_height = 800
    box = [200, 100, 400, 300]  # An example box

    # Expected YOLO format values
    expected_x_center = (200 + 400) / 2 / img_width
    expected_y_center = (100 + 300) / 2 / img_height
    expected_width = (400 - 200) / img_width
    expected_height = (300 - 100) / img_height

    # Call the function
    x_center, y_center, width, height = convert_bbox_to_yolo_format(box, img_width, img_height)

    # Assert that the results are close to the expected values
    assert x_center == pytest.approx(expected_x_center)
    assert y_center == pytest.approx(expected_y_center)
    assert width == pytest.approx(expected_width)
    assert height == pytest.approx(expected_height)

def test_convert_bbox_to_yolo_format_at_edge():
    """
    Tests the bounding box conversion for a box at the edge of the image.
    """
    img_width = 1000
    img_height = 800
    box = [0, 0, 1000, 800]  # Box covers the entire image

    # Expected YOLO format values should be center (0.5, 0.5) and size (1.0, 1.0)
    expected_x_center = 0.5
    expected_y_center = 0.5
    expected_width = 1.0
    expected_height = 1.0

    # Call the function
    x_center, y_center, width, height = convert_bbox_to_yolo_format(box, img_width, img_height)

    # Assert that the results are correct
    assert x_center == pytest.approx(expected_x_center)
    assert y_center == pytest.approx(expected_y_center)
    assert width == pytest.approx(expected_width)
    assert height == pytest.approx(expected_height) 