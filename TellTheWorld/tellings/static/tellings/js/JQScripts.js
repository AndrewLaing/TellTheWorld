/*
 * Filename:     JQScripts.js
 * Author:       Andrew Laing
 * Email:        parisianconnections@gmail.com
 * Last updated: 26/03/2020.
 * Description:  JQuery scripts used by the 'Tell the World' website.
 */

$(document).ready(function(){

    /** -------------------------------------------------------------
     *           VARIABLES USED WITHIN THIS FILE
     *  -------------------------------------------------------------
     */
    var originalPostText;
    var editingPost = false;
    var originalCommentText;
    var editingComment = false;
  
    var StatusCode = {
      ERROR: 0,
      SUCCESS: 1,
      CENSORED: 2,
      INVALIDPASSWORD: 3
    };

    var messages = {
      accountDeleted: "Your account will now be deleted!",
      ajaxResponseError: "Error: Something went wrong whilst trying to process your request. Please contact the site's administrator.",
      completeAllFields: "Please complete ALL of the required data fields!",
      enterReplyFieldEmpty: "The 'Enter your reply' field cannot be left empty!",
      methodNotAllowedOnPage: "Sorry, you cannot perform the action on this page!",
      operationCancelled: "Operation cancelled.",
      unsavedChanges: "You must first save all changes before performing this action",
      userLoggedOut: "You are now logged out.",
      confirmBlockUser: "Are you sure that you want to block this user? Blocking users means that you will no longer be able to see their posts or comments, and that they will no longer be able to see your posts/comments.",
      confirmUnblockUser: "Are you sure you want to unblock this user?",
      confirmShowBlockedContent: "Proceeding further will show you content from a user that you have blocked. If you do not wish to see this content, press CANCEL.",
      confirmDeleteComment: "Are you sure you want to delete this comment?",
      confirmDeletePost: "Are you sure you want to delete this post?",
      confirmDeleteAccount: "Are you sure you want to delete your account?",
      confirmHidePost: "Are you sure that you want to hide this post?",
      confirmLogout: "Are you sure you want to log out of your account?",
      confirmUnhidePost: "Are you sure that you want to unhide this post?",
      confirmUnhideAllPosts: "Are you sure that you want to unhide all posts by this user?",
      confirmSaveChanges: "Are you sure you want to save these changes?"
    };

    var btnTexts = {
      hideReply: "Hide reply",
      reply: "Reply",
      hideComments: "Hide comments",
      viewComments: "View all comments",
      hideUpdate: "Hide Update",
      viewUpdate: "View Update"
    };
  
  
    /** -------------------------------------------------------------
     *           SHARED FUNCTIONS
     *  -------------------------------------------------------------
     */
  
    /**
     * Returns the contents of a Cookie with the name specified,
     * or null if the Cookie name was not found.
     * Needed to get the CSRF token for POST requests.
     * Source: https://docs.djangoproject.com/en/2.2/ref/csrf/
     */
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  
  
    /** -------------------------------------------------------------
     *           NAVBAR FUNCTIONS
     *  -------------------------------------------------------------
     */
  
    /**
     * Adds the active class to the current page link in the navbar.
     */
    $(function( ){
      var current = location.pathname;

      // If on the homepage change bg colour of brand
      if( $('.navbar-brand').attr('href').indexOf(current) !== -1) {
        $(".navbar-brand").css("backgroundColor", "black");
        $(".navbar-brand").css("color", "white");
        return;
      }

      // Only allow one page to be marked as active
      count = 0;
  
      $('.navbar-nav li a').each(function(){
        // Add active to dropdown menu toggle if child page active
        if($(this).parent().hasClass('dropdown-menu-item')) {
          if(count == 0) {
            if($(this).attr('href').indexOf(current) !== -1){
              $(this).parent().parent().parent().addClass('active');
              count = count + 1;
            }                        
          }
        }
        else if(count == 0) {
          if($(this).attr('href').indexOf(current) !== -1){
            $(this).parent().addClass('active');
            count = count + 1;
          }
        }  
      })
    });
  
  
    /**
     * Displays a dropdown's links when the user hovers over it.
     */ 
    $(".dropdown").hover(
      function () { $(this).addClass('open') },
      function () { $(this).removeClass('open') }
    );
  
  
    /** -------------------------------------------------------------
     *           LOGIN MODAL FUNCTIONS
     *  -------------------------------------------------------------
     */
  
    /**
     * Loads the loginModal into the page and shows it.
     */
    $("#loginBtn").on("click", function(e) {   
      $('#modal_container').empty();
  
      $('#modal_container').load("/loginmodal/", function(result){
        // Focus the username field when the modal is shown
        $('#loginModal').on('shown.bs.modal', function () {
          $('#username').focus();
        });
  
        $('#loginModal').modal('show');
      });
    }); 
  
  
    /**
     * Checks that the user has filled in both fields
     * in the LoginModal before submission.
     */
    $.validate_login = function() {
      var usernameLen = $("#username").val().length;  
      var passwordLen = $("#pwd").val().length;  
      
      if(usernameLen===0 || passwordLen===0) {
        alert(messages.completeAllFields);
        return false;
      }
      $('#loginModal').modal('hide');
      return true;
    };
  
  
    /** -------------------------------------------------------------
     *           ADD UPDATE MODAL FUNCTIONS
     *  -------------------------------------------------------------
     */
  
    /**
     * Handles the submit button click for the addUpdateModal.
     */
    $(document).on('click', '#addNewUpdatePostBtn', function() { 
      if ($.validate_addUpdate_fields()) {
        $.addNewUserUpdate();
      } else {
        return false;
      }
    });
  
  
    /**
     * Loads the addUpdateModal into the modal_container div and shows it. 
     */
    $.load_addUpdateModal = function() {
      $('#modal_container').empty();
  
      $('#modal_container').load("/addupdatemodal/", function(result){
        // Focus the username field when the modal is shown
        $('#addUpdateModal').on('shown.bs.modal', function () {
          $('#postTitle').focus();
        });
  
        $('#addUpdateModal').modal('show');
      });
    };
  
  
    /**
     * Opens the addUpdateModal if the user has not posted today.
     */
    $("#addUpdateBtn").click(function () {
      // Do not allow updates to be added from certain pages
      currentPathname = window.location.pathname
      methodNotAllowedHere = ["changeuserdetails", "changepassword"];
  
      for (i = 0; i < methodNotAllowedHere.length; i++) {
        if(currentPathname.includes(methodNotAllowedHere[i])) {
          alert(messages.methodNotAllowedOnPage);
          return false;
        }     
      }
  
      $.ajax({
        url: "/hasexceededmaxposts/",
        type: 'get',
        success: function (data) {
          if (data.status == StatusCode.SUCCESS) {
            // Show the add update modal 
            $.load_addUpdateModal();
          } else {
            alert(data.message);
          }  
        },
        error: function () {
          alert(messages.ajaxResponseError);
        }
      });
    }); 
  
  
    /**
     * Checks that the user has filled in all fields 
     * in the addUpdateModal before submission.
     */
    $.validate_addUpdate_fields = function() {
      var postTitleLen = $("#postTitle").val().length;  
      var postTextLen = $("#postText").val().length;  
      var postTagsLen = $("#tagDiv").val().length;  
      
      if(postTitleLen==0 || postTextLen==0 || postTagsLen==0 ) {
        alert(messages.completeAllFields);
        return false;
      }

      $('#addUpdateModal').modal('hide');
      return true;
    };
  
    
    /**
     * Hides the addUpdateModal modal.
     */
    $.errorAddUpdateModal = function(message) {
      $('#addUpdateModal').modal('show');
      alert(message);        
    };
  
  
    /**
     * Adds a new user update to the database.
     */
    $.addNewUserUpdate = function () {
      var p_postTitle = $("#postTitle").val();
      var p_postText  = $("#postText").val();
      var p_postTags = $("#tagDiv").val();
      var csrftoken = getCookie('csrftoken');
  
      $.post("/addnewupdate/",
      {
        postTitle: p_postTitle,
        postText: p_postText,
        postTags: JSON.stringify(p_postTags),
        csrfmiddlewaretoken: csrftoken,
      },
      function(data, status) {
        if (status === 'success') {
          if (data.status == StatusCode.SUCCESS) {
            alert(data.message);
            location.reload();
          } 
          else if (data.status == StatusCode.CENSORED) {
            $.censorNewUpdateModal(data.message);
          }
          else {
            $.errorAddUpdateModal(data.message);
          }
        }
        else {
          alert(messages.ajaxResponseError);
          $("#postTitle").val("");
        }
      });
    };
  
  
    /**
     * Clears the fields of the addUpdateModal when it is closed.
     */
    $('#addUpdateModal').on('hidden.bs.modal', function () {
      $('#frmAddUpdate')[0].reset();   
      $("#postTags").tagsinput('removeAll');       
    });
  
  
    /** -------------------------------------------------------------
     *           DELETE ACCOUNT MODAL FUNCTIONS
     *  -------------------------------------------------------------
     */
  
    /**
     * Loads the deleteAccountModal into the page and shows it. 
     */
    $("#deleteAccountBtn").click(function(){
      // Do not allow account to be to deleted from certain pages
      currentPathname = window.location.pathname
      methodNotAllowedHere = ["changeuserdetails", "changepassword"];
  
      for (i = 0; i < methodNotAllowedHere.length; i++) {
        if(currentPathname.includes(methodNotAllowedHere[i])) {
          alert(messages.methodNotAllowedOnPage);
          return false;
        }     
      }
  
      $('#modal_container').empty();
  
      $('#modal_container').load("/deleteaccountmodal/", function(result){
        $('#deleteAccountModal').modal('show');
      });
    });
  
  
    /**
     * Clears the fields of the deleteAccountModal when it is closed.
     */
    $('#deleteAccountModal').on('hidden.bs.modal', function () {
      $('#frmDeleteAccount')[0].reset();
    });
  
  
    /**
     * Deletes a user's account
     */
    $.delete_user_account = function (data) {
    // post to account deleted here with reasons no password
    //document.location.href =  "/accountdeleted/";
    var csrftoken = getCookie('csrftoken');
    var p_reason = $(reasonsList).val();
  
    $.redirect("/accountdeleted/", {
      'reason': p_reason,
      'csrfmiddlewaretoken': csrftoken });
    };
  
  
    /**
     * Confirms that a user wishes to delete their account
     */
    $.confirm_deleteAccount = function (data) {
      if (confirm(messages.confirmDeleteAccount)) {
        alert(messages.accountDeleted);
        $("#deleteAccountModal").modal('toggle');
        $.delete_user_account();
        return true;
      }
      else {
        alert(messages.operationCancelled);
        $("#deleteAccountModal").modal('toggle');
        return false;
      }
    };

    $.invalid_password_entered = function (data) { 
      alert(data.message);
      return false;
    }
  
    /**
     * Checks that the user has entered their password correctly
     * before the account can be deleted.
     */
    $.validate_deleteAccount = function () {
      var password = $("#pwd_deleteModal").val()
      $.entered_password_is_valid(password);
    };
  
  
    /**
     * Checks that the user has entered in their password correctly
     * before performing delete account.
     */
    $.entered_password_is_valid = function (p_password) {
      result = false;
      var csrftoken = getCookie('csrftoken');
  
      $.post("/checkuserpassword/",
      {
        pwd: p_password,
        csrfmiddlewaretoken: csrftoken
      },
      function (data, status) {
        if (status === 'success') {
          if (data.status == StatusCode.SUCCESS) {
            $.confirm_deleteAccount(data);
          } 
          else if (data.status == StatusCode.INVALIDPASSWORD) {
            $.invalid_password_entered(data);
          } 
          else {
            alert(data.message);
            $("#deleteAccountModal").modal('toggle');
          }
        }
        else {
          alert(messages.ajaxResponseError);
          $("#deleteAccountModal").modal('toggle');
        }
      });
    };
  
  
    /** -------------------------------------------------------------
     *           CONFIRM LOGOUT FUNCTION
     *  -------------------------------------------------------------
     */
  
    /**
     * Confirm that the user wishes to log out.
     */
    $.confirm_logout = function() {
      var r = confirm(messages.confirmLogout);
  
      if (r == true) {
        alert(messages.userLoggedOut);
      } else {
        return false;
      } 
    };
  
  
    /** -----------------------------------------------------------------
     *           CENSORSHIP METHODS
     * ------------------------------------------------------------------
     */
  
    /**
     * Changes the element text to the one passed.
     * Used as a callback because of the asynchromnous nature of AJAX calls.
     */
    $.updateElementText = function (ele, newText) {
      ele.focus().val(newText);
      //ele.focus();
    };
  
  
    /**
     * Censors text in the element passed.
     * ele = $("#postTitle")     etc
     */
    $.censorElementText = function (ele) {
      var in_toCensor = ele.val();
      var csrftoken = getCookie('csrftoken');
  
      $.post("/censortext/",
      {
        textToCensor: in_toCensor,
        csrfmiddlewaretoken: csrftoken,
      },
      function(data, status) {
        if (status === 'success') { 
          if (data.status == StatusCode.SUCCESS) {
            $.updateElementText(ele, data.message);  
          } else {
            alert(data.message);
          }
        }
        else {
          alert(messages.ajaxResponseError);
        }
      });
    };
  
  
    /**
     * Updates an array element. Note this is done as a callback
     * because of the Asynchronous nature of AJAX.
     */
    $.updatePostTags = function(ele_postTags, data) {
      var newTags = JSON.parse(data);
  
      ele_postTags.tagsinput('removeAll');
      newTags.forEach(function (item, index) {
        ele_postTags.tagsinput('add', item);
      });
  
      ele_postTags.tagsinput('refresh');
    }; 
            
              
    /**
     * Censors text in the tag element passed.
     * Note: Arrays are passed by reference.
     */
    $.censorPostTags = function (ele_postTags) {
      var csrftoken = getCookie('csrftoken');
      var p_postTags = ele_postTags.val();
  
      $.post("/censortext/",
      {
        textToCensor: JSON.stringify(p_postTags),
        csrfmiddlewaretoken: csrftoken,
      },
      function(data, status) {
        if (status === 'success') {
          if (status === 'success') { 
            if (data.status == StatusCode.SUCCESS) {
              $.updatePostTags(ele_postTags, data.message); 
            } else {
              alert(data.message);
            }
          }               
        }
        else {
          alert(messages.ajaxResponseError);
        }
      });
    };
  
  
    /**
     * This censors the content of the new update modal after
     * banned words are detected in it.
     */
    $.censorNewUpdateModal = function (message) {
      alert(message);
      
      var ele_postTitle = $("#postTitle");
      var ele_postText  = $("#postText");
      var ele_postTags = $("#tagDiv");

      $('#addUpdateModal').modal('show');
      $.censorElementText(ele_postTitle);
      $.censorElementText(ele_postText);
      $.censorPostTags(ele_postTags);
    };


    $.confirm_block_user = function(username) {
      return confirm(message.confirmBlockUser);
    };

    $.block_user = function(in_username) {
      if(editingPost || editingComment) {
        alert(messages.unsavedChanges);
        return;
      } 

      if($.confirm_block_user(in_username)==true) {
        var csrftoken = getCookie('csrftoken');

        $.post("/blockuser/",
        {
          username: in_username,
          csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
          if (status === 'success') {
            if (data.status == StatusCode.SUCCESS) {
              alert(data.message);
              location.reload();
            } else {
              alert(data.message);
            }
          }
          else {
            alert(messages.ajaxResponseError);
          }
        });     
      }
    };


    $.confirm_unblock_user = function(username) {
      return confirm(messages.confirmUnblockUser);
    };

    $.unblock_user = function(in_username) {
      if($.confirm_unblock_user(in_username)==true) {
        var csrftoken = getCookie('csrftoken');

        $.post("/unblockuser/",
        {
          username: in_username,
          csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
          if (status === 'success') {
            if (data.status == StatusCode.SUCCESS) {
              alert(data.message);
              location.reload();
            } else {
              alert(data.message);
            }
          }
          else {
            alert(messages.ajaxResponseError);
          }
        });     
      }
    };


    $.confirm_view_blockeduser_posts = function(username) {
      return confirm(messages.confirmShowBlockedContent);
    };


    $.confirm_hide_post = function() {
      return confirm(messages.confirmHidePost);
    };


    $.hide_post = function(in_postID) {
      if(editingPost || editingComment) {
        alert(messages.unsavedChanges);
        return;
      }
      
      if($.confirm_hide_post()==true) {
        var csrftoken = getCookie('csrftoken');

        $.post("/hidepost/",
        {
          postID: in_postID,
          csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
          if (status === 'success') {
            if (data.status == StatusCode.SUCCESS) {
              alert(data.message);
              location.reload();
            } else {
              alert(data.message);
            }
          }
          else {
            alert(messages.ajaxResponseError);
          }
        });     
      }
    };


    $.confirm_unhide_all_user_posts = function() {
      return confirm(messages.confirmUnhideAllPosts);
    };


    $.unhide_all_user_posts = function(in_user) {      
      if($.confirm_unhide_all_user_posts()==true) {
        var csrftoken = getCookie('csrftoken');

        $.post("/unhideuserposts/",
        {
          user: in_user,
          csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
          if (status === 'success') {
            if (data.status == StatusCode.SUCCESS) {
              alert(data.message);
              window.location = window.location.href.split("?")[0];
            } else {
              alert(data.message);
            }
          }
          else {
            alert(messages.ajaxResponseError);
          }
        });     
      }
    };    


    $.confirm_unhide_post = function() {
      return confirm(messages.confirmUnhidePost);
    };


    $.unhide_post = function(in_postID) {
      if($.confirm_unhide_post()==true) {
        var csrftoken = getCookie('csrftoken');

        $.post("/unhidepost/",
        {
          postID: in_postID,
          csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
          if (status === 'success') {
            if (data.status == StatusCode.SUCCESS) {
              alert(data.message);
              window.location = window.location.href.split("?")[0];
            } else {
              alert(data.message);
            }
          }
          else {
            alert(messages.ajaxResponseError);
          }
        });     
      }
    };



    /** -----------------------------------------------------------------
     *           EDIT COMMENT METHODS
     * ------------------------------------------------------------------
     */
  
    /**
     * Confirms that the user wishes to edit their comment.
     */
    $.confirm_edit_comment = function() {
      return confirm(messages.confirmSaveChanges);
    };
  
  
    /**
     * Handles the edit user comment link click.
     */
    $.edit_comment = function (in_commentID) {
      // Only allow the user to edit one comment at a time
      if ( editingComment || editingPost ) {
        alert(messages.unsavedChanges);
        return false;
      }
      
      editingComment = true;
      
      var textCommentID = "#text_comment_" + in_commentID;
      originalCommentText = $(textCommentID).html();  // Store the current comment text
      
      // Load the page element and insert it into the panel
      url = '/editusercomment/' + in_commentID;
      $(textCommentID).load(url);
    
      // Focus on the input and position cursor at end of text to edit
      $("#edit_comment_box").focus().val(originalCommentText);
      return true;
    };
  
  
    /**
     * Replaces the edit box with the edited comment after saving.
     */
    $.show_new_comment_text = function(textCommentID, commentText) {
      editingComment = false;
      $(textCommentID).html(commentText);
    } 
    
  
    /**
     * Handles saving changes to a user's commentText.
     */
    $.save_edit_comment = function (in_commentID) {
      var textCommentID = "#text_comment_" + in_commentID;
      var currentText = $("#edit_comment_box").val();
  
      if($.confirm_edit_comment()==true) {
        var csrftoken = getCookie('csrftoken');
  
        $.post("/editusercomment/",
        {
          commentID: in_commentID,
          commentText: currentText,
          csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
          if (status === 'success') {
            if (data.status == StatusCode.SUCCESS) {
              alert(data.message);
              $.show_new_comment_text(textCommentID, currentText);
            } 
            else if (data.status == StatusCode.CENSORED) {
              $.censorElementText($("#edit_comment_box"));
              alert(data.message);
            } 
            else {
              alert(data.message);
            }
          }
          else {
            alert(messages.ajaxResponseError);
          }
        });
      }
    };    
  
  
    /**
     * Retores the original commentText when editing is cancelled.
     */
    $.cancel_edit_comment = function (commentID) {
      var textCommentID = "#text_comment_" + commentID;
  
      $(textCommentID).html(originalCommentText);   
      editingComment = false;
    };
  
  
    /** -----------------------------------------------------------------
     *           EDIT POST METHODS
     * ------------------------------------------------------------------
     */
  
    /**
     * Confirms that the user wishes to edit their post.
     */
    $.confirm_edit_post = function() {
      return confirm(messages.confirmSaveChanges);
    };
  
  
    /**
     * Handles the edit user post link click.
     */
    $.edit_post = function (in_postID) {
      // Only allow the user to edit one thing at a time.
      if (editingPost || editingComment ) {
        alert(messages.unsavedChanges);
        return false;
      }
      
      editingPost = true;
      
      var textPostID = "#text_post_" + in_postID;
      originalPostText = $(textPostID).html();  // Store the current post text
      
      // If the collapse is not showing, show it
      var collapsePostID = "#collapse" + in_postID;
      $(collapsePostID).collapse("show");
      $(collapsePostID).siblings('.panel-header').children('.align-panel-text-right').children('.collapse_btn').text(btnTexts.hideUpdate);

      // Load the page element and insert it into the panel
      url = '/edituserpost/' + in_postID;
      $(textPostID).load(url);
    
      // Focus on the input and position cursor at end of text to edit
      $("#edit_post_box").focus().val(originalPostText);
      return true;
    };
  
  
    /**
     * Replaces the edit box with the edited post after saving.
     */
    $.show_new_post_text = function(textPostID, postText) {
      editingPost = false;
      $(textPostID).html(postText);
    } 
  
    /**
     * Handles saving changes to a user's postText.
     */
    $.save_edit_post = function (in_postID) {
      var textPostID = "#text_post_" + in_postID;
      var currentText = $("#edit_post_box").val();
  
      if($.confirm_edit_post()==true) {
        var csrftoken = getCookie('csrftoken');
  
        $.post("/edituserpost/",
        {
          postID: in_postID,
          postText: currentText,
          csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
          if (status === 'success') {
            if (data.status == StatusCode.SUCCESS) {
              alert(data.message);
              $.show_new_post_text(textPostID, currentText);
            } 
            else if (data.status == StatusCode.CENSORED) {
              $.censorElementText($("#edit_post_box"));
              alert(data.message);
            } 
            else {
              alert(data.message);
            }
          }
          else {
            alert(messages.ajaxResponseError);
          }
        });
      }
    };    
  
  
    /**
     * Retores the original postText when editing is cancelled.
     */
    $.cancel_edit_post = function (postID) {
      var textPostID = "#text_post_" + postID;
  
      $(textPostID).html(originalPostText);  
      editingPost = false;
    };
  
  
    /**
     * Stops user from opening or closing post collapses whilst editing.
     */
    $('.collapse_btn').on('click', function(event) {
      if(editingComment || editingPost) {
        alert(messages.unsavedChanges);
        event.stopPropagation();
        return;
      }
      
      /* Toggle the text shown on the update collapse button */
      if ( $(this).text() == btnTexts.viewUpdate)  {
        $(this).text(btnTexts.hideUpdate);
      } else {
        $(this).text(btnTexts.viewUpdate);
      }
    });
  
  
    /** -----------------------------------------------------------------
     *           DELETE POST METHODS
     * ------------------------------------------------------------------
     */
  
    /**
     * Confirms that the user wishes to delete their post.
     */
    $.confirm_delete_post = function() {
      return confirm(messages.confirmDeletePost);
    };
  
  
    /**
     * Handles the delete user post event.
     */
    $.delete_post = function (in_postID) {
      if(editingPost || editingComment) {
        alert(messages.unsavedChanges);
        return;
      } 

      if($.confirm_delete_post()==true) {
        var csrftoken = getCookie('csrftoken');
  
        $.post("/deleteuserpost/",
        {
          postID: in_postID,
          csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
          if (status === 'success') {
            if (data.status == StatusCode.SUCCESS) {
              alert(data.message);
              location.reload();
            } else {
              alert(data.message);
            }
          }
          else {
            alert(messages.ajaxResponseError);
          }
        });
      }
    };
  
  
    /** -----------------------------------------------------------------
     *           UPDATE PANEL METHODS
     * ------------------------------------------------------------------
     */
  
    /**
      * Shows the comment panel of an update collapse when it is opened.
      */
    $('.panel-collapse').on('shown.bs.collapse', function () {          
      $(this).siblings('.comment-panel').slideToggle();
    });
  
  
    /**
      * When an update collapse is closed, this hides the comment panel
      * and its contents.
      */
    $('.panel-collapse').on('hidden.bs.collapse', function () {
      $(this).siblings('.comment-panel').slideToggle();
      $(this).siblings('.comment-panel').children('.user-reply-section').hide();
      $(this).siblings('.comment-panel').children('.user-comment-section').hide();
      
      $(this).siblings('.comment-panel').children('.reply_btn').text(btnTexts.reply);
      $(this).siblings('.comment-panel').children('.view_comments_btn').text(btnTexts.viewComments);
    });
  
      
    /**
      * Shows the user reply section when the reply button is clicked
      */
    $('.reply_btn').on('click', function () {
      $(this).siblings('.user-reply-section').children('.user-comment-input-area').val("");
      /* Toggle the text shown on the reply button */
      if ( $(this).text() == btnTexts.reply)  {
        $(this).text(btnTexts.hideReply);
      } else {
        $(this).text(btnTexts.reply);
      }
      $(this).siblings('.user-reply-section').slideToggle();
      $(this).siblings('.user-reply-section').children('.user-comment-input-area').focus();
    });
  
  
    /**
      * Toggles the visibility of the user comment section when the
      * view/hide comments button is clicked, and populates it with
      * user comments where necessary.
      */
    $('.view_comments_btn').on('click', function () {
      if ( $(this).text() == btnTexts.viewComments)  {
        var postID = $(this).parent().attr('id');
        postID = postID.replace('comments','');
        $.fetchComments($(this), postID);
        $(this).text(btnTexts.hideComments);
      } else {
        $(this).text(btnTexts.viewComments);
        editingComment = false;
      }
      $(this).siblings('.user-comment-section').slideToggle();
    });
      
      
    /**
      * Fetches comments attached to a post and adds them to the user-comment-section.
      */
    $.fetchComments = function ($this, in_postID) {
      var url="/usercomments/?postID=" + in_postID;
  
      $this.siblings('.user-comment-section').empty();
      $this.siblings('.user-comment-section').load(url);        
    };
  
  
    /**
    * Resizes the comment text area if necessary when text is inputted 
    */
    $('.user-comment-input-area').on('keyup input', function () {
      var offset = this.offsetHeight - this.clientHeight;
      $(this).css('height', 'auto').css('height', this.scrollHeight + offset);
    });    
  
    /** 
     * Resizes editing textareas  if necessary when the window is resized. 
     */
    $(window).on('resize', function () {
      $this1 = $( '.user-comment-input-area' );
      $this1.trigger('input'); // trigger input event to call function above
    });  
  
  
    /** -----------------------------------------------------------------
     *           ADD COMMENT METHODS
     * ------------------------------------------------------------------
     */
  

    /**
     * Triggers the reply_btn click when the user clicks on the
     * .user-no-comments-text paragraph
     */ 
    $('.user-comment-section').on('click', '.user-no-comments-text', function() {
      $(this).parent().parent().children('.reply_btn').trigger('click');
    });


    /**
      * Clears user input and closes the user reply section when
      * the cancel reply button is clicked.
      */
    $('.cancel_reply_btn').on('click', function () {
      $(this).siblings(".user-comment-input-area").val("");
      $(this).parent().parent().children('.reply_btn').text(btnTexts.reply);
      $(this).parent().slideToggle();
    });
  
  
    /**
      * This callback is used because of the Asychronous nature of AJAX
      */
    $.unable_to_add_comment = function(post_reply_btn, message) {
      post_reply_btn.prop('disabled', false);
      $.censorElementText(post_reply_btn.siblings(".user-comment-input-area"));
      alert(message);      
      post_reply_btn.siblings(".user-comment-input-area").focus();
      return false;
    }  
  
    /**
      * This callback is used because of the Asychronous nature of AJAX
      */
    $.comment_was_censored = function(post_reply_btn, message) {
      post_reply_btn.prop('disabled', false);
      alert(message);
      return false;
    }

  
    /**
      * This callback is used because of the Asychronous nature of AJAX
      */
    $.postedCommentCallback = function (post_reply_btn, message) {
      // Reenable the post reply button because the comment post has been dealt with
      post_reply_btn.prop('disabled', false);
  
      // Tidy up the comment input area, then hide it
      post_reply_btn.siblings(".user-comment-input-area").val("");
      post_reply_btn.parent().parent().children('.reply_btn').text(btnTexts.reply);
      post_reply_btn.parent().slideToggle();
  
      var commentSection = post_reply_btn.parent().siblings('.user-comment-section');

      if(commentSection.is(":visible")){
        // If the comment section is visible trigger the viewcomments button
        // to update it, showing the newly posted comment
        alert(message);

        $comments_btn = commentSection.siblings('.view_comments_btn');
        $comments_btn.trigger('click'); // hide comments
        $comments_btn.trigger('click'); // show comments
      } else {
        alert(message);
      }
    };
  
  
    /**
      * Fetches comments attached to a post and adds them to the user-comment-section.
      */
    $.postComment = function (postBtnElement, in_postID, in_commentText) {
      var csrftoken = getCookie('csrftoken');

      // Disable the post button to stop the user from spamming comments
      postBtnElement.prop('disabled', true);

      $.post("/addusercomment/",
      {
        postID: in_postID,
        commentText: in_commentText,
        csrfmiddlewaretoken: csrftoken,
      },
      function(data, status) {
        if (status === 'success') {
          if (data.status == StatusCode.SUCCESS) {
            $.postedCommentCallback(postBtnElement, data.message);
          } 
          else if (data.status == StatusCode.CENSORED) {
            $.comment_was_censored(postBtnElement, data.message);
          } 
          else {
            $.unable_to_add_comment(postBtnElement, data.message);            
          }
        }
        else {
          $.unable_to_add_comment(postBtnElement,  messages.ajaxResponseError);
        }
      });
    };
  
  
    /**
      * Handles adding a comment to the post when the post reply button is clicked.
      */
    $('.post_reply_btn').on('click', function () {
      var commentText = $(this).siblings(".user-comment-input-area").val().trim();
      var commentLength = commentText.length;
      var postID = $(this).parent().parent().attr('id');
      postID = postID.replace('comments','');
      
      // No empty comments are allowed
      if (commentLength == 0) {
        alert(messages.enterReplyFieldEmpty);
        $(this).siblings(".user-comment-input-area").focus();
        return false;
      };
      
      // Add comment to DB
      $.postComment($(this), postID, commentText);
    });    
     
  
    /** -----------------------------------------------------------------
     *           DELETE COMMENT METHODS
     * ------------------------------------------------------------------
     */
  
    /**
     * Confirms that the user wishes to delete their comment.
     */
    $.confirm_delete_comment = function() {
      return confirm(messages.confirmDeleteComment);
    };
  
  
    /**
     * Refreshes the comments section after deleting a comment.
     */
    $.comment_deleted = function(viewCommentsBtn) {
      viewCommentsBtn.trigger('click');   // Hide comments
      viewCommentsBtn.trigger('click');   // Show comments
    } 
  
    /**
     * Handles the delete user comment event.
     */
    $.delete_comment = function (in_commentID) {
      if(editingPost || editingComment) {
        alert(message.unsavedChanges);
        return;
      } 

      if($.confirm_delete_comment()==true) {
        var csrftoken = getCookie('csrftoken');
        var textCommentID = "#text_comment_" + in_commentID;
        var viewCommentsBtn = $(textCommentID).parent().parent().parent().children('.view_comments_btn');
  
        $.post("/deleteusercomment/",
        {
            commentID: in_commentID,
            csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
          if (status === 'success') {
            if (data.status == StatusCode.SUCCESS) {
              alert(data.message);
              $.comment_deleted(viewCommentsBtn);
            } else {
              alert(data.message);
            }
          }
          else {
            alert(messages.ajaxResponseError);
          }
        });
      }
    };
  
});
  