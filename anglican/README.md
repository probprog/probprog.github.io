Anglican homepage
=================

Anglican homepage on probprog.github.io/anglican, made using jekyll, bootstrap and jekyll-scholar (for bibtex publication list).

Build instructions
------------------

    git checkout development
    make


FAQ
---

1. How to run locally?

        gem install jekyll jekyll-scholar jekyll-assets kramdown wdm

        jekyll serve --watch --baseurl=

2. The most recent version of xcode / clang on OSX will give compiler errors if you try to install jekyll using the instructions on jekyll's website (i.e. via "gem install").
If you have this issue, you can work around it by setting an additional compiler flag, like so:
        
        sudo ARCHFLAGS="-Wno-error=unused-command-line-argument-hard-error-in-future" gem install jekyll
There is some discussion, as well as a "one-liner" which will patch your system ruby configuration so that you'll be able to compile rubygems (this worked for Brooks, at least), here:

        http://stackoverflow.com/questions/22352838/ruby-gem-install-json-fails-on-mavericks-and-xcode-5-1-unknown-argument-mul


3. To run the plots, you need both `feedgnuplot` and `gnuplot` itself. On ubuntu, these are both available via apt-get (try `sudo apt-get install feedgnuplot`).
On OSX, gnuplot can be installed via homebrew (`brew install gnuplot`).
The feedgnuplot script requires perl modules `IPC::Run` and `String::ShellQuote`, both of which can be installed with the CPAN package manager.
