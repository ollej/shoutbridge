#!python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from utils.Conf import Conf
from utils.ObjectFactory import *

def start_shoutbridge():
    # Read command line options.
    parser = OptionParser(version="%prog 1.0")
    parser.add_option("-c", "--config", dest="config", default="config.ini",
                      help="Read configuration from FILE", metavar="FILE")
    parser.add_option("-S", "--section", dest="section", default="LOCAL",
                      help="Read configuration from SECTION", metavar="SECTION")
    parser.add_option("-D", "--debug",
                      action="store_false", dest="debug", default=False,
                      help="Print RAW data sent and received on the stream.")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="quiet", default=True,
                      help="Don't print status messages to stdout")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=True,
                      help="make lots of noise [default]")
    parser.add_option("-s", "--start", dest="latest_shout",
                      help="Start reading shouts from START", metavar="START")
    parser.add_option("-l", "--login", dest="xmpp_login",
                      help="XMPP login JID.", metavar="JID")
    parser.add_option("-p", "--pass", dest="xmpp_pass",
                      help="XMPP password.", metavar="PASSWD")
    parser.add_option("-r", "--room", dest="xmpp_room",
                      help="Join this XMPP room.", metavar="ROOM")
    parser.add_option("-d", "--host", dest="xmpp_host",
                      help="Set XMPP host.", metavar="HOST")
    parser.add_option("-o", "--port", dest="xmpp_port",
                      help="Set XMPP port.", metavar="PORT")
    parser.add_option("-A", "--status", dest="xmpp_status",
                      help="Set default XMPP away status message.", metavar="STATUS")
    parser.add_option("-R", "--resource", dest="xmpp_resource",
                      help="Set XMPP resource for this client instance.", metavar="RESOURCE")
    parser.add_option("-L", "--loop", dest="loop_time",
                      help="Read shoutbox messages every SECS.", metavar="SECS")
    parser.add_option("-X", "--plugins", dest="plugins",
                      help="Load comma separated extensions/plugins.", metavar="PLUGINS")
    parser.add_option("-u", "--url", dest="base_url",
                      help="Read shoutbox messages from this URL.", metavar="URL")
    parser.add_option("-t", "--show-time", dest="show_time",
                      help="Prepend time to each message.")
    parser.add_option("-n", "--show-nick", dest="show_nick",
                      help="Prepend originating nick to each message.")
    parser.add_option("-b", "--bridge", dest="bridge_type",
                      help="Use this XMPP bridge class.", metavar="BRIDGE")
    parser.add_option("-B", "--shoutbox", dest="shoutbox_type",
                      help="Use this shoutbox connector class.", metavar="SHOUTBOX")
    parser.add_option("-H", "--db-host", dest="db_host",
                      help="Host for DB connector.", metavar="HOST")
    parser.add_option("-N", "--db-name", dest="db_name",
                      help="Name for DB connector.", metavar="NAME")
    parser.add_option("-U", "--db-user", dest="db_user",
                      help="User for DB connector.", metavar="USER")
    parser.add_option("-P", "--db-pass", dest="db_pass",
                      help="Password for DB connector.", metavar="PASS")
    parser.add_option("-f", "--jid-field", dest="ubb_jid_field",
                      help="UBB.threads profile table field containing user JID.", metavar="FIELD")
    parser.add_option("-C", "--secret", dest="secret", metavar="SECRET",
                      help="Use this secret word to connect to MessageShoutbox server script.")
    parser.add_option("-F", "--date-format", dest="log_date_format",
                      help="Use this date format when logging.", metavar="FORMAT")
    (options, args) = parser.parse_args()

    # Read configuration.
    configfile = options.config or 'config.ini'
    configsection = options.section or 'LOCAL'
    cfg = Conf(configfile, configsection)
    cfg.set_items(vars(options))

    if cfg.verbose:
        print "Shoutbridge started..."

    # Setup Shoutbox
    of = ObjectFactory()
    sbox = of.create(cfg.shoutbox_type, mod='shoutbox', inst="Shoutbox")
    sbox.setConfig(cfg)

    # Setup xmpp bridge
    bridge = of.create(cfg.bridge_type, mod='bridge', inst="XmppBridge")
    bridge.setup(sbox, cfg)

    # Start bridge
    bridge.listen()
    if cfg.verbose:
        print "Shoutbridge ended."

# Call the main function.
if __name__ == '__main__':
    start_shoutbridge()

