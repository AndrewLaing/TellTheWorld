/*
 * Filename:     JQScripts.js
 * Author:       Andrew Laing
 * Email:        parisianconnections@gmail.com
 * Last updated: 29/01/2020.
 * Description:  JQuery scripts used by the 'Tell the World' website.
 */

$(document).ready(function(){

    /**
     * Variables used for editing posts.
     */
    var originalPostText;
    var editingPost = false;

    /**
     * Adds the active class to the current page link in the navbar
     * so that it can be styled with css.
     */
    $(function( ){
        $('a').each(function() {
            if($(this).prop('href') == window.location.href) {
               $(this).addClass('active'); 
               $(this).parents('li').addClass('active');
            }
        });
    });


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
     * Displays a dropdown's links when the user hovers over it.
     */ 
    $(".dropdown").hover(
        function () { $(this).addClass('open') },
        function () { $(this).removeClass('open') }
    );


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


    $.delete_user_account = function (data) {
        // post to account deleted here with reasons no password
        //document.location.href =  "/accountdeleted/";
        var csrftoken = getCookie('csrftoken');
        var p_reason = $(reasonsList).val();

        $.redirect("/accountdeleted/", {
            'reason': p_reason,
            'csrfmiddlewaretoken': csrftoken });
    };

    $.confirm_deleteAccount = function (data) {
        if (data === 'True') {
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
                //alert("Data: " + data + "\nStatus: " + status);
                if (status === 'success') {
                    if (data === 'True' || data === 'False') {
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


    /**
     * Checks that the user has entered their password correctly
     * before the account can be deleted.
     */
    $.validate_deleteAccount = function () {
        var password = $("#pwd_deleteModal").val()
        $.entered_password_is_valid(password);
    };


    /**
     * Loads the addUpdateModal into the page and shows it. 
     */
    $.load_addUpdateModal = function() {
        $('#modal_container').empty();

        $('#modal_container').load("/addupdatemodal/",function(result){

            // Event handler to focus the username field when
            // the modal is shown
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
                if (data === 'True') {
                    // User has already posted today!
                    alert("Sorry. You have already posted today's update.");
                } else if (data!=='False') {
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
        return true;
    };


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
        return true;
    };


    /**
     * Confirms that the user logout wishes to log out.
     */
    $.confirm_logout = function() {
        var r = confirm("Are you sure you want to log out of your account?");

        if (r == true) {
            alert("You are now logged out.");
        } else {
            return false;
        } 
    };


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
                if(data==='True') {
                    alert('Sorry. You must choose a unique title.');
                    $("#postTitle").val("");
                    $('#postTitle').focus();
                } else if(data==='Censored') {
                    alert('Sorry. The title you have chosen contains one or more banned words. Please refer to our acceptable usage policy.');
                    $("#postTitle").val("");
                    $('#postTitle').focus();
                } else if (data!=='False') {
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
                if(data==='True') {
                    alert('Your update has been added.');
                    location.reload();
                } else if (data!=='False') {
                    alert("Database error: please contact the administrator.");    
                } else {
                    alert('Sorry. Unable to add your update.');
                }    
            }
            else {
                alert("Database error: please contact the administrator.");
                $("#postTitle").val("");
            }
        });

        // Hide the add update modal.
        $("#addUpdateModal").modal('toggle');
    };


    /**
     * Clears the fields of the addUpdateModal when it is closed.
     */
    $('#addUpdateModal').on('hidden.bs.modal', function () {
        $('#frmAddUpdate')[0].reset();   
        $("#postTags").tagsinput('removeAll');       
    });


    /**
     * Hide a selected post. (temporarily)
     */
    $.hide_post = function (postID) {
        var panelID = "#panel_post_" + postID
        $(panelID).hide();
    };


    /**
     * Confirms that the user logout wishes to edit their post.
     */
    $.confirm_edit_post = function() {
        return confirm("Are you sure you want to save your changes?");
    };


    /**
     * Handles the edit user post link click.
     */
    $.edit_post = function (in_postID, in_collapseID) {
    
      // Only allow the user to edit one post at a time
      if (editingPost) {
        alert("You have unsaved changes!");
        return false;
      }
      
      editingPost = true;
      
      var textPostID = "#text_post_" + in_postID;
      originalPostText = $(textPostID).html();  // Store the current post text
      
      // If the collapse is not showing, show it
      var collapsePostID = "#collapse" + in_collapseID;
      $(collapsePostID).collapse("show");

      // Load the page element and insert it into the panel
      url = '/edituserpost/' + in_postID;
      $(textPostID).load(url);
    
      // Focus on the input and position cursor at end of text to edit
      $("#edit_box").focus().val(originalPostText);
      return true;
    };


    /**
     * Handles saving changes to a user's postText.
     */
    $.save_edit_post = function (in_postID) {
        var textPostID = "#text_post_" + in_postID;
        var currentText = $("#edit_box").val();

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
                        if (data === 'True') {
                            alert('Your post has been updated.');
                            location.reload();
                        } else {
                            alert(data);
                            location.reload();
                        }
                    }
                    else {
                        alert("Database error: please contact the administrator.");
                        // redirect to error page instead?
                        location.reload();
                    }
                });
        }
        else {
            alert("Cancelled");
        } 
      };    


    /**
     * Retores the original postText when editing is cancelled.
     */
    $.cancel_edit_post = function (postID) {
      var textPostID = "#text_post_" + postID;
    
      alert("Cancelled");

      $(textPostID).html(originalPostText);   
      editingPost = false;
    };


    /**
     * Stops user from opening or closing post collapses whilst editing.
     */
    $('.collapse_btn').on('click', function(event) {
      if($('#edit_box').length) {
          alert("You still have unsaved changes!");
          event.stopPropagation();
      }
    });


    /**
     * Confirms that the user logout wishes to delete their post.
     */
    $.confirm_delete_post = function() {
        return confirm("Are you sure you want to delete this post?");
    };


    /**
     * Handles the delete user post event.
     */
    $.delete_post = function (in_postID) {
        if($.confirm_delete_post()==true) {
            var csrftoken = getCookie('csrftoken');

            $.post("/deleteuserpost/",
                {
                    postID: in_postID,
                    csrfmiddlewaretoken: csrftoken,
                },
                function (data, status) {
                    if (status === 'success') {
                        if (data === 'True') {
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
        else {
            alert("Delete cancelled");
        }
    };

});
