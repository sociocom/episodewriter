# Use the official Node.js 14 image as the base image
FROM node:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the Vue application
RUN npm run build

# Expose the container's port (change it if necessary)
EXPOSE 80

# Define the command to run the application
CMD [ "npm", "run", "dev"]