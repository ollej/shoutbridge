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
 * Twisted
 * MySQL (for direct connection to shoutbox)
 * UBB.threads v7 (for shoutbox bridge)
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


Running Shoutbridge
-------------------
Now you should be ready to start the program:

    $ python shoutbridge.py


Configuration Options
---------------------
There are a lot of available configuration options for Shoutbridge.

 * xmpp_login - Jabber account JID to login as.
 * xmpp_pass - Password for Jabber account.
 * xmpp_room - Jabber conference room to connect to.
 * xmpp_host - Jabber host to connect to.
 * xmpp_port - Jabber port to connect to.
 * xmpp_status - Jabber status message for the Shoutbridge client.
 * xmpp_resource - Jabber resource of this client instance.
 * bridge_type - XMPP library class to use. Leave as is.
 * shoutbox_type - Shoutbox connector class.
   * MessageShoutbox - Read/post shout messages via HTTP, requires a server-side
     script to be installed on the UBB.threads server.
   * MysqlShoutbox - Read/post shout messages directly to UBB.threads db.
   * FakeShoutbox - Dummy connector, use this if you don't want the shoutbox 
     bridge functionality.
   * ExternalShoutbox - Read shout messages via HTTP, doesn't require extra
     server-side script, but doesn't allow posting.
 * db_host - Hostname for MySQL db for UBB.threads, only required for MysqlShoutbox.
 * db_name - Name of MySQL db for UBB.threads, only required for MysqlShoutbox.
 * db_user - Username of MySQL db for UBB.threads, only required for MysqlShoutbox.
 * db_pass - Password of MySQL db for UBB.threads, only required for MysqlShoutbox.
 * base_url - Base URL to the UBB.threads installation, used by MessageShoutbox and 
   ExternalShoutbox.
 * ubb_jid_field - UBB.threads profile database field containing user JID Login.
 * secret - Secret key to use when sending messages with ExternalShoutbox, must also be
   entered in the server-side script.
 * loop_time - How many seconds between each update from the shoutbox.
 * show_time - If set to "True", the time of the shoutbox message will be prepended in jabber.
 * show_nick - Set to "True" to prefix each message with shoutbox nick. Otherwise the bot will rename itself to the username of the shoutbox user.
 * log_date_format - Date format for logging.
 * latest_shout - Start reading shout messages from this id.
 * plugins - Comma separated list of plugin names to load.

### Jabber conference room ###
The jabber conference room has to be created already when the Shoutbridge box
connects. 

### UBB.threads Jabber ID ###
In UBB.threads, you should set Profile Extra Field 1 to "JID Login". If a user 
enters their jabber id in this field, messages sent from that jid will be written
as that user in the shoutbox.

When a user has entered this information, messages relayed from Jabber from this JID
will be entered as coming from the user in the shoutbox.

### Server-side script for ExternalShoutbox ###
When using the ExternalShoutbox connector, a server-side script must be uploaded to
the UBB.threads installation.

Upload the following file to the scripts/ directory of your UBB.threads installation:
    ubb/scripts/listshouts.inc.php

Make sure you enter the same secret as in the configuration. This secret is sent in
plain text in the URL and is not secure. Knowing this will allow injecting any
message in the shoutbox. Only use ExternalShoutbox if absolutely necessary,
and take the proper precautions.


Command Line Options
--------------------
Shoutbridge has a number of command line options available. All configuration 
options can be overridden with a corresponding command line option.

Additionally, it is possible to select another configuration file and 
section than the default. 

There are also three options to change how much information shoutbridge
should output on the terminal: debug, quiet and verbose

