#!/bin/bash

# Install Node.js and npm (if not already installed)
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Installing..."
    curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Create a directory for your Next.js project
mkdir my-nextjs-app
cd my-nextjs-app

# Initialize a new Node.js project
npm init -y

# Install Next.js and React
npm install next react react-dom

# Create a pages directory for your Next.js pages
mkdir pages

# Create a sample index.js page
echo "function HomePage() {
  return <div>Welcome to Next.js!</div>;
}
export default HomePage;" > pages/index.js

# Add the "dev" script to package.json
cat > package.json <<EOF
{
  "name": "my-nextjs-app",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev"
  }
}
EOF

# Start the Next.js development server
npm run dev
