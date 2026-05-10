test:
	pytest -sv
	
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.dot" -type f -delete
	find . -name "*.cov*" -type f -delete
