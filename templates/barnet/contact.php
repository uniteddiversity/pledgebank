<?
// contact.php:
// Barnet contact us template for PledgeBank.
//
// Copyright (c) 2010 UK Citizens Online Democracy. All rights reserved.
// Email: matthew@mysociety.org. WWW: http://www.mysociety.org

    print '<div id="tips">';
 
    if ($comment_id) {
        print p(_('You are reporting the following comment to us:'));
        print '<blockquote>';
        $row = db_getRow('select *,extract(epoch from ms_current_timestamp()-whenposted) as whenposted from comment where id = ? and not ishidden', $comment_id);
        if ($row)
            print comments_show_one($row, true);
        else
            print '<em>Comment no longer exists</em>';
        print '</blockquote>';
    }

    print "</div>";

    if (sizeof($errors)) {
        print '<div id="errors"><ul><li>';
        print join ('</li><li>', $errors);
        print '</li></ul></div>';
    } ?>
<form name="contact" accept-charset="utf-8" action="/contact" method="post"><input type="hidden" name="contactpost" value="1"><input type="hidden" name="ref" value="<?=htmlspecialchars($ref)?>"><input type="hidden" name="referrer" value="<?=htmlspecialchars($referrer)?>"><input type="hidden" name="pledge_id" value="<?=htmlspecialchars($pledge_id)?>"><input type="hidden" name="comment_id" value="<?=htmlspecialchars($comment_id)?>">
<?  if ($comment_id) {
        print h2(_('Report abusive, suspicious or wrong comment'));
        print p(_("Please let us know exactly what is wrong with the comment, and why you think it should be removed."));
    } else {
        print h2("Suggest a pledge");
        $contact_email = str_replace('@', '&#64;', OPTION_CONTACT_EMAIL);
        
        print "<p>Do you have an idea for a pledge that could appear on this site?</p>";
        print "<p>What would you like to get done? </p>";

        printf(_('If you prefer, you can email %s instead of using the form.'), '<a href="mailto:' . $contact_email . '">' . $contact_email . '</a>');
        print "</p>";
    }
?>

<p><label for="name"><?=_('Your name:') ?></label> <input type="text" id="name" name="name" value="<?=htmlspecialchars($name) ?>" size="30">

<p><label for="e"><?=_('Your email:') ?></label> <input type="text" id="e" name="e" value="<?=htmlspecialchars($email) ?>" size="30"></p>

<input type="hidden" id="subject" name="subject" value="">

<p><label for="message">Your suggestion:</label>
<br><textarea rows="7" cols="40" name="message" id="message"><?=htmlspecialchars(get_http_var('message', true)) ?></textarea></p>

<p>
<input type="submit" name="submit" value="Send to PledgeBank team"></p>
<?  if (! $comment_id) { ?>
  <p>The PledgeBank team will...</p>
  <ul>
    <li>review suggestions and add them to the website</li>
    <li>Share your pledge through tweets, social networks and flyers</li>
    <li>Recruit people to help and get things done</li>
  </ul>
<? } ?>
</form>