### Options: ###
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -c FILE, --config=FILE
                          Read configuration from FILE
    -S SECTION, --section=SECTION
                          Read configuration from SECTION
    -D, --debug           Print RAW data sent and received on the stream.
    -q, --quiet           Don't print status messages to stdout
    -v, --verbose         make lots of noise [default]
    -s START, --start=START
                          Start reading shouts from START
    -l JID, --login=JID   XMPP login JID.
    -p PASSWD, --pass=PASSWD
                          XMPP password.
    -r ROOM, --room=ROOM  Join this XMPP room.
    -d HOST, --host=HOST  Set XMPP host.
    -o PORT, --port=PORT  Set XMPP port.
    -A STATUS, --status=STATUS
                          Set default XMPP away status message.
    -R RESOURCE, --resource=RESOURCE
                          Set XMPP resource for this client instance.
    -L SECS, --loop=SECS  Read shoutbox messages every SECS.
    -X PLUGINS, --plugins=PLUGINS
                          Load comma separated extensions/plugins.
    -u URL, --url=URL     Read shoutbox messages from this URL.
    -t SHOW_TIME, --show-time=SHOW_TIME
                          Prepend time to each message.
    -n SHOW_NICK, --show-nick=SHOW_NICK
                          Prepend originating nick to each message.
    -b BRIDGE, --bridge=BRIDGE
                          Use this XMPP bridge class.
    -B SHOUTBOX, --shoutbox=SHOUTBOX
                          Use this shoutbox connector class.
    -H HOST, --db-host=HOST
                          Host for DB connector.
    -N NAME, --db-name=NAME
                          Name for DB connector.
    -U USER, --db-user=USER
                          User for DB connector.
    -P PASS, --db-pass=PASS
                          Password for DB connector.
    -f FIELD, --jid-field=FIELD
                          UBB.threads profile table field containing user JID.
    -C SECRET, --secret=SECRET
                          Use this secret word to connect to MessageShoutbox
                          server script.
    -F FORMAT, --date-format=FORMAT
                          Use this date format when logging.

Plugins
-------
Shoutbridge has a plugin system to allow new bot commands and general message handling.

Which plugins are loaded is defined by the "plugins" configuration and command line option.

A number of plugins are available by default, and it's very easy to write new ones.

Commands can have synonyms, i.e. multiple commands trigger the same method handler.

### MonkeyPlugin ###
This is a very simple plugin that sends back pre-defined messages based on specific
commands.

By default, it has a lot of commands that returns simple one-line ascii art.

The name of the plugin comes from the command !monkey which returns the following
message:

    @({-_-})@

If there are several return messages for a command, one of the messages is selected
by random and sent.

At the time of writing, this plugin has the following commands available:

    !monkey, !tits, !penis, !koala, !fish, !sheep, !spider, !cat, !rose, !mouse,
    !sword, !snail, !coffee

### DiceyPlugin ###
The DiceyPlugin can roll dice and return the results.

#### Available dice ####
Dicey can roll dice with the following number of sides:

    2, 4, 6, 8, 10, 12, 100

#### Commands ####
Dicey understands the following commands.

##### Roll one die #####
Added "d" or "D" in front of the number of sides the die should have.

    !dicey d10

##### Multiple dice #####
Roll multiple dice with the same number of sides and add up the results.

    !dicey 3d6

##### Modifications #####
Roll three 6-sided dice and add 4 to the result. Also works with subtraction.

    !dicey 3d6+4

##### Choose highest #####
Add an "h" and a number to the end of the die roll to choose the that number of 
dice with the highest values. Use "l" (lower case L) to instead choose the lowest 
results. E.g. Roll five 8-sided dice and return the 4 highest. 

    !dicey 5d8h4

##### Multiple rolls #####
Up to five sets of rolls can be rolled at the same time:

    !dicey 3d6 5d8-2 6d10h4 2d12l1 d100

##### Open ended rolls #####
To roll an open ended die, where the another die is rolled and added to the 
result if the die roll is the highest possible value of the die. Prefix the
die roll with "Open".

    !dicey OpenD20

##### Exploding rolls #####
Exploding, or limitless, dice like those in games from Neogames. Every die that
rolls the maximum value is replaced by two dice and re-rerolled. Prefix the
die roll with "Ob".

    Ob3d6

#### Character Generation ####

Additionally, Dicey can automatically make the rolls needed to create 
characters in a few roleplaying games.

##### Dngeons & Dragons #####
Roll 4 d6 and choose the 3 highest for: STR, CON, DEX, INT, WIS and CHA

    !dicey DnD

##### Drakar och Demoner #####
Roll 3d6 for the following values: STY, KRO, STO, INT, KRA, SKI, KAR

    !dicey DoD

##### Eon #####
Roll 3d6 for each of these values: STY, TÅL, RÖR, PER, PSY, VIL, BIL, SYN, HÖR

    !dicey eon

