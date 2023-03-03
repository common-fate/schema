generate:
	poetry run pytest
	poetry run jsonschema-to-openapi output/provider/v1alpha1 output/provider/v1alpha1-openapi