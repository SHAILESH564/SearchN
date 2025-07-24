#!/usr/bin/env bash
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Set paths
STORAGE_DIR=/opt/render/project/.render
CHROME_DIR=$STORAGE_DIR/chrome
CHROME_BIN=$CHROME_DIR/opt/google/chrome/google-chrome

# Download Chrome
if [[ ! -d $CHROME_DIR ]]; then
  echo "🔧 Downloading Chrome..."
  mkdir -p $CHROME_DIR
  cd $CHROME_DIR
  wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x google-chrome-stable_current_amd64.deb .
  rm google-chrome-stable_current_amd64.deb
  cd -
else
  echo "✅ Chrome already downloaded."
fi

# Download Chromedriver (known working version: 114.0.5735.90)
if [[ ! -f /usr/local/bin/chromedriver ]]; then
  echo "🔧 Downloading Chromedriver..."
  wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
  unzip -q chromedriver_linux64.zip
  rm chromedriver_linux64.zip
  chmod +x chromedriver
  mv chromedriver /usr/local/bin/
else
  echo "✅ Chromedriver already installed."
fi

# Export Chrome binary path for Selenium
export CHROME_BIN=$CHROME_BIN
export PATH=$PATH:/usr/local/bin

# Apply DB migrations
python manage.py migrate
