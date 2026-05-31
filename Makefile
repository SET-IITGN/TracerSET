test:
	pytest -sv
	
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f \( -name "*.tmp" -o -name "*.svg" -o -name "*.dot" -o -name "*.cov*" -o -name "*.htm*" -o -name "*.gv" \) -delete
	rm -rf dist tracerset.egg-info
