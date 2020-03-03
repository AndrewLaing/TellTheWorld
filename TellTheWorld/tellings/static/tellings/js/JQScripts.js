/*
 * Filename:     JQScripts.js
 * Author:       Andrew Laing
 * Email:        parisianconnections@gmail.com
 * Last updated: 24/02/2020.
 * Description:  JQuery scripts used by the 'Tell the World' website.
 */

$(document).ready(function(){

    /** -------------------------------------------------------------
     *           VARIABLES USED FOR EDITING POSTS AND COMMENTS
     *  -------------------------------------------------------------
     */
    var originalPostText;
    var editingPost = false;
    var originalCommentText;
    var editingComment = false;
  
  
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
        alert("Error - both fields must be completed!");
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
  
      $('#modal_container').load("/addupdatemodal/",function(result){
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
          alert("Sorry you are unable to add updates from this page!");
          return false;
        }     
      }
  
      $.ajax({
        url: "/haspostedtoday/",
        type: 'get',
        success: function (data) {
          if (data === 'true') {
            alert("Sorry. You have already posted today's update.");
          } else if (data!=='false') {
            alert("Database error: please contact the administrator.");    
          } else {
            // Show the add update modal 
            $.load_addUpdateModal();
          }   
        },
        error: function () {
          alert('Error: please contact the site administrator.');
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
        alert("Please complete ALL of the data fields!");
        return false;
      }

      $('#addUpdateModal').modal('hide');
      return true;
    };
  
  
    /**
     * Verifies that the user has chosen a unique title
     * for their post on the addUpdateModal when they leave the
     * postTitle field.
     */
    $(document).on('change', "#postTitle", function (e) {
      var p_postTitle = $("#postTitle").val();
      var csrftoken = getCookie('csrftoken');
  
      $.post("/titleexists/",
      {
        title: p_postTitle,
        csrfmiddlewaretoken: csrftoken,
      },
      function(data, status) {
        if(status==='success') {
          if(data==='true') {
            alert('Sorry. You must choose a unique title.');
            $("#postTitle").val("");
            $('#postTitle').focus();
          } else if(data==='censored') {
            alert('Sorry, we cannot accept the title you have chosen as it contains one or more banned words. Please refer to our acceptable usage policy for guidance.');
            $("#postTitle").val("");
            $('#postTitle').focus();
          } else if (data!=='false') {
            alert("Database error: please contact the administrator.");    
            $("#addUpdateModal").modal('toggle');  // Hide the add update modal.
          }  
        }
        else {
          alert("Database error: please contact the administrator.");
          $("#addUpdateModal").modal('toggle');
        }
      });
    }); 
  
    
    /**
     * Hides the addUpdateModal modal.
     */
    $.errorAddUpdateModal = function(msg) {
      $('#addUpdateModal').modal('show');
      alert(msg);        
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
          if(data==='true') {
            alert('Your update has been added.');
            location.reload();
          } else if (data === 'censored') {
            alert('Sorry, we cannot accept your post data as it contains one or more banned words. The update has been censored. You can either now post the censored version of the update, or rewrite it with the banned words omitted.  Please refer to our acceptable usage policy for guidance.');
            $.censorNewUpdateModal();
          } else if (data!=='false') {
            $.errorAddUpdateModal("Database error: please contact the administrator.");    
          } else {
            $.errorAddUpdateModal('Sorry. Unable to add your update.');
          }    
        }
        else {
          alert("Database error: please contact the administrator.");
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
          alert("Sorry you are unable to delete your account from this page!");
          return false;
        }     
      }
  
      $('#modal_container').empty();
  
      $('#modal_container').load("/deleteaccountmodal/",function(result){
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
      if (data === 'true') {
        if (confirm("Are you sure you want to delete your account?")) {
          alert("Your account will now be deleted!");
          $("#deleteAccountModal").modal('toggle');
          $.delete_user_account();
          return true;
        }
        else {
          alert("Operation cancelled.");
          $("#deleteAccountModal").modal('toggle');
          return false;
        }
      }
      else {
        alert('You have entered an incorrect password!');
        return false;
      }
    };
  
  
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
          if (data === 'true' || data === 'false') {
            $.confirm_deleteAccount(data);
          } else {
            alert("Error: Cannot perform this action. please contact the administrator.");
            $("#deleteAccountModal").modal('toggle');
          }
        }
        else {
          alert("Error: Cannot perform this action. please contact the administrator.");
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
      var r = confirm("Are you sure you want to log out of your account?");
  
      if (r == true) {
        alert("You are now logged out.");
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
          $.updateElementText(ele, data);   
        }
        else {
          alert("AJAX error: please contact the administrator.");
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
          $.updatePostTags(ele_postTags, data);               
        }
        else {
          alert("AJAX error: please contact the administrator.");
        }
      });
    };
  
  
    /**
     * This censors the content of the new update modal after
     * banned words are detected in it.
     */
    $.censorNewUpdateModal = function () {
      var ele_postTitle = $("#postTitle");
      var ele_postText  = $("#postText");
      var ele_postTags = $("#tagDiv");

      $('#addUpdateModal').modal('show');
      $.censorElementText(ele_postTitle);
      $.censorElementText(ele_postText);
      $.censorPostTags(ele_postTags);
    };


    $.confirm_block_user = function(username) {
      var msg = "Are you sure that you want to block '" + username + "'?"
      msg = msg + " Blocking posts by this user means that you will no longer be able to see their posts or comments, and that they will no longer be able to see your posts/comments."
      return confirm(msg);
    };

    $.block_user = function(in_username) {
      if(editingPost || editingComment) {
        alert("Cannot block a user whilst there are still unsaved changes on this page.");
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
            if (data === 'true') {
              alert('You have successfully blocked the user.');
              location.reload();
            } else if (data === 'admin') {
              alert('Sorry, we cannot allow you to block posts or comments from an administrator. If you wish to complain about the posts or comments of an administrator, please send an email to manager@ttw.com. All complaints will be dealt with confidentially.');
            } else {
              alert(data);
            }
          }
          else {
            alert("Database error: please contact the administrator.");
          }
        });     
      }
    };


    $.confirm_unblock_user = function(username) {
      var msg = "Are you sure that you want to unblock '" + username + "'?"
      return confirm(msg);
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
            if (data === 'true') {
              alert('You have successfully unblocked the user.');
              location.reload();
            } else {
              alert(data);
            }
          }
          else {
            alert("Database error: please contact the administrator.");
          }
        });     
      }
    };


    $.confirm_view_blockeduser_posts = function(username) {
      var msg = "Proceeding further will show you content from a user that you have blocked. If you do not wish to see this content, press CANCEL."
      return confirm(msg);
    };


    $.confirm_hide_post = function() {
      var msg = "Are you sure that you want to hide this post?";
      return confirm(msg);
    };


    $.hide_post = function(in_postID) {
      if(editingPost || editingComment) {
        alert("Cannot hide this post whilst there are still unsaved changes on this page.");
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
            if (data === 'true') {
              alert('The post will now be hidden from you.');
              location.reload();
            } else {
              alert(data);
            }
          }
          else {
            alert("Database error: please contact the administrator.");
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
      return confirm("Are you sure you want to save your changes?");
    };
  
  
    /**
     * Handles the edit user comment link click.
     */
    $.edit_comment = function (in_commentID) {
      // Only allow the user to edit one comment at a time
      if ( editingComment || editingPost ) {
        alert("You have unsaved changes!");
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
            if (data === 'true') {
              alert('Your comment has been updated.');
              $.show_new_comment_text(textCommentID, currentText);
            } else if (data === 'censored') {
              $.censorElementText($("#edit_comment_box"));
              alert('Sorry, we cannot accept your edit as it contains one or more banned words. Please refer to our acceptable usage policy for guidance.');
            } else {
              alert(data);
            }
          }
          else {
            alert("Database error: please contact the administrator.");
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
      return confirm("Are you sure you want to save your changes?");
    };
  
  
    /**
     * Handles the edit user post link click.
     */
    $.edit_post = function (in_postID) {
      // Only allow the user to edit one thing at a time.
      if (editingPost || editingComment ) {
        alert("You have unsaved changes!");
        return false;
      }
      
      editingPost = true;
      
      var textPostID = "#text_post_" + in_postID;
      originalPostText = $(textPostID).html();  // Store the current post text
      
      // If the collapse is not showing, show it
      var collapsePostID = "#collapse" + in_postID;
      $(collapsePostID).collapse("show");
      $(collapsePostID).siblings('.panel-header').children('.align-panel-text-right').children('.collapse_btn').text("Hide Update");

  
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
            if (data === 'true') {
              alert('Your post has been updated.');
              $.show_new_post_text(textPostID, currentText);
            } else if (data === 'censored') {
              $.censorElementText($("#edit_post_box"));
              alert('Sorry, we cannot accept your edit as it contains one or more banned words. The edit has been censored. You can either now post the censored version of the edit, or rewrite it with the banned words omitted. Please refer to our acceptable usage policy for guidance.');
            } else {
              alert(data);
            }
          }
          else {
            alert("Database error: please contact the administrator.");
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
        alert("You still have unsaved changes!");
        event.stopPropagation();
        return;
      }
      
      /* Toggle the text shown on the update collapse button */
      if ( $(this).text() == "View Update")  {
        $(this).text("Hide Update");
      } else {
        $(this).text("View Update");
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
      return confirm("Are you sure you want to delete this post?");
    };
  
  
    /**
     * Handles the delete user post event.
     */
    $.delete_post = function (in_postID) {
      if(editingPost || editingComment) {
        alert("Cannot delete this post whilst there are still unsaved changes on this page.");
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
            if (data === 'true') {
              alert('Your post has been deleted.');
              location.reload();
            } else {
              alert(data);
            }
          }
          else {
            alert("Database error: please contact the administrator.");
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
      $(this).siblings('.user-reply-section').slideToggle();
      $(this).siblings('.user-reply-section').children('.user-comment-input-area').focus();
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
        $.fetchComments($(this), postID);
        $(this).text("Hide comments");
      } else {
        $(this).text("View all comments");
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
      $(this).parent().parent().children('.reply_btn').text("Reply");
      $(this).parent().slideToggle();
    });
  
  
    /**
      * This callback is used because of the Asychronous nature of AJAX
      */
    $.postedCommentCallback = function (post_reply_btn, postID, response) {
      // Reenable the post reply button because the comment post has been dealt with
      post_reply_btn.prop('disabled', false);

      if (response == 'false') {
        alert("Error: Unable to add your comment! Please contact the administrator!");
        return false;
      } else if (response == 'censored') {
        $.censorElementText(post_reply_btn.siblings(".user-comment-input-area"));
        alert('Sorry, we cannot accept your comment as it contains one or more banned words. The comment has been censored. You can either now post the censored version of the comment, or rewrite it with the banned words omitted.  Please refer to our acceptable usage policy for guidance.');
        post_reply_btn.siblings(".user-comment-input-area").focus();
        return false;
      }
  
      // Tidy up the comment input area, then hide it
      post_reply_btn.siblings(".user-comment-input-area").val("");
      post_reply_btn.parent().parent().children('.reply_btn').text("Reply");
      post_reply_btn.parent().slideToggle();
  
      var commentSection = post_reply_btn.parent().siblings('.user-comment-section');

      if(commentSection.is(":visible")){
        // If the comment section is visible trigger the viewcomments button
        // to update it, showing the newly posted comment
        alert("Your comment has been posted.");

        $comments_btn = commentSection.siblings('.view_comments_btn');
        $comments_btn.trigger('click'); // hide comments
        $comments_btn.trigger('click'); // show comments
      } else {
        alert("Your comment has been posted.");
      }
    };


    $errorPostComment = function(post_reply_btn, msg) {
      post_reply_btn.prop('disabled', false);
      alert(msg);
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
          if(data == 'true') {
            $.postedCommentCallback(postBtnElement, in_postID, 'true');
          } else if (data == 'censored') {
            $.postedCommentCallback(postBtnElement, in_postID, 'censored');
          } else {
            $errorPostComment(postBtnElement, "Error: Unable to add your comment! Please contact the administrator!");
          }
        }
        else {
          $errorPostComment(postBtnElement, "Error: Unable to add your comment! Please contact the administrator!");
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
        alert("The 'Enter your reply' field cannot be left empty!");
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
      return confirm("Are you sure you want to delete this comment?");
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
        alert("Cannot delete this comment whilst there are still unsaved changes on this page.");
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
            if (data === 'true') {
              alert('The comment has been deleted.');
              $.comment_deleted(viewCommentsBtn);
            } else {
              alert(data);
            }
          }
          else {
            alert("Database error: please contact the administrator.");
          }
        });
      }
    };
  
});
  