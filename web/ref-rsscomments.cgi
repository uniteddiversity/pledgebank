#!/usr/bin/perl -w
#
# rss-comments:
# Generate RSS feed for comments for a particular pledge
#
# Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/

my $rcsid = ''; $rcsid .= '$Id: ref-rsscomments.cgi,v 1.10 2008-02-04 22:50:29 matthew Exp $';

use strict;
require 5.8.0;

# Horrible boilerplate to set up appropriate library paths.
use FindBin;
use lib "$FindBin::Bin/../perllib";
use lib "$FindBin::Bin/../commonlib/perllib";

use mySociety::Config;
BEGIN {
    mySociety::Config::set_file("$FindBin::Bin/../conf/general");
}
use mySociety::DBHandle qw(dbh);
use mySociety::WatchUpdate;
use mySociety::Web qw(ent);
use PB;
use Encode;
use XML::RSS;
use CGI::Carp;
use mySociety::CGIFast qw(-no_xhtml);

my %CONF = ( number_of_comments => 20,
             base_url => mySociety::Config::get('BASE_URL') . '/',
             contact_email => mySociety::Config::get('CONTACT_EMAIL')
            );

my $W = new mySociety::WatchUpdate();
our $request;
while ($request = new mySociety::CGIFast()) {
    run();
    $W->exit_if_changed();
}

sub run {
    my $ref = $request->param('ref') || '';
    # Do our own encoding
    my $rss = new XML::RSS (version => '1', encoding => 'UTF-8', encode_output => undef );

    my $query= dbh()->prepare("select id,title from pledges where ref=? and pin is null");
    $query->execute($ref);
    my ($pledge_id, $title) = $query->fetchrow_array;
    $title ||= '';
    # Probably just migrate to PHP really, the functions are more set up for it.
    # e.g. Would naturally get the base URL with full lang/country as needed in RSS feeds.
    $rss->channel(
        title        => "Comments on $ref pledge",
        link         => $CONF{base_url} . $ref,
        description  => ent("Comments on '$title'"),
        dc => {
            creator    => $CONF{contact_email},
            language   => 'en-gb',
            ttl        =>  600
        },
        syn => {
            updatePeriod     => "hourly",
            updateFrequency  => "2",
            updateBase       => "1901-01-01T00:00+00:00",
        },
    );

    $query= dbh()->prepare("select id, name, text from comment
                            where pledge_id = ? and not ishidden
                            order by id desc limit $CONF{number_of_comments}");
    $query->execute($pledge_id);

    while (my $row = $query->fetchrow_hashref) {
        $rss->add_item(
            title => ent("Comment by $row->{name}"),
            link => "$CONF{base_url}$ref#comment_$row->{id}",
            description=> ent(ent($row->{text})) # Yes, double-encode
         );
    }

    print CGI->header( -type => 'application/xml; charset=utf-8' );
    print Encode::encode_utf8($rss->as_string);
}
