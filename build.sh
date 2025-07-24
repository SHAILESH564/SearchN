#!/usr/bin/env bash
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

python manage.py collectstatic --no-input

# Download Google Chrome
echo "🔧 Installing Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -x google-chrome-stable_current_amd64.deb chrome/
rm google-chrome-stable_current_amd64.deb

# Set Chrome binary path (this will be used in Chrome options)
export CHROME_BIN=$PWD/chrome/opt/google/chrome/google-chrome

# Download Chromedriver (matching Chrome version)
echo "🔧 Installing Chromedriver..."
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget -N https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/chromedriver

# Migrate DB
python manage.py migrate