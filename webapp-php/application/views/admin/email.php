<!-- TODO(aok) w3c validate each page -->
<div class="page-heading">
  <h2>Post Crash Email</h2>
</div>
<div class="panel postcrash">
  <?php View::factory('common/recent_email_campaigns')->render(TRUE); ?>
  <div class="body notitle">
    <div class="admin">
      <h3>Email</h3>
      <p>During a product release, use this form to contact user's that a crash has been fixed.</p>
      <p>The email is sent immediately. Setting a date range into the future will have no effect.</p>
      <p>There are two variables you can use in the email body:
        <ul>
          <li><code class="email-var">*|EMAIL_ADDRESS|*</code> - Will be replaced with user's email. Example jane@doe.name</li>
          <li><code class="email-var">*|UNSUBSCRIBE_URL|*</code> - Will be replaced with user's unique un-subscribe URL</li>
        </ul></p>
      <?php View::factory('common/form_errors')->render(TRUE); ?>
      <form class="" name="postcrashemail" action="confirm_email" method="post">
        <label for="email_product">Product</label>
        <select name="email_product" class="input">
        <?php foreach($products as $product) { ?>
            <option value="<?= $product ?>" <?php if ($product == $email_product) echo 'SELECTED' ?> ><?= $product ?></option>
        <?php } ?>
        </select>
        <label for="email_versions" title="Versions is a comma seperated list of version numbers. 4.06b, 4.0b7pre, 3.6.10">Versions <span class="help">(Comma sepearted)</span></label>
        <input name="email_versions" type="text" value="<?= $email_versions ?>" size="80" />
        <label for="email_signature" class="<?php if (isset($errors) && array_key_exists('email_signature', $errors)) { echo 'form_error'; }; ?>">Exact Signature</label><input name="email_signature" type="text" value="<?= $email_signature ?>" size="80" />

        <label for="email_subject" class="<?php if (isset($errors) && array_key_exists('email_subject', $errors)) { echo 'form_error'; }; ?>">Subject</label>
        <input name="email_subject" type="text" value="<?= $email_subject ?>" size="80" />

        <label for="email_body" class="<?php if (isset($errors) && array_key_exists('email_body', $errors)) { echo 'form_error'; }; ?>">Email Body</label><textarea name="email_body" row="10" cols="80"><?= $email_body ?></textarea>

        <label for="email_start_date" class="<?php if (isset($errors) && array_key_exists('email_start_date', $errors)) { echo 'form_error'; }; ?>">Start Date</label> 
        <div class="input"><input name="email_start_date" type="text" value="<?= $email_start_date ?>" size="8" /></div>

        <label for="email_end_date" class="<?php if (isset($errors) && array_key_exists('email_end_date', $errors)) { echo 'form_error'; }; ?>">End Date</label> <div class="input"><input name="email_end_date" type="text" value="<?= $email_end_date ?>" size="8" /></div>
        <input name="submit" type="submit" value="Next Step" />
      </form>
      <br class="clear" />
    </div><!-- .admin -->
  </div><!-- .body .notitle -->

</div><!-- .panel -->
