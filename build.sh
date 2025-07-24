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
BIN_DIR=$STORAGE_DIR/bin

mkdir -p $BIN_DIR

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

# Download Chromedriver (fixed version)
if [[ ! -f $BIN_DIR/chromedriver ]]; then
  echo "🔧 Downloading Chromedriver..."
  wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
  unzip -q chromedriver_linux64.zip
  rm chromedriver_linux64.zip
  chmod +x chromedriver
  mv chromedriver $BIN_DIR/
else
  echo "✅ Chromedriver already installed."
fi

# Export paths for use during app runtime
export PATH=$BIN_DIR:$PATH
export CHROME_BIN=$CHROME_BIN

# Apply DB migrations
python manage.py migrate
