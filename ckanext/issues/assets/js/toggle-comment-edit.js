this.ckan.module('toggle-comment-edit', function($, _) {
  return {
    initialize: function() {
      var self = this;
      // Listen for click on the Cancel button inside .issue-comment-edit
      this.el.on('click', '.issue-comment-edit button[type="button"]', function(e) {
        e.preventDefault();
        var $form = $(this).closest('.issue-comment-edit');
        var $textarea = $form.find('textarea');
        var $saveBtn = $form.find('button[type="submit"]');
        // Toggle visibility of the textarea and Save/Cancel buttons
        if ($textarea.is(':visible')) {
          $textarea.hide();
          $saveBtn.hide();
          $(this).text('Edit');
        } else {
          $textarea.show();
          $saveBtn.show();
          $(this).text('Cancel');
        }
      });
      // Optionally, hide textarea and save button on load
      this.el.find('.issue-comment-edit textarea, .issue-comment-edit button[type="submit"]').hide();
      this.el.find('.issue-comment-edit button[type="button"]').text('Edit');
    }
  };
});