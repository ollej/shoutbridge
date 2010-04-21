Shoutbridge
===========

UBB.threads Shoutbox <-> XMPP Bridge

Description
-----------
A bridge software that allows discussions in a UBB.threads shoutbox to be mirrored to an XMPP chat.


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


Requirements
------------
 * Python 2.6
 * MySQL
 * UBB.threads v7
 * Twisted
 * MySQLdb (for direct connection to shoutbox)


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
 * Move date formats into configuration.
 * Possibly change to a transport gateway using XEP-0100: Gateway Interaction
 * Plugins for message hooks, to allow simple bot-like behavior.
 * Dice Bot which can roll dice, e.g. "/dice 3d6" gives "Dice roll result: 12 (5 + 3 + 4)"
 * /me 
 * When time is the same as the current time, don't prepend time to message.
 * If room hasn't been created when joining, accept default room configuration.
 * Answer to presence requests from server, or whatever is necessary not to be disconnected.
 * Add functionality to sendShout for MessageShoutbox