##### Twerps #####
Roll a D10 for the value Strength.

    !dicey Twerps

### FortunePlugin ###
Prints a random fortune cookie, quote or amusing tidbit of information.

Requires the fortune program installed on the computer running the jabber bot.

#### Command: ####

    !fortune

### KraetyzPlugin ###
A bot that sends a pre-defined message whenever one of a configured list of users'
write something specific.

By default, if a user named "Kraetyz" writes something containing "jag tycker", the
bot will return the following message:
"/me bannar %s för uttryckande av åsikt."

If the text contains "%s", without quotes, it will be replaced by the name of the
user.

### ElizaPlugin ###
Eliza is a cute little chat bot that pretends to be a (very bad) psychologist.

The plugin is just a wrapper for an external Python module which contains the actual
"artificial intelligence". The Eliza python module is available in the Shoutbridge
package since it needed a small code change. If you want to run this bot, you need to
copy the file "extras/eliza.py" into the root Shoutbridge directory. Then add "Eliza"
to the list of available plugins in the configuration.

The original script is written by Jez Higgins and is available from this URL:
http://www.jezuk.co.uk/cgi-bin/view/software/eliza

#### Command: ####

    Eliza, who are you?

Remember to prepend all messages to Eliza with "Eliza, " or she won't answer.

### NamePlugin ###
Return a message with the names of the day in the Swedish calendar.

#### Command: ####

    !dagensnamn

### NominoPlugin ###
Nomino is a random name generator.

#### Command: ####

    !name

It is also possible to define name list to use, as well as how many names to generate,
and which gender they should be.

#### Example: ####

    !name 5 scottish women

You can also choose different lists for given name and surname.

#### Example: ####

    !name chinese gaelic

#### Available name lists ####
Arabic, Chinese, Czech, English1500ce, English, French, Gaelic, German, Hindu, Irish,
Japanese, Mutant, Russian, Scottish, Spanish, Svenska2000ce, Venetarian1300ce

### QuotesPlugin ###
Sends a random quote from different quote files.

#### Command: ####

    !quote

#### Additional quote files: ####

 * !jeff - Quotes by Jeff Murdoch from TV series Coupling
 * !murphy - Random Murphy's Law
 * !kimjongil - Swedish silly Kim Jong Il messages.
 * !kjell - Swedish quotes from TV series Kjell
 * !evaemma - Swedish quotes from blogger EvaEmma Andersson
 * !storuggla - Swedish quotes from Storuggla

#### Add new quotes ####
It is also possible to add new quotes which are added to a temporary file. These
have to be added to used quote file by hand later.

##### Command: #####
    !quote add "New quote to add here."

#### Quote file format ####
The quote files should be encoded in UTF-8. Each quote should be separated by a
line containing only a percentage sign:

##### Example: #####

    First quote.
    %
    Second quote.


### SlapPlugin ###
Writes a possibly hilarious slapping message.

#### Command: ####

    !slap username

### TermPlugin ###
Returns definitions of given term, prints a random definition and allows adding
new definitions.

#### Commands ####
List of commands available for the Term plugin.

##### Command: #####

    !term

##### Command: #####

    !term 'dnd'

##### Command: #####

    !term add Term=Definition

New terms are added to a separate file and needs to be added to the main file by hand.

### WeekPlugin ###
Returns the week number according to the ISO date standard, commonly used in Scandinavia.

#### Command: ####

    !week


Write your own plugin
---------------------
If you know a little Python, writing your own bot plugin is easy.

For a quick start, take a look at an easy plugin, like WeekPlugin.py

### HelloWorldPlugin ###
Create a new file called HelloWorldPlugin.py

Start by importing the necessary modules:

    from Plugin import *

Next, create the actual plugin class, make sure it extends the base Plugin class:

    class HelloWorldPlugin(Plugin):

The class should have some attributes describing the class.

    name = "HelloWorldPlugin"
    author = "Your Name"
    description = "A simple Hello World plugin."

The most important attribute is "commands", which contains a list of commands
and matching method handlers, as well as additional information needed for the command.

