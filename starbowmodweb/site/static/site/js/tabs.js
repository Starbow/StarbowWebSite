/*
 * tabs.js
 *
 * Desc: sets up functionality for tabs
 */

$(function() {
  $('div[tab]').hide();
  $('div[tab]:first').show();

  $('li[tab]').each(function() {
    $(this).click(function() {
      tab = $(this).attr('tab');
      $('div[tab]').toggle();
      $('li[tab]').toggleClass('active');
    });
  });
});
