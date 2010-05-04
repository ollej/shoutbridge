Shoutbridge
===========

Jabber chat bot with a bridge to the shoutbox in the UBB.threads forum software.

Description
-----------
A bridge software that allows discussions in a UBB.threads shoutbox to be mirrored to an XMPP chat. Can also run independantly and work as a generic jabber chat bot with pluggable commands.


Main features
-------------
These are the main features of Shoutbridge:

 * All messages written in Shoutbox should be sent to the XMPP chat room.
 * All messages written in the XMPP chat room should be sent to the Shoutbox.
 * If no XMPP details, messages will be sent with UBB.threads username prepended to message.
 * Messages from XMPP will be added as user in Shoutbox if they have XMPP login details saved in profile.
 * Simple API to UBB.threads to read/write messages and get user by login details and login details from user.
 * Keep track of roster via prescence, read user info only once.
 * Connect to an xmpp conference room instead of just sending messages to a user
 * Can read shoutbox info directly via MySQL database, or over http.
 * Plugins with bot commands can easily be written.
 * Easily configured using command line options or config file.
 * Includes several plugins: Quotes, Definitions, Dice roller, Name generator, Eliza, Slap etc.


Requirements
------------
 * Python 2.6
 * MySQL
 * UBB.threads v7
 * Twisted
 * MySQLdb (for direct connection to shoutbox)
 * pyOpenSSL (for secure connections)


Installation
------------
Shoutbridge requires a few extra python modules to run. Currently, the only
working xmpp bridge class is Twisted, so that python module must be installed.
The MySQLdb module is needed for a direct connection to the shoutbox. If you
don't have access to the UBB.threads database where you run the Shoutbridge,
you can instead use the ExternalShoutbridge class. In this case, you don't
need the MySQLdb module.

Install necessary modules:

    $ sudo easy_install Twisted
    $ sudo easy_install MySQLdb
    $ sudo easy_install pyOpenSSL

Next, create a configuration file from the example.

    $ cp config-example.ini config.ini

Edit the config.ini file and change the values to something appropriate.
The db_* values should be set to your UBB.threads installation.

xmpp_login and xmpp_pass should be set to an xmpp account that will be used to relay
messages between the shoutbox and the chat room. You have to register this account
yourself.

xmpp_room should be the full jid to the chat room to connect to. This should
already be created, as Shoutbridge currently can't create it.
xmpp_host and xmpp_port should be set to the jabber server to connect to.

In UBB.threads, you should set Profile Extra Field 1 to "JID Login". If a user 
enters their jabber id in this field, messages sent from that jid will be written
as that user in the shoutbox.

If you are running the ExternalShoutbox you must enter the URL to your UBB.threads
installation. 

Now you should be ready to start the program:

    $ python shoutbridge.py


TODO
----
Some ideas for future development.

 * If UBB.threads user has XMPP login details saved, messages should be sent using these.
 * Possibly change to a transport gateway using XEP-0100: Gateway Interaction
 * When time is the same as the current time, don't prepend time to message.
 * If room hasn't been created when joining, accept default room configuration.
 * Move plugin command matching code to XmppBridge.trigger_plugin_event
 * Add priority sorting to plugin triggering.
 * away presence could hide user on forum
 * Load plugin method should use reflection on plugins to find out commands, and handler methods.
 * Log all exceptions to file.
 * HelpPlugin
     * Add help information for plugins. Read using reflection by HelpPlugin
     * HelpPlugin should list all available commands if no argument is given.
     * If a command is given to !help, print doc string for that command.
 * Add support to choose config section via command line for shoutbridge.py
 * BUG: Exception raised if plugin not found: ImportError: No module named NamnPlugin
 * BUG: When loadUrl fails, reactor stops running that loop.
 * Move plugins into plugin sub-directory.
 * Move xmpp bridges into bridges/ and shoutbox classes into shoutbox/
 * Consolidate all quote plugins. IN PROGRESS
 * Plugin commands should not be case sensitive. IN PROGRESS
 * Plugin ideas:
   * !seen <user> - showing last online time for user
   * !help - Display help information from all plugins.
   * !calc - calculator
   * Possibly convert !trivia, !weather, !translate, !google etc from other bots.
   * Use people's dictionary and synlist.
 * Plugin handlers should always receive a generic object instead of the raw twisted domish object. For messages, this can be a Shout object.
 * Have the possibility to not have shoutbox bridge at all.
 * Add __init__.py file
 * Keep connection open on server-side script and read new shout messages immediately.
 * Follow verbose and quiet options.
   * debug = print raw send/recv stanzas.
   * quiet = no output
   * verbose = print logprints
 * BUG: Graemlin replacement should be done before html stripping.
 * BUG: HTML-stripping not quite up to par.
