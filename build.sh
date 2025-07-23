#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --no-input

#!/usr/bin/env bash
# Exit on error
set -o errexit

# Chrome install dir
STORAGE_DIR=/opt/render/project/.render
CHROME_DIR=$STORAGE_DIR/chrome
CHROME_BIN=$CHROME_DIR/opt/google/chrome/google-chrome

if [[ ! -f "$CHROME_BIN" ]]; then
  echo "...Downloading Chrome"
  mkdir -p $CHROME_DIR
  cd $CHROME_DIR
  wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x google-chrome-stable_current_amd64.deb $CHROME_DIR
  rm google-chrome-stable_current_amd64.deb
else
  echo "...Using cached Chrome"
fi

# Set env variables so Django/Selenium can access Chrome
echo "export CHROME_BIN=$CHROME_BIN" >> ~/.bashrc
echo "export PATH=$CHROME_DIR:$PATH" >> ~/.bashrc

# Install Python dependencies
pip install -r requirements.txt


python manage.py migrate