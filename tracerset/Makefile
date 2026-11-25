test:
	pytest -sv
	
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "outputs" -exec rm -rf {} +
	find . -type f \( -name "*.tmp" -o -name "*.svg" -o -name "*.png" -o -name "*.json*" -o -name "*.dot" -o -name "*.cov*" -o -name "*.htm*" -o -name "*.gv" \) -delete
	find . -type d \( -name ".pytest_cache" -o -name ".complexipy_cache" \) -exec rm -rf {} +	
