#!/bin/sh

#install homebrew 
echo 'installing homebrew'
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
echo 'tapping cask'
brew tap caskroom/cask

#install psql
echo 'installing psql'
brew install postgres

#setup rsa for aws access
echo 'generating ssh keys'
ssh-krygen -t rsa

#install pip and virtualenv
echo 'installing pip'
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

sudo python get-pip.py

echo 'installing virtualenv'

sudo pip install virtualenv

#setup core

echo 'setting up core'
mkdir git

cd git

virtualenv achcore

git clone https://github.com/sjsu-achilis/core.git

cd core

source ../achcore/bin/activate

sudo pip install -r requirements.txt

#setup iterm2, vscode and slack
echo 'installing slack'
brew cask install slack

echo 'installing vscode'
brew cask install visual-studio-code

echo 'installing iterm2'
brew cask install iterm2

echo 'installing postman'
brew cask install postman

echo 'all done...please goto docker site and installdocker for mac and you are all set'