Each dict() element in the commands list is the description of a single command. A command
can have several different bot trigger commands, in this case only "!hello" is used.
This means that when a user writes a message starting with this text, the method in the
"handler" is called.

In the onevents list, you should list each of the events that should trigger this handler.
The available events are:

 * Message - Triggered on both Shoutbox messages and XMPP messages. First argument is a Shout object.
 * ShoutMessage - Trsggered on Shoutbox messages. First argument is a Shout object.
 * XmppMessage - Triggered only on XMPP messages. First argument to method is stanza as xml string.
 * XmppPresence - Triggered on XMPP Presence stanzas. First argument to method is stanza as xml string.
 * XmppIq - Triggered on XMPP IQ stanzas, first argument to method is stanza as xml string.


The entire command dictionary is sent to the handler method. This means that any extra
information is available in the method.

    commands = [
        dict(
            command = ['!hello'],
            handler = 'hello_world',
            onevents = ['Message'],
        )
    ]

Finally, we need to define the handler method. The name should be the same as the "handler"
in the commands list.

The method will receive four arguments, text, nick, command and cmd.

 * shout - A Shout object with information about message.
   shout.name = Name of sender.
   shout.text = Message body text.
   shout.time = Unix timestamp of when message was received.
   shout.id = ID of message, if message was read from shoutbox.
   shout.userid = User id, if message was read from shoutbox.
 * command - Command that matched, will be one of the text strings in "command" in the dictionary.
 * comobj - The entire command dictionary object.

First the method definition.

    def hello_world(self, shout, command, comobj):

The content of the handler method should do any necessary calculations. To send messages
just call self.bridge.send_and_shout(text, nick) where text is the message to send and
nick is the nick the message should be sent as. By default, self.nick contains the name
"HALiBot". This can be overridden in the plugin class attributes.

        self.bridge.send_and_shout("Hello World!", self.nick)

That's all that is needed to create a simple plugin for Shoutbridge. More advanced actions
can be done. For more information, check the Plugin base class.

#### Full example ####

    from plugins.Plugin import *

    class HelloWorldPlugin(Plugin):
        name = "HelloWorldPlugin"
        author = "Your Name"
        description = "A simple Hello World plugin."
        commands = [
            dict(
                command = ['!hello'],
                handler = 'hello_world',
                onevents = ['Message'],
            )
        ]

        def hello_world(self, shout, command, comobj):
            self.bridge.send_and_shout(shout.name + ": Hello World!", self.nick)


TODO
----
Some ideas for future development.

 * If UBB.threads user has XMPP login details saved, messages should be sent using these.
 * Possibly change to a transport gateway using XEP-0100: Gateway Interaction
 * When time is the same as the current time, don't prepend time to message.
 * If room hasn't been created when joining, accept default room configuration.
 * Move plugin command matching code to XmppBridge.trigger_plugin_event
 * Add priority sorting to plugin triggering.
 * Load plugin method should use reflection on plugins to find out commands, and handler methods.
 * Away presence could hide user on forum
 * Log all exceptions to file.
 * HelpPlugin
     * Add help information for plugins. Read using reflection by HelpPlugin
     * HelpPlugin should list all available commands if no argument is given.
     * If a command is given to !help, print doc string for that command.
 * BUG: Exception raised if plugin not found: ImportError: No module named NamnPlugin
 * BUG: When loadUrl fails, reactor stops running that loop.
 * Allow commands to be sent as direct messages as well.
 * Plugin ideas:
   * !seen <user> - showing last online time for user
   * !help - Display help information from all plugins.
   * !calc - calculator
   * !memory - display used memory
   * !tell <user> <text> - When <user> is seen next, send message with <text>
   * !cyborg <word> - cyborgify <word> - http://www.brunching.com/
   * !techify <word> - techify <word> - http://www.brunching.com/
   * Possibly convert !trivia, !weather, !translate, !google, !wiki etc from other bots.
   * Use people's dictionary and synlist.
 * Direct message commands:
   * !say - make bot say something.
   * !die - make bot disconnect and shutdown
   * !reconnect - make bot reconnect
   * !reload - make bot reload all plugins
   * !jump - make bot move to another conference room
   * !rehash - make bot reload configuration
 * Create unit tests for all code.
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
 * Add language support for easy translation.
