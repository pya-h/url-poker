# Poker App
# Language: Python
Simple poker app for glitch. As you know glitch.com provides free hosting for node.js/python/etc.

But it sends apps that aren't active a while to sleep. So next time you try to access your web app, it may take a while, 
or if it has some scheduling and stuff like that, it will encounter with some problems.

This App simply tries to send get requests on a specific interval to a specific url, so glitch consider your app as active.

It also has a command line, so that you can edit the list of the domains you want to poke, change the interval, etc.

# Features

* Poking mechasim as explained above
* Logging result of each request, and errors that may raise.
* Adding/removing domains to poke list
* Saving target list for next execution of the program.
* interval change, cutoff(truncuate) level change.
* All operations are implemented asynchronous-ly.
* Its obvious That this app can be used for services other services with glitch-like limitations too.

# Command-Line Help:
* add domain1 [domain2 domain3 ...]
    Adds and saves the list of domains provided, to the poke list.
    * Note: writing 'http://' or 'https://' is optional. 
* del domain1 [domain2 domain3 ...]
    Deletes them
* interval [number]
    Changes the poking interval to your desired time in seconds. If i remember correctly,
    glith will consider an app as inative, if it doesnt have any api interaction within 5 minutes.
    So set your interval below that, if you want your site to never go to sleep.
    * Note: glitch has another limitation. all your projects can be active nearly 1000 hours a month.
        Consider this in your interval value too.
* cutoff [value]
    cutoff value, is an integer value, which determines how many characters of the get request response, should be logged.
    After that the text will be trunctuated.(...)
* fuckoff
    The app will shutdown after the next interval.
* $ [command index]
    executes previous commands.
    index > 0: execute the (index)th command from all commands, that has been executed so far; starting from the app execution.
    index < 0: execute the latest commands. for example $ -1 will execute previous command.
* help
    Obvious! Prints the Command-Line Help