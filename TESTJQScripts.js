/*
 * Filename:     JQScripts.js
 * Author:       Andrew Laing
 * Email:        parisianconnections@gmail.com
 * Last updated: 29/01/2020.
 * Description:  JQuery scripts used by the 'Tell the World' website.
 */

$(document).ready(function(){

    /**
      * Shows the comment panel of an update collapse when it is opened.
      */
    $('.panel-collapse').on('shown.bs.collapse', function () {          
        $(this).siblings('.comment-panel').toggle();
    });


    /**
      * When an update collapse is closed, this hides the comment panel
      * and its contents.
      */
    $('.panel-collapse').on('hidden.bs.collapse', function () {
        $(this).siblings('.comment-panel').toggle();
        $(this).siblings('.comment-panel').children('.user-reply-section').hide();
        $(this).siblings('.comment-panel').children('.user-comment-section').hide();
        
        $(this).siblings('.comment-panel').children('.reply_btn').text("Reply");
        $(this).siblings('.comment-panel').children('.view_comments_btn').text("View all comments");
    });

    
    /**
      * Shows the user reply section when the reply button is clicked
      */
    $('.reply_btn').on('click', function () {
        $(this).siblings('.user-reply-section').children('.user-comment-input-area').val("");
        /* Toggle the text shown on the reply button */
        if ( $(this).text() == "Reply")  {
          $(this).text("Hide reply");
        } else {
          $(this).text("Reply");
        }
        $(this).siblings('.user-reply-section').toggle();
        $(this).siblings('.user-reply-section').children('.user-comment-input-area').focus();
        
    });

    /**
      * Clears user input and closes the user reply section when
      * the cancel reply button is clicked.
      */
    $('.cancel_reply_btn').on('click', function () {
        $(this).siblings(".user-comment-input-area").val("");
        $(this).parent().parent().children('.reply_btn').text("Reply");
        $(this).parent().toggle();
    });

    /**
      * Toggles the visibility of the user comment section when the
      * view/hide comments button is clicked, and populates it with
      * user comments where necessary.
      */
    $('.view_comments_btn').on('click', function () {
        if ( $(this).text() == "View all comments")  {
          var postID = $(this).parent().attr('id');
          postID = postID.replace('comments','');
          //$.fetchComments($(this), postID);
          $(this).text("Hide comments");
        } else {
          $(this).text("View all comments");
        }
        $(this).siblings('.user-comment-section').toggle();
    });
    
    
    /**
      * Fetches comments attached to a post and adds them to the user-comment-section.
      */
    $.fetchComments = function ($this, in_postID) {
        alert(in_postID);
        //alert("add comments to user-comment-section here");
        // Make AJAX call and add html to user-comment-section here
        var data = '<p style="margin-left: 20px; padding-top: 10px; padding-bottom:10px;">Be the first person to make a comment on this post.</p>';
        
        $this.siblings('.user-comment-section').empty();
        $this.siblings('.user-comment-section').html(data);
        
        var url="/commentlist/?postID=" + in_postID;
        alert(url);
        
        //$this.siblings('.user-comment-section').empty();
        //var url="/commentlist/?postID=" + in_postID;
        //$this.siblings('.user-comment-section').load(url, function(result){
        // });
        
    };
    
    
    /**
      * Handles adding a comment to the post when the post reply button is clicked.
      */
    $('.post_reply_btn').on('click', function () {
        alert("POST A REPLY");
        
        // ///////////////////////////////////////////////////////////////////////////
        // Note: this a test so I will be able to create a generic function
        //       that can reload the comments for a post.
        $(this).parent().siblings('.user-comment-section').html("CHIZU CHIZU CHIZU");
        // ///////////////////////////////////////////////////////////////////////////
        
        var commentText = $(this).siblings(".user-comment-input-area").val().trim();
        var commentLength = commentText.length;
        var postID = $(this).parent().parent().attr('id');
        postID = postID.replace('comments','');
        
        if (commentLength == 0) {
          alert("The 'Enter your reply' field cannot be left empty!");
          $(this).siblings(".user-comment-input-area").focus();
          return false;
        };
        
        // Post comment here
        alert(commentText);
        alert(postID);
        $(this).siblings(".user-comment-input-area").val("");
        $(this).parent().parent().children('.reply_btn').text("Reply");
        $(this).parent().toggle();
    });    
   
   
    /** 
     * Resizes the comment text area if necessary when text is inputted 
     */
    $('.user-comment-input-area').on('keyup input', function () {
        var offset = this.offsetHeight - this.clientHeight;
        $(this).css('height', 'auto').css('height', this.scrollHeight + offset);
    });    
   
   
    /** 
     * Resizes the comment text area if necessary when the window is resized. 
     */
    $(window).on('resize', function () {
        $this = $('.user-comment-input-area');
        $this.trigger('input'); // trigger input event to call function above
    });     
   
});
