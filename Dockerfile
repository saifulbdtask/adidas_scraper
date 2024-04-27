# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV TWISTED_REACTOR twisted.internet.asyncioreactor.AsyncioSelectorReactor

# Run the spider when the container launches
CMD ["scrapy", "crawl", "adidas", "-o", "products.csv"